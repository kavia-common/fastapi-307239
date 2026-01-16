from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.query("/items/")
def query_items(q: str = ""):
    """
    Test endpoint for QUERY method.
    """
    return {"items": ["item1", "item2"], "query": q}


@app.query("/search/{item_id}")
def query_item(item_id: int, q: str = ""):
    """
    Test endpoint for QUERY method with path parameter.
    """
    return {"item_id": item_id, "query": q}


client = TestClient(app)


def test_query_method():
    """
    Test QUERY method routing.
    """
    response = client.request("QUERY", "/items/")
    assert response.status_code == 200
    assert response.json() == {"items": ["item1", "item2"], "query": ""}


def test_query_method_with_query_params():
    """
    Test QUERY method with query parameters.
    """
    response = client.request("QUERY", "/items/?q=test")
    assert response.status_code == 200
    assert response.json() == {"items": ["item1", "item2"], "query": "test"}


def test_query_method_with_path_param():
    """
    Test QUERY method with path parameter.
    """
    response = client.request("QUERY", "/search/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "query": ""}


def test_query_method_with_path_and_query_params():
    """
    Test QUERY method with both path and query parameters.
    """
    response = client.request("QUERY", "/search/42?q=test")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "query": "test"}


def test_openapi_schema_includes_query():
    """
    Test that OpenAPI schema includes QUERY method.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_schema = response.json()
    
    # Check that /items/ path exists and has query method
    assert "/items/" in openapi_schema["paths"]
    assert "query" in openapi_schema["paths"]["/items/"]
    
    # Check that /search/{item_id} path exists and has query method
    assert "/search/{item_id}" in openapi_schema["paths"]
    assert "query" in openapi_schema["paths"]["/search/{item_id}"]
