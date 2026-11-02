"""
API Tests for the College Helpdesk system.

These tests verify the REST API endpoints work correctly.
Requires the backend to be running and database to be seeded.

Usage:
    python -m pytest tests/test_api.py -v
"""
import pytest
import requests
import os

BASE_URL = os.getenv("API_URL", "http://localhost:8000")


def get_auth_token(username="student1", password="password123"):
    """Helper to get an authentication token."""
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


class TestHealthCheck:
    def test_root(self):
        try:
            response = requests.get(f"{BASE_URL}/")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_health(self):
        try:
            response = requests.get(f"{BASE_URL}/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")


class TestAuthentication:
    def test_login_success(self):
        try:
            response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "username": "student1",
                "password": "password123"
            })
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"
            assert data["role"] == "student"
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_login_admin(self):
        try:
            response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "username": "admin",
                "password": "admin123"
            })
            assert response.status_code == 200
            data = response.json()
            assert data["role"] == "admin"
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_login_failure(self):
        try:
            response = requests.post(f"{BASE_URL}/api/auth/login", json={
                "username": "student1",
                "password": "wrongpassword"
            })
            assert response.status_code == 401
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_get_me(self):
        try:
            token = get_auth_token()
            if not token:
                pytest.skip("Could not authenticate")
            response = requests.get(f"{BASE_URL}/api/auth/me", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            data = response.json()
            assert data["username"] == "student1"
            assert data["role"] == "student"
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")


class TestUnauthorizedAccess:
    def test_no_token(self):
        try:
            response = requests.get(f"{BASE_URL}/api/auth/me")
            assert response.status_code == 401
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_invalid_token(self):
        try:
            response = requests.get(f"{BASE_URL}/api/auth/me", headers={
                "Authorization": "Bearer invalid_token_here"
            })
            assert response.status_code == 401
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_student_cannot_access_admin(self):
        try:
            token = get_auth_token("student1", "password123")
            if not token:
                pytest.skip("Could not authenticate")
            response = requests.get(f"{BASE_URL}/api/admin/analytics", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 403
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")


class TestStudentEndpoints:
    def test_get_notices(self):
        try:
            token = get_auth_token()
            if not token:
                pytest.skip("Could not authenticate")
            response = requests.get(f"{BASE_URL}/api/student/notices", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            notices = response.json()
            assert isinstance(notices, list)
            assert len(notices) > 0
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_get_timetable(self):
        try:
            token = get_auth_token()
            if not token:
                pytest.skip("Could not authenticate")
            response = requests.get(
                f"{BASE_URL}/api/student/timetable",
                params={"department": "Computer Science", "semester": 5},
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            timetable = response.json()
            assert isinstance(timetable, list)
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")


class TestChatEndpoint:
    def test_chat_unauthorized(self):
        try:
            response = requests.post(f"{BASE_URL}/api/chat/ask", json={
                "question": "What is the fee?"
            })
            assert response.status_code == 401
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_chat_ask(self):
        try:
            token = get_auth_token()
            if not token:
                pytest.skip("Could not authenticate")
            response = requests.post(
                f"{BASE_URL}/api/chat/ask",
                headers={"Authorization": f"Bearer {token}"},
                json={"question": "What is the attendance requirement?"},
                timeout=60
            )
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "sources" in data
            assert "conversation_id" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")
        except requests.exceptions.Timeout:
            pytest.skip("Request timed out (LLM may not be configured)")

    def test_chat_history(self):
        try:
            token = get_auth_token()
            if not token:
                pytest.skip("Could not authenticate")
            response = requests.get(f"{BASE_URL}/api/chat/history", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")


class TestAdminEndpoints:
    def test_admin_analytics(self):
        try:
            token = get_auth_token("admin", "admin123")
            if not token:
                pytest.skip("Could not authenticate as admin")
            response = requests.get(f"{BASE_URL}/api/admin/analytics", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            data = response.json()
            assert "total_users" in data
            assert "total_documents" in data
            assert "total_queries" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_admin_get_documents(self):
        try:
            token = get_auth_token("admin", "admin123")
            if not token:
                pytest.skip("Could not authenticate as admin")
            response = requests.get(f"{BASE_URL}/api/admin/documents", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            assert isinstance(response.json(), list)
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")

    def test_admin_get_faqs(self):
        try:
            token = get_auth_token("admin", "admin123")
            if not token:
                pytest.skip("Could not authenticate as admin")
            response = requests.get(f"{BASE_URL}/api/admin/faqs", headers={
                "Authorization": f"Bearer {token}"
            })
            assert response.status_code == 200
            faqs = response.json()
            assert isinstance(faqs, list)
            assert len(faqs) > 0
        except requests.exceptions.ConnectionError:
            pytest.skip("Server is not running")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
