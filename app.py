"""Variant Lookup API — a simple Flask app for querying genomic variants."""

import os
from functools import wraps

from flask import Flask, request, jsonify

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

REQUIRED_FIELDS = {
    "gene": str,
    "chrom": str,
    "pos": int,
    "ref": str,
    "alt": str,
    "qual": float,
}


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        expected_key = os.getenv("API_KEY")
        if not expected_key:
            return jsonify({"error": "server misconfigured"}), 500
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split(" ", 1)
        if len(parts) != 2 or parts[0] != "Bearer" or parts[1] != expected_key:
            return jsonify({"error": "unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper


@app.errorhandler(Exception)
def handle_unexpected_error(exc: Exception):
    return jsonify({"error": "an unexpected error occurred"}), 500


@app.route("/variants", methods=["GET"])
def get_variants():
    return jsonify(variants)


@app.route("/variants/<variant_id>", methods=["GET"])
def get_variant(variant_id: str):
    try:
        parsed_id = int(variant_id)
    except ValueError:
        return jsonify({"error": "id must be an integer"}), 400
    matched = [v for v in variants if v["id"] == parsed_id]
    if not matched:
        return jsonify({"error": "variant not found"}), 404
    return jsonify(matched[0]), 200


@app.route("/variants", methods=["POST"])
@require_api_key
def add_variant():
    global next_id
    body = request.get_json(force=True, silent=True)
    if body is None or not isinstance(body, dict):
        return jsonify({"error": "request body must be valid JSON"}), 400

    for field_name in REQUIRED_FIELDS:
        if field_name not in body:
            return jsonify({"error": f"missing required field: {field_name}"}), 400

    for extra_key in body:
        if extra_key not in REQUIRED_FIELDS:
            return jsonify({"error": f"unexpected field: {extra_key}"}), 400

    for field_name, expected_type in REQUIRED_FIELDS.items():
        value = body[field_name]
        if expected_type is float:
            if not isinstance(value, (int, float)):
                return jsonify({"error": f"invalid type for field: {field_name}"}), 400
            body[field_name] = float(value)
        elif not isinstance(value, expected_type):
            return jsonify({"error": f"invalid type for field: {field_name}"}), 400

    body["id"] = next_id
    next_id += 1
    variants.append(body)
    return jsonify(body), 201


@app.route("/variants/search", methods=["GET"])
def search_variants():
    gene = request.args.get("gene")
    if gene:
        # BUG 6: Case-sensitive comparison — "brca1" won't match "BRCA1"
        results = [v for v in variants if v["gene"] == gene]
    else:
        results = variants
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", port=5001)
