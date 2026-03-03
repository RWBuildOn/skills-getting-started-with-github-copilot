def test_unregister_removes_existing_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "message" in payload

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload


def test_unregister_non_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not-enrolled@mergington.edu"},
    )

    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload


def test_unregister_missing_email_returns_422(client):
    response = client.delete("/activities/Chess%20Club/participants")

    assert response.status_code == 422
    payload = response.json()
    assert "detail" in payload
