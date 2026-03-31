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


import app as app_module


@pytest.fixture(autouse=True)
def reset_variants():
    original = list(app_module.variants)
    yield
    app_module.variants.clear()
    app_module.variants.extend(original)


def test_delete_variant_returns_204(client):
    response = client.delete("/variants/1")
    assert response.status_code == 204


def test_delete_variant_removes_it(client):
    client.delete("/variants/1")
    response = client.get("/variants")
    ids = [v["id"] for v in response.get_json()]
    assert 1 not in ids


def test_delete_variant_not_found_returns_404(client):
    response = client.delete("/variants/999")
    assert response.status_code == 404


def test_delete_variant_invalid_id_returns_400(client):
    response = client.delete("/variants/abc")
    assert response.status_code == 400
