import unittest

from fastapi.testclient import TestClient

from app.config.database import Base, SessionLocal, engine
from app.main import app
from app.model.user_model import User


class APITestCase(unittest.TestCase):
    auth_prefix = "/api/v1/auth"
    admin_users_prefix = "/api/v1/admin/users"
    movies_prefix = "/api/v1/movie/movies"

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def setUp(self) -> None:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self._seed_admin_user()
        self.auth_headers = self._login_headers()

    def _seed_admin_user(self) -> None:
        db = SessionLocal()
        try:
            user = User(email="admin@example.com", password="secret123", role="admin")
            db.add(user)
            db.commit()
        finally:
            db.close()

    def _login_headers(self) -> dict:
        response = self.client.post(
            f"{self.auth_prefix}/login",
            json={"email": "admin@example.com", "password": "secret123"},
        )
        token = response.json()["token"]
        return {"Authorization": f"Bearer {token}"}

    def _register_user(self, email: str, password: str = "secret123") -> dict:
        response = self.client.post(
            f"{self.auth_prefix}/register",
            json={"email": email, "password": password},
        )
        self.assertEqual(response.status_code, 201)
        return response.json()

    def test_login_returns_token(self) -> None:
        response = self.client.post(
            f"{self.auth_prefix}/login",
            json={"email": "admin@example.com", "password": "secret123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_register_creates_public_user_with_default_role(self) -> None:
        response = self.client.post(
            f"{self.auth_prefix}/register",
            json={"email": "user@example.com", "password": "secret123"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["role"], "user")
        self.assertEqual(response.json()["email"], "user@example.com")

    def test_register_rejects_duplicate_email(self) -> None:
        self._register_user("user@example.com")

        response = self.client.post(
            f"{self.auth_prefix}/register",
            json={"email": "user@example.com", "password": "secret123"},
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "User already exists")

    def test_movie_crud_flow(self) -> None:
        create_response = self.client.post(
            self.movies_prefix,
            json={
                "title": "The Matrix",
                "overview": "A hacker discovers the reality behind his world.",
                "year": 1999,
                "rating": 9,
                "category": "SciFi",
            },
        )
        self.assertEqual(create_response.status_code, 201)
        movie_id = create_response.json()["id"]

        get_response = self.client.get(f"{self.movies_prefix}/{movie_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"], "The Matrix")

        update_response = self.client.put(
            f"{self.movies_prefix}/{movie_id}",
            json={
                "title": "The Matrix Reloaded",
                "overview": "Neo continues the fight against the machines in Zion.",
                "year": 2003,
                "rating": 8,
                "category": "SciFi",
            },
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["title"], "The Matrix Reloaded")

        delete_response = self.client.delete(f"{self.movies_prefix}/{movie_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(
            delete_response.json()["message"],
            "Deleted movie successfully",
        )

    def test_movie_not_found_returns_404(self) -> None:
        response = self.client.get(f"{self.movies_prefix}/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Movie not found")

    def test_create_many_movies_requires_non_empty_payload(self) -> None:
        response = self.client.post(f"{self.movies_prefix}/all", json=[])
        self.assertEqual(response.status_code, 400)
        self.assertIn("At least one movie is required", response.json()["detail"])

    def test_admin_endpoints_require_admin_role(self) -> None:
        user_response = self._register_user("user@example.com")
        login_response = self.client.post(
            f"{self.auth_prefix}/login",
            json={"email": "user@example.com", "password": "secret123"},
        )
        self.assertEqual(login_response.status_code, 200)
        headers = {"Authorization": f"Bearer {login_response.json()['token']}"}

        response = self.client.get(self.admin_users_prefix, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "Admin access required")

        self.assertEqual(user_response["role"], "user")

    def test_admin_can_list_get_update_and_delete_users(self) -> None:
        user_response = self._register_user("user@example.com")

        list_response = self.client.get(self.admin_users_prefix, headers=self.auth_headers)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()), 2)

        get_response = self.client.get(
            f"{self.admin_users_prefix}/{user_response['id']}",
            headers=self.auth_headers,
        )
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["email"], "user@example.com")

        update_response = self.client.put(
            f"{self.admin_users_prefix}/{user_response['id']}",
            headers=self.auth_headers,
            json={
                "email": "editor@example.com",
                "password": "updated123",
                "role": "admin",
            },
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["email"], "editor@example.com")
        self.assertEqual(update_response.json()["role"], "admin")

        duplicate_response = self.client.put(
            f"{self.admin_users_prefix}/{user_response['id']}",
            headers=self.auth_headers,
            json={
                "email": "admin@example.com",
                "password": "updated123",
                "role": "admin",
            },
        )
        self.assertEqual(duplicate_response.status_code, 409)
        self.assertEqual(duplicate_response.json()["detail"], "User already exists")

        delete_response = self.client.delete(
            f"{self.admin_users_prefix}/{user_response['id']}",
            headers=self.auth_headers,
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.json()["message"], "Deleted user successfully")

    def test_admin_endpoints_return_404_for_missing_user(self) -> None:
        get_response = self.client.get(f"{self.admin_users_prefix}/999", headers=self.auth_headers)
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_response.json()["detail"], "User not found")

        delete_response = self.client.delete(
            f"{self.admin_users_prefix}/999",
            headers=self.auth_headers,
        )
        self.assertEqual(delete_response.status_code, 404)
        self.assertEqual(delete_response.json()["detail"], "User not found")


if __name__ == "__main__":
    unittest.main()
