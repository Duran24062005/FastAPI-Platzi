import unittest

from fastapi.testclient import TestClient

from app.config.database import Base, SessionLocal, engine
from app.main import app
from app.model.user_model import User


class APITestCase(unittest.TestCase):
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
            user = User(email="admin@example.com", password="secret123")
            db.add(user)
            db.commit()
        finally:
            db.close()

    def _login_headers(self) -> dict:
        response = self.client.post(
            "/Login",
            json={"email": "admin@example.com", "password": "secret123"},
        )
        token = response.json()["token"]
        return {"Authorization": f"Bearer {token}"}

    def test_login_returns_token(self) -> None:
        response = self.client.post(
            "/Login",
            json={"email": "admin@example.com", "password": "secret123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_movie_crud_flow(self) -> None:
        create_response = self.client.post(
            "/movies",
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

        get_response = self.client.get(f"/movies/{movie_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["title"], "The Matrix")

        update_response = self.client.put(
            f"/movies/{movie_id}",
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

        delete_response = self.client.delete(f"/movies/{movie_id}")
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(
            delete_response.json()["message"],
            "Deleted movie successfully",
        )

    def test_movie_not_found_returns_404(self) -> None:
        response = self.client.get("/movies/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Movie not found")

    def test_create_many_movies_requires_non_empty_payload(self) -> None:
        response = self.client.post("/movies/all", json=[])
        self.assertEqual(response.status_code, 400)
        self.assertIn("At least one movie is required", response.json()["detail"])

    def test_user_endpoints_require_jwt_and_support_queries(self) -> None:
        create_response = self.client.post(
            "/create_user/",
            json={"email": "user@example.com", "password": "secret123"},
            headers=self.auth_headers,
        )
        self.assertEqual(create_response.status_code, 201)

        list_response = self.client.get("/get_user", headers=self.auth_headers)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()), 2)

        get_response = self.client.get(
            "/get_user/",
            params={"email": "user@example.com"},
            headers=self.auth_headers,
        )
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["email"], "user@example.com")


if __name__ == "__main__":
    unittest.main()
