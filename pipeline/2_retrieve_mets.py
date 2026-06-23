import json
from lxml import etree

import requests
import requests_cache

requests_cache.install_cache(
    ".cache", expire_after=60 * 60 * 24 * 7 * 31
)  # Cache for 1 month


def process_mets(identifiers_file="data/identifiers.json"):

    with open(identifiers_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Processing {len(data)} items...")

    for i, item in enumerate(data):
        if i > 0 and i % 100 == 0:
            print(f"Processed {i} items...", end="\r")

        # Check if already processed
        if "pid" in item or "is_map" in item:
            continue

        # Build the new OAI METS URL
        item_id = item.get("item_id")
        if not item_id:
            item_id = item["mets_link"].split("=")[-1]

        mets_url = f"https://uvaerfgoed.nl/viewer/oai?verb=GetRecord&metadataPrefix=mets&identifier={item_id}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        response = requests.get(mets_url, headers=headers)
        if response.status_code != 200:
            continue

        # Parse XML
        print(response.url)  # TODO DEBUG
        print(response.content)  # TODO DEBUG
        root = etree.fromstring(response.content)

        type_ap_elements = root.xpath("//*[local-name()='type_ap']")
        ark_elements = root.xpath("//*[local-name()='ark']")

        type_ap = type_ap_elements[0].text if type_ap_elements else ""
        ark_link = ark_elements[0].text if ark_elements else ""

        if ark_link:
            item["pid"] = ark_link

        item["type_ap"] = type_ap

        # Filter on 'map'
        if type_ap and "map" in type_ap.lower():
            item["is_map"] = True
        else:
            item["is_map"] = False

    maps_count = sum(1 for item in data if item.get("is_map"))
    print(f"\nFound {maps_count} map items.")

    with open(identifiers_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Saved to {identifiers_file}")


if __name__ == "__main__":
    process_mets()
