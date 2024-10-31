# PICA project 'Toegankelijke Kaartencollectie'

Dit project richt zich op het verbeteren van de toegankelijkheid en deelbaarheid van de gedigitaliseerde kaartencollectie van de Bibliotheek UvA/HvA/Allard Pierson. We verrijken de kaarten met metadata en duurzame identifiers en maken annotatie van de kaarten mogelijk.

Tijdens deze pilot selecteren we representatieve kaarten om te bepalen hoe we verrijkte metadata modelleren en duurzaam opslaan in de systemen van de Bibliotheek en het Allard Pierson. De uitkomsten helpen ons een efficiënte workflow te ontwikkelen voor dit project en toekomstige Linked Open Data-campagnes.

## Samenwerking

Dit project wordt uitgevoerd door de Bibliotheek UvA/HvA en het Allard Pierson museum en wordt ondersteund door de Amsterdam Time Machine (https://www.amsterdamtimemachine.nl/) en het CREATE Lab (https://www.create.humanities.uva.nl/). Hiermee combineren we:
* Inhoudelijke kennis van cartografisch erfgoed
* Expertise in metadatering en digitaal collectiebeheer
* Innovatieve Linked Open Datatechnieken
* Ervaring met het open en 'FAIR' ontsluiten van gedigitaliseerde kaartencollecties

## Datamodel en LOD-template
Nieuw in dit project is dat we de notie van het individuele item in de linked data van de UB introduceren. Het is immers het individuele item waarvan een gedigitaliseerde kopie te zien is via een IIIF Manifest. Aanvullend maken we ook een aanzet tot het modelleren van de individuele kaarten, waarvoor mogelijk andere metadata voorhanden is dan voor het hele werk waar de kaarten onderdeel van uitmaken. Hiervoor hebben we een model in schema.org opgesteld waarin we onderscheid maken tussen het niveau van Manifestation, Item en Kaart, waarmee het in de toekomst mogelijk wordt om meerdere versies van dezelfde kaart (bijvoorbeeld in verschillende collecties) eenvoudig met elkaar te kunnen verbinden.

Zie [`template.md`](docs/template.md) voor ons model in schema.org. 

## Selectie van kaarten

In dit pilotproject hebben we 25 kaarten geselecteerd uit de collectie van de Bibliotheek UvA/HvA/Allard Pierson. Deze kaarten zijn representatief voor de verschillende typen kaarten in de collectie en bevatten een breed scala aan metadata. De helft van de kaartselectie heeft betrekking op Amsterdam, de andere helft op voormalig Nederlands-Indië, met het oog op integratie in de Amsterdam Time Machine en het GLOBALISE-project (https://globalise.huygens.knaw.nl).

De kaartselectie is opgenomen in [`selectie.csv`](selectie.csv) en is als één IIIF Manifest in [`manifest.json`](manifest.json) gemodelleerd zodat de kaarten eenvoudig in een viewer kunnen worden getoond én waardoor de kaarten gegeorefereerd kunnen worden in Allmaps (https://allmaps.org/). De Canvas identifiers uit de oorspronkelijke manifesten zijn hierin hergebruikt. Het manifest bevat, indien beschikbaar, een extra annotationpage met daarin de georeferentie-annotatie uit Allmaps.

Bekijk de selectie in [Mirador](https://projectmirador.org/embed/?iiif-content=https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/manifest.json) of in [Allmaps](https://editor.allmaps.org/#/collection?url=https%3A%2F%2Famsterdamtimemachine.github.io%2Fpica-toegankelijke-kaartcollectie%2Fmanifest.json).

De URI van dit manifest is: [`https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/manifest.json`](https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/manifest.json).

### Alternatief

Als alternatief is er ook een IIIF Collection beschikbaar die de bestaande manifesten uit de UvA Beeldbank samen aanbiedt: [`https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/collection.json`](https://amsterdamtimemachine.github.io/pica-toegankelijke-kaartcollectie/collection.json). Hierin zijn geen annotaties opgenomen.
