import json
import urllib.request
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader


def harvest_identifiers(url):
    opener = urllib.request.build_opener()
    urllib.request.install_opener(opener)

    registry = MetadataRegistry()
    registry.registerReader("oai_dc", oai_dc_reader)
    client = Client(url, registry)

    identifiers_data = []

    print("Harvesting identifiers...")

    headers = client.listIdentifiers(metadataPrefix="oai_dc")
    for header in headers:

        identifier = header.identifier()
        date = header.datestamp()
        if hasattr(date, "isoformat"):
            date = date.isoformat()

        mets_link = f"https://uvaerfgoed.nl/viewer/oai?verb=GetRecord&metadataPrefix=mets&identifier={identifier}"
        manifest_link = (
            f"https://uvaerfgoed.nl/viewer/api/v1/records/{identifier}/manifest/"
        )

        identifiers_data.append(
            {
                "id": identifier,
                "date": date,
                "mets_link": mets_link,
                "manifest_link": manifest_link,
            }
        )

        if len(identifiers_data) > 0 and len(identifiers_data) % 100 == 0:
            print(f"Harvested {len(identifiers_data)}...", end="\r")

    print(f"\nHarvested {len(identifiers_data)} identifiers.")

    with open("data/identifiers.json", "w", encoding="utf-8") as f:
        json.dump(identifiers_data, f, indent=4)

    print("Saved to data/identifiers.json")


if __name__ == "__main__":
    URL = "https://uvaerfgoed.nl/viewer/oai"

    harvest_identifiers(URL)
