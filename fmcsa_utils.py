import os
import requests

FMCSA_API_KEY = os.getenv("FMCSA_API_KEY")
BASE_URL = "https://mobile.fmcsa.dot.gov/qc/services"

def verify_mc(mc_number: str) -> dict:
    if not FMCSA_API_KEY:
        return {"error": "FMCSA API key not set in environment"}

    url = f"{BASE_URL}/carriers/docket-number/{mc_number}"
    params = {"webKey": FMCSA_API_KEY}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": "Failed to fetch data from FMCSA",
            "details": str(e),
            "status_code": getattr(e.response, 'status_code', None)
        }

