# Biolink Beacon

A knowledge beacon implementation for the Monarch Biolink API (https://api.monarchinitiative.org/api/), a biomedical data source containing information about diseases, phenotypes, and genes, and the relations between them.

## Getting the Project

The **biolink-beacon** package is not yet available through PyPI, thus, to install, clone this repo using git.

```bash
git clone https://github.com/NCATS-Tangerine/biolink-beacon

# ... then  enter  into your cloned project repository
cd biolink-beacon
```

## Installing and Running without Docker

First, create a virtual environment:

```shell
python3.7 -m venv venv
source venv/bin/activate
```

The application expects to use a Python release 3.7.4 or newer binary (note that your binary in the `venv` command 
above may just be typed as `python3.7`, `python3` or even just `python` but the `python --version` should 
resolve to 3.7.4 or better). 

Next, make sure that your pip version is 3.7 compliant. It is also a good idea to ensure that you have the latest version of 
pip for your venv:

```shell
python -m pip install --upgrade pip
```

### Site Configuration

The beacon server runtime relies on a `swagger.yaml` file sitting under `server/swagger_server/swagger`. Two templates 
are currently provided - one assuming a development 'localhost' host and root basepath; the other for NCATS endpoint 
deployment. Copy over one or the other template into a file named `swagger.yaml` within the same directory.

### Dependencies

Then, run the following commands within the `biolink-beacon` directory. Note that errors may result if `ontobio` and 
connexion[swagger-ui] are not installed separately.

```shell
pip install ontobio
pip install -r requirements.txt
pip install connexion[swagger-ui]
pip install client/
pip install server/
cd server/
python -m swagger_server
```

## Running with Docker

```shell
docker build -t ncats:biolink .
docker run -d --rm --name biolink -p 8080:8080 ncats:biolink
```

This will run the Docker container named 'biolink' as a daemon on port 8080.

Navigate to http://localhost:8080 in your browser to see the Swagger UI or whichever URL to which you have aliased 
the server (e.g. for NCATS, might be something like https://kba.ncats.io/beacon/biolink).

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
