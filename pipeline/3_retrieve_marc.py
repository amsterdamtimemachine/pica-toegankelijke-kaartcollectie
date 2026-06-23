import json

from lxml import etree
from pymarc import marcxml

import requests
import requests_cache

requests_cache.install_cache(
    ".cache", expire_after=60 * 60 * 24 * 7 * 31
)  # Cache for 1 month


def process_marc():

    with open("data/identifiers.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter to process only maps
    maps_to_process = [item for item in data if item.get("is_map")]
    print(f"Retrieving MARC for {len(maps_to_process)} map items...")

    for i, item in enumerate(maps_to_process):
        if i > 0 and i % 50 == 0:
            print(f"Processed {i} items...")

        if "marc21" in item:
            continue

        pid = item.get("pid", "")
        alma_id = pid.split("pid.uba.uva.nl/ark:/88238/b1")[-1] if pid else None

        oai_url = f"https://uva.alma.exlibrisgroup.com/view/oai/31UKB_UAM1_INST/request?verb=GetRecord&identifier=oai:alma.31UKB_UAM1_INST:{alma_id}&metadataPrefix=marc21"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        try:
            response = requests.get(oai_url, headers=headers)
            if response.status_code != 200:
                continue

            root = etree.fromstring(response.content)
            record_elements = root.xpath(
                "//*[local-name()='record' and namespace-uri()='http://www.loc.gov/MARC21/slim']"
            )

            if not record_elements:
                # Some OAI-PMH use no namespace or different namespace prefixes
                record_elements = root.xpath("//*[local-name()='record']")

            # Make sure it's the MARC record, not the OAI header record
            marc_record = None
            for r in record_elements:
                if r.xpath(".//*[local-name()='datafield']"):
                    marc_record = r
                    break

            if marc_record is not None:
                marc_xml_bytes = etree.tostring(marc_record)

                # Parse with pymarc
                records = marcxml.parse_xml_to_array(marc_xml_bytes)
                if records:
                    record = records[0]
                    item["marc21"] = record.as_dict()
            else:
                print(f"No MARC record found for {alma_id}")

        except Exception as e:
            print(f"Error processing MARC for {alma_id}: {e}")

    with open("data/maps.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Saved to data/maps.json")


if __name__ == "__main__":
    process_marc()
