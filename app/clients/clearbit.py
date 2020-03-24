import clearbit
from requests import HTTPError


class ClearBitClient:
    def __init__(self, key: str):
        clearbit.key = key

    @staticmethod
    def get_enrichment(email: str):
        try:
            return clearbit.Enrichment.find(email=email, stream=True)
        except HTTPError as exc:
            print(f"Exception requesting Enrichment for email {email}:\n {exc}")
            return None
