"""Basic tests for the Variant Lookup API."""

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_variants_returns_list(client):
    response = client.get("/variants")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 5


def test_get_variants_has_expected_fields(client):
    response = client.get("/variants")
    data = response.get_json()
    variant = data[0]
    assert "id" in variant
    assert "gene" in variant
    assert "chrom" in variant
    assert "pos" in variant


# NOTE: More tests needed — participants will add these with Claude's help
