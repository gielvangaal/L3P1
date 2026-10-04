# L3P1 Data Engineering

## Structuur

- `data/raw` - ruwe bronbestanden
- `data/processed` - verwerkte output
- `src/config.py` - bestandslocaties
- `src/extract.py` - data inladen
- `src/transform.py` - data opschonen en transformeren
- `src/validate.py` - basiscontroles op data
- `src/load.py` - output wegschrijven
- `src/model.py` - merges/relaties per user story
- `src/measures.py` - berekende measures
- `src/visuals.py` - visualisaties
- `main.py` - startpunt van de pipeline

## Werkwijze

1. Bronnen inladen
2. Data transformeren
3. Data valideren
4. Verwerkte data opslaan
5. `DimCountry` opbouwen
6. Benodigde tabellen per user story mergen
7. Measures berekenen
8. Visualisaties maken

## Dependencies

Dependencies staan in `requirements.txt`.

Installeren met:

```bash
pip install -r requirements.txt
```

## Git
De inhoud van data/ wordt niet meegenomen in Git.