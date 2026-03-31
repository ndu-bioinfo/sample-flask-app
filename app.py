"""Variant Lookup API — a simple Flask app for querying genomic variants."""

import logging
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory variant store
variants = [
    {"id": 1, "gene": "BRCA1", "chrom": "17", "pos": 43044295, "ref": "A", "alt": "G", "qual": 99.0},
    {"id": 2, "gene": "Brca2", "chrom": "13", "pos": 32315474, "ref": "C", "alt": "T", "qual": 85.5},
    {"id": 3, "gene": "TP53",  "chrom": "17", "pos": 7676154,  "ref": "G", "alt": "A", "qual": 92.3},
    {"id": 4, "gene": "EGFR",  "chrom": "7",  "pos": 55259515, "ref": "T", "alt": "C", "qual": 78.1},
    {"id": 5, "gene": "KRAS",  "chrom": "12", "pos": 25398284, "ref": "C", "alt": "A", "qual": 95.7},
]

next_id = 6


@app.route("/variants", methods=["GET"])
def get_variants():
    response = jsonify(variants)
    logger.info("%s %s %d", request.method, request.path, response.status_code)
    return response


@app.route("/variants/<id>", methods=["GET"])
def get_variant(id):
    # BUG 1: No type conversion — id comes in as string, compared to int
    # BUG 2: Off-by-one — using id as index instead of matching by id field
    variant = variants[int(id)]
    response = jsonify(variant)
    logger.info("%s %s %d", request.method, request.path, response.status_code)
    return response


@app.route("/variants", methods=["POST"])
def add_variant():
    global next_id
    # BUG 3: No input validation — accepts any JSON (or crashes on non-JSON)
    data = request.get_json()
    # BUG 4: No check for required fields
    data["id"] = next_id
    next_id += 1
    variants.append(data)
    # BUG 5: Returns 200 instead of 201 for resource creation
    response = jsonify(data)
    logger.info("%s %s %d", request.method, request.path, response.status_code)
    return response


# TODO: add authentication — currently anyone can read/write variants


@app.route("/variants/search", methods=["GET"])
def search_variants():
    gene = request.args.get("gene")
    if gene:
        # BUG 6: Case-sensitive comparison — "brca1" won't match "BRCA1"
        results = [v for v in variants if v["gene"] == gene]
    else:
        results = variants
    response = jsonify(results)
    logger.info("%s %s %d", request.method, request.path, response.status_code)
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5001)
