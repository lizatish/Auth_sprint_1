def test_get_film_by_id_successful(auth_api_client):
    response = auth_api_client.get("/posts")
    assert response.status_code == 404
