import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = {
        name: {
            key: value.copy() if isinstance(value, list) else value
            for key, value in details.items()
        }
        for name, details in activities.items()
    }

    activities.clear()
    activities.update(
        {
            name: {
                key: value.copy() if isinstance(value, list) else value
                for key, value in details.items()
            }
            for name, details in original.items()
        }
    )

    yield

    activities.clear()
    activities.update(
        {
            name: {
                key: value.copy() if isinstance(value, list) else value
                for key, value in details.items()
            }
            for name, details in original.items()
        }
    )


@pytest.fixture()
def client():
    return TestClient(app)


def test_get_activities_returns_seed_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["participants"]


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    activities_response = client.get("/activities")
    assert "newstudent@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_from_activity(client):
    response = client.delete(
        "/activities/Chess%20Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in response.json()["participants"]

    activities_response = client.get("/activities")
    assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]
