import pandas as pd
import iiif_prezi3

iiif_prezi3.config.configs["helpers.auto_fields.AutoLang"].auto_lang = "nl"


def main():
    df = pd.read_csv("selectie.csv")

    manifest = iiif_prezi3.Manifest(
        id="https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/manifest.json",
        label="Selectie kaarten voor het PICA-project 'Toegankelijke Kaartencollectie' van de Universiteit van Amsterdam",
    )

    for i in df.itertuples():

        iiif_service_info = i.Beeldbank_iiif_info
        canvas_id = i.Beeldbank_iiif_canvas
        label = f"{i.index} - {i.Titel}"

        uri_handle = i.Beeldbank
        uri_ark = i.URI
        uri_manifest = i.Beeldbank_iiif_manifest

        manifest.make_canvas_from_iiif(
            url=iiif_service_info,
            id=canvas_id,
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

    with open("manifest.json", "w") as outfile:
        outfile.write(manifest.json(indent=2))


if __name__ == "__main__":
    main()
