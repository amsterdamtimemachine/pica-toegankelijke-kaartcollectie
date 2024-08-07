import pandas as pd
import iiif_prezi3

iiif_prezi3.config.configs["helpers.auto_fields.AutoLang"].auto_lang = "nl"

PREFIX = "https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/"


def main():
    df = pd.read_csv("selectie.csv")

    collection = iiif_prezi3.Collection(
        id=f"{PREFIX}collection.json",
        label="Selectie kaarten voor het PICA-project 'Toegankelijke Kaartencollectie' van de Universiteit van Amsterdam",
    )

    for i in df.itertuples():

        manifest_id = i.Beeldbank_iiif_manifest

        collection.add_item(
            iiif_prezi3.Reference(
                id=manifest_id,
                label=f"{i.index} - {i.Titel}".strip(),
                type="Manifest",
            )
        )

    with open("collection.json", "w") as outfile:
        outfile.write(collection.json(indent=2))


if __name__ == "__main__":
    main()
