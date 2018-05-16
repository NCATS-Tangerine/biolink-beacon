# Biolink Beacon

A knowledge beacon implementation for the Monarch Biolink API (https://api.monarchinitiative.org/api/), a biomedical data source containing information about diseases, phenotypes, and genes, and the relations between them.

## Running with Docker

```shell
docker build -t ncats:biolink .
docker run -d --rm --name biolink -p 8078:8080 ncats:biolink
```

This will run the Docker container named 'biolink' as a daemon.

Navigate to http://localhost:8078/ui/ in your browser to see the Swagger UI

Sometimes, if you get an unexpected runtime error, docker will fail and exit silently, denying you access to the log message of the error.  In such a situation, you need to run docker directly to see the error. In that case, omit the **-d** argument in the previous docker run command, i.e.

```shell
docker run -rm --name biolink -p 8078:8080 ncats:biolink
```
The runtime error should now show up on your console.

## Usage
http://localhost:8080/concepts?keywords=FANC&pageSize=1
```
[
  {
    "definition": "A Fanconi anemia that has_material_basis_in homozygous or compound heterozygous mutation in the FANCA gene on chromosome 16q24.",
    "id": "MONDO:0009215",
    "name": "Fanconi anemia complementation group a",
    "synonyms": [
      "Estren-Dameshek Variant of Fanconi Anemia",
      "FANCONI ANEMIA, COMPLEMENTATION GROUP A",
      "Fanconi Anemia",
      "FANCA",
      "Fanconi Anemia, Estren-Dameshek Variant",
      "Estren-Dameshek Variant of Fanconi Pancytopenia",
      "Fanconi anemia complementation group type A",
      "FANCONI ANEMIA, COMPLEMENTATION GROUP A; FANCA",
      "Fanconi Anemia, Complementation Group type a"
    ],
    "type": "disease"
  }
]
```
http://localhost:8080/statements?s=MONDO:0009215&pageSize=1

```
[
  {
    "id": "BLM:06c7f4a5-65e5-4243-bbdd-ab92ced62997",
    "object": {
      "id": "HP:0000252",
      "name": "Microcephaly",
      "type": "phenotype"
    },
    "predicate": {
      "id": "RO:0002200",
      "name": "has phenotype"
    },
    "subject": {
      "id": "MONDO:0009215",
      "name": "Fanconi anemia complementation group a",
      "type": "disease"
    }
  }
]
```
http://localhost:8080/concepts/HP:0000252
```
[
  {
    "id": "HP:0000252",
    "name": "Microcephaly",
    "synonyms": [
      "Reduced head circumference",
      "Abnormally small skull",
      "Decreased size of cranium",
      "Decreased circumference of cranium",
      "small cranium",
      "Small head circumference",
      "Abnormally small cranium",
      "Decreased size of head",
      "Decreased size of skull",
      "Abnormally small head",
      "Small head",
      "small calvarium",
      "Small skull"
    ],
    "type": "Phenotype"
  }
]
```
