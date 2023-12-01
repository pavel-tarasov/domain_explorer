import os
import pathlib

from domain_availability_verifier import DomainAvailabilityVerifier
from word_generator import WordGenerator

if __name__ == "__main__":
    gen = WordGenerator(source_file=pathlib.Path("data", "syllables.txt"))
    words = set()
    for _ in range(100):
        words.add(gen.generate_word(2))
    words = list(words)

    API_KEY = os.environ.get("GODADDY_PRODUCTION_API_KEY")
    API_SECRET = os.environ.get("GODADDY_PRODUCTION_API_SECRET")
    verifier = DomainAvailabilityVerifier(
        environment="Production",
        api_key=API_KEY,
        api_secret=API_SECRET,
        extensions=[".com", ".world", ".place"],
    )
    results = verifier.check_domains_list(domain_names=words)
    if results:
        for result in results:
            print(result)
