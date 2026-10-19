def test_get_post_by_id(api_client):
    response = api_client.get("/posts/1")

    assert response.status_code == 200

    post = response.json()

    assert post["userId"] == 1
    assert post["id"] == 1
    assert "title" in post
    assert "body" in post

def test_create_post(api_client):
    payload = {
        "title": "Mobile Automation",
        "body": "Testing API integration",
        "userId": 1,
    }

    response = api_client.post("/posts", payload)

    assert response.status_code == 201

    created_post = response.json()

    assert created_post["title"] == payload["title"]
    assert created_post["body"] == payload["body"]
    assert created_post["userId"] == payload["userId"]
    assert "id" in created_post


def test_update_post(api_client):
    payload = {
        "id": 1,
        "title": "Updated Mobile Automation",
        "body": "Testing API updates",
        "userId": 1,
    }

    response = api_client.put("/posts/1", payload)

    assert response.status_code == 200

    updated_post = response.json()

    assert updated_post["id"] == 1
    assert updated_post["title"] == payload["title"]
    assert updated_post["body"] == payload["body"]


def test_delete_post(api_client):
    response = api_client.delete("/posts/1")

    assert response.status_code == 200

    assert response.json() == {}


def test_get_nonexistent_post(api_client):
    response = api_client.get("/posts/999999")

    assert response.status_code == 404


def test_get_nonexistent_post(api_client):
    response = api_client.get("/posts/999999")

    assert response.status_code == 404
    assert response.json() == {}