# Variant Lookup API

A simple Flask REST API for querying genomic variants. Built as an AI training demo with intentional bugs for participants to find and fix.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Server

```bash
python app.py
```

The server starts in debug mode on http://localhost:5001.

## API Endpoints

### List all variants

```
GET /variants
```

### Get a variant by ID

```
GET /variants/<id>
```

### Add a new variant

```
POST /variants
Content-Type: application/json

{"gene": "ALK", "chrom": "2", "pos": 29415640, "ref": "C", "alt": "T", "qual": 88.0}
```

### Search variants by gene

```
GET /variants/search?gene=BRCA1
```

## Available Genes

| Gene  | Chromosome | Position   |
|-------|------------|------------|
| BRCA1 | 17         | 43044295   |
| BRCA2 | 13         | 32315474   |
| TP53  | 17         | 7676154    |
| EGFR  | 7          | 55259515   |
| KRAS  | 12         | 25398284   |

## Running Tests

```bash
pytest test_app.py -v
```
