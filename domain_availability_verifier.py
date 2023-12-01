import itertools
import json
import logging
from typing import Literal, Optional

import requests

logger = logging.getLogger(__name__)


class DomainInfo:
    def __init__(
        self, name: str, available: bool, currency: str = None, price: int = None
    ):
        self.name = name
        self.available = available
        self.currency = currency
        if price:
            self.price = price / 1e6
        else:
            self.price = None

    def __str__(self):
        if self.price:
            return f"{self.name} available: {self.price} ({self.currency})"
        else:
            return f"{self.name} not available"


class DomainAvailabilityVerifier:
    def __init__(
        self,
        environment: Literal["OTE", "Production"],
        api_key: str,
        api_secret: str,
        extensions: list[str],
    ):
        if environment == "OTE":
            self.url = "https://api.ote-godaddy.com/v1/domains/available?"
        elif environment == "Production":
            self.url = "https://api.godaddy.com/v1/domains/available?"
        self.headers = {
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        self.extensions = extensions

    def _perform_api_request(self, domains: list[str]) -> Optional[list[dict]]:
        data = json.dumps(domains)
        response = requests.post(self.url, data=data, headers=self.headers)
        response_data = json.loads(response.text)
        if response.status_code == 200:
            return response_data["domains"]
        elif response.status_code == 203:
            logger.warning(
                f'API request returned errors for {len(response_data["errors"])} errors'
            )
            return response_data["domains"]
        else:
            logger.error(
                f"API request failed with with error: {response_data['code']} {response_data['message']}"
            )

    def check_domains_list(self, domain_names: list[str]) -> Optional[list[DomainInfo]]:
        domains = [
            domain_name + domain_extension
            for domain_name, domain_extension in itertools.product(
                domain_names, self.extensions
            )
        ]
        # TODO: check max 500 strings
        response = self._perform_api_request(domains)
        if response:
            domains_info = []
            for row in response:
                domains_info.append(
                    DomainInfo(
                        name=row["domain"],
                        available=row["available"],
                        currency=row.get("currency"),
                        price=row.get("price"),
                    )
                )
            return domains_info
