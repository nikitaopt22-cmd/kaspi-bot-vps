import requests
import time

class KaspiAPI:
    def __init__(self, base_url, client_id, client_secret, token=None):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self._expires = 0

    def _authenticate(self):
        r = requests.post(f"{self.base_url}/oauth/token", data={
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })
        data = r.json()
        self.token = data.get("access_token")
        self._expires = time.time() + int(data.get("expires_in", 3600))

    def _ensure_token(self):
        if not self.token or time.time() > self._expires:
            self._authenticate()

    def headers(self):
        self._ensure_token()
        return {"Authorization": f"Bearer {self.token}"}

    def fetch_invoices(self, params=None):
        r = requests.get(f"{self.base_url}/invoices", headers=self.headers(), params=params or {})
        return r.json()

    def download_invoice(self, invoice_id):
        r = requests.get(f"{self.base_url}/invoices/{invoice_id}/download", headers=self.headers())
        return r.content
