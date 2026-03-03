def test_signup_adds_new_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert signup_response.status_code == 200
    payload = signup_response.json()
    assert "message" in payload

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload


def test_signup_duplicate_participant_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    payload = response.json()
    assert "detail" in payload


def test_signup_missing_email_returns_422(client):
    response = client.post("/activities/Chess%20Club/signup")

    assert response.status_code == 422
    payload = response.json()
    assert "detail" in payload
