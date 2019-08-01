def test_root_route(inject_secret_key, patched_open_id_connect, client):
    """Should induce login redirect."""
    response = client.get("/")
    assert response.status_code == 200
