"""Tests for the FastAPI activities endpoints."""

import pytest


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_redirects_to_static(self, client):
        """Test that GET / redirects to /static/index.html"""
        # Arrange & Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        # Arrange & Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        # Verify all expected activities are present
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Team",
            "Art Club",
            "Drama Club",
            "Math Club",
            "Robotics Club"
        ]
        for activity in expected_activities:
            assert activity in data

    def test_activity_has_required_fields(self, client):
        """Test that each activity has required fields"""
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Soccer Team"
        email = "newemail@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant to the activity"""
        # Arrange
        activity_name = "Basketball Team"
        email = "newstudent@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup fails for nonexistent activity"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self, client):
        """Test signup fails when student is already signed up"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]


class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_unregister_successful(self, client):
        """Test successful unregistration from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        response = client.get("/activities")
        
        # Assert
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregister fails for nonexistent activity"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_nonexistent_participant(self, client):
        """Test unregister fails when participant not in activity"""
        # Arrange
        activity_name = "Soccer Team"
        email = "notinactivity@mergington.edu"  # Not in Soccer Team
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]
