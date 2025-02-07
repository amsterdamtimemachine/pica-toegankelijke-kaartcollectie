import json
import hashlib
import requests
import pandas as pd
import iiif_prezi3

iiif_prezi3.config.configs["helpers.auto_fields.AutoLang"].auto_lang = "nl"
iiif_prezi3.load_bundled_extensions()

PREFIX = "https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/"


def make_manifest(df):

    manifest = iiif_prezi3.Manifest(
        id=f"{PREFIX}manifest.json",
        label="Selectie kaarten voor het PICA-project 'Toegankelijke Kaartencollectie' van de Universiteit van Amsterdam",
    )

    for i in df.itertuples():

        index = i.index

        iiif_service_info = i.Beeldbank_iiif_info
        canvas_id = i.Beeldbank_iiif_canvas
        label = f"{index} - {i.Titel}".strip()

        uri_handle = i.Beeldbank
        uri_ark = i.URI
        uri_manifest = i.Beeldbank_iiif_manifest

        manifest.make_canvas_from_iiif(
            url=iiif_service_info,
            id=canvas_id,
            anno_page_id=f"{PREFIX}manifest.json/{index}/p0/page",
            anno_id=f"{PREFIX}manifest.json/{index}/p0/page/anno",
            label=label,
            metadata=[
                iiif_prezi3.KeyValueString(
                    label="Titel",
                    value={"nl": [label]},
                ),
                iiif_prezi3.KeyValueString(
                    label="URI (Beeldbank)",
                    value={"nl": [f'<a href="{uri_handle}">{uri_handle}</a>']},
                ),
                iiif_prezi3.KeyValueString(
                    label="URI (Catalogus)",
                    value={"en": [f'<a href="{uri_ark}">{uri_ark}</a>']},
                ),
                iiif_prezi3.KeyValueString(
                    label="Origineel manifest",
                    value={"en": [f'<a href="{uri_manifest}">{uri_manifest}</a>']},
                ),
            ],
        )

    return manifest


def get_georeferencing_annotations(
    identifier, iiif_service_info, canvas_id, manifest, embedded=False
):

    annotation_page_id = f"{PREFIX}annotations/georeferencing/{identifier}.json"

    try:
        r = requests.get(
            "https://annotations.allmaps.org/", params={"url": iiif_service_info}
        )
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return

    ap = r.json()

    # Change target from image to Canvas
    # ap["items"][0]["target"]["source"] = ap["items"][0]["target"]["source"]["partOf"][0]
    for item in ap["items"]:
        item["target"]["source"] = {
            "id": canvas_id,
            "type": "Canvas",
            "partOf": {"id": manifest.id, "type": "Manifest", "label": manifest.label},
        }

    if not embedded:
        ap = {"id": annotation_page_id, **ap}

        with open(f"annotations/georeferencing/{identifier}.json", "w") as outfile:
            json.dump(ap, outfile, indent=2)

        return iiif_prezi3.Reference(
            id=annotation_page_id,
            label="Georeferencing Annotations made with Allmaps",
            type="AnnotationPage",
        )
    else:
        return ap


def get_navplace_feature(iiif_service_info):

    if iiif_service_info.endswith("/info.json"):
        iiif_service_info = iiif_service_info.replace("/info.json", "")

    allmaps_image_id = hashlib.sha1(iiif_service_info.encode()).hexdigest()[:16]

    try:
        r = requests.get(
            f"https://annotations.allmaps.org/images/{allmaps_image_id}.geojson"
        )
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)
        return

    feature_collection = r.json()

    for feature in feature_collection["features"]:
        del feature["properties"]

    return feature_collection


def main(
    selection_filepath="selectie.csv", output_filepath="manifest.json", embedded=False
):

    df = pd.read_csv(selection_filepath)

    # First, make the manifest
    manifest = make_manifest(df)

    # Then, add georeferencing annotations and save the annotation pages
    for i in df.itertuples():

        identifier = i.index
        iiif_service_info = i.Beeldbank_iiif_info
        canvas_id = i.Beeldbank_iiif_canvas

        ap = get_georeferencing_annotations(
            identifier, iiif_service_info, canvas_id, manifest, embedded=embedded
        )

        if ap is None:
            continue

        navPlace = iiif_prezi3.NavPlace(**get_navplace_feature(iiif_service_info))

        for c in manifest.items:
            if c.id == canvas_id:

                if not c.annotations:
                    c.annotations = []

                c.annotations.append(ap)

                c.navPlace = navPlace

    # Edit context
    manifest_jsonld = manifest.jsonld_dict()
    manifest_jsonld["@context"] = [
        "http://iiif.io/api/extension/navplace/context.json",
        "http://iiif.io/api/presentation/3/context.json",
    ]

    # Save the manifest
    with open(output_filepath, "w") as outfile:
        json.dump(manifest_jsonld, outfile, indent=2)


if __name__ == "__main__":

    # One manifest with external (referenced) annotations
    main(selection_filepath="selectie.csv", output_filepath="manifest.json")

    # And one with embedded annotations
    main(
        selection_filepath="selectie.csv",
        output_filepath="manifest_embedded.json",
        embedded=True,
    )
