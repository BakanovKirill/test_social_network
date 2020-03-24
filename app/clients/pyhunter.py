from pyhunter import PyHunter
from requests import HTTPError


class PyHunterClient:
    def __init__(self, key: str):
        self.cli = PyHunter(key)

    def verify_email(self, email: str):
        try:
            return self.cli.email_verifier(email)
        except HTTPError as exc:
            print(f"Exception requesting Enrichment for email {email}:\n {exc}")
            return None
