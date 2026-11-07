import logging
import requests
from bs4 import BeautifulSoup

URL = "https://www.terminland.de/noris-psychotherapie/online/Autismus-Diagnostik%20Erwachsene%20(GKV)/"

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_page_status():
  response = requests.get(URL, timeout=15)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, "html.parser")
  text = soup.get_text(" ", strip=True).lower()

  if "keine freien termine" in text:
    return "UNAVAILABLE"

  if "keine termine verfügbar" in text:
    return "UNAVAILABLE"

  locations = []

  for label in soup.select("label.tl-radio"):
    radio = label.find("input", type="radio")

    if radio is not None:
      locations.append(label.get_text(" ", strip=True).lower())

  if "nürnberg" in locations and "schwabach" in locations:
    return "POTENTIALLY_AVAILABLE"

  return "UNKNOWN"

if __name__ == "__main__":
  logging.info("Checking Terminland...")

  try:
    status = get_page_status()
    logging.info("Page status: %s", status)

  except requests.RequestException:
    logging.exception("HTTP request failed.")
    raise
