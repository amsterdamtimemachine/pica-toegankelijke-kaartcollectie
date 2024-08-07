import json
import requests
import pandas as pd
import iiif_prezi3

iiif_prezi3.config.configs["helpers.auto_fields.AutoLang"].auto_lang = "nl"

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


def get_georeferencing_annotations(identifier, iiif_service_info):

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
    ap = {"id": annotation_page_id, **ap}

    # Change target from image to Canvas
    ap["items"][0]["target"]["source"] = ap["items"][0]["target"]["source"]["partOf"][0]

    with open(f"annotations/georeferencing/{identifier}.json", "w") as outfile:
        json.dump(ap, outfile, indent=2)

    return iiif_prezi3.Reference(
        id=annotation_page_id,
        label="Georeferencing Annotations made with Allmaps",
        type="AnnotationPage",
    )


def main():

    df = pd.read_csv("selectie.csv")

    # First, make the manifest
    manifest = make_manifest(df)

    # Then, add georeferencing annotations and save the annotation pages
    for i in df.itertuples():

        identifier = i.index
        iiif_service_info = i.Beeldbank_iiif_info
        canvas_id = i.Beeldbank_iiif_canvas

        ap = get_georeferencing_annotations(identifier, iiif_service_info)

        if ap is None:
            continue

        for c in manifest.items:
            if c.id == canvas_id:

                if not c.annotations:
                    c.annotations = []

                c.annotations.append(ap)

    # Save the manifest
    with open("manifest.json", "w") as outfile:
        outfile.write(manifest.json(indent=2))


if __name__ == "__main__":
    main()
