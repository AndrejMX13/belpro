import base64
from httpx import AsyncClient


async def test_get_manager_returns_profile(client: AsyncClient, auth: dict) -> None:
    r = await client.get("/api/managers/me", headers=auth)
    assert r.status_code == 200
    data = r.json()
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Manager"
    assert data["email"] == "test@belpro.si"


async def test_create_manager_returns_409_when_already_configured(
    client: AsyncClient, auth: dict
) -> None:
    payload = {
        "first_name": "Nova",
        "last_name": "Upravljalka",
        "phone": "+38641999999",
        "email": "nova@belpro.si",
        "ngo_name": "Nova NGO",
        "ngo_street": "Nova 1",
        "ngo_postal_code": "2000",
        "ngo_city": "Maribor",
    }
    r = await client.post("/api/managers", json=payload, headers=auth)
    assert r.status_code == 409


async def test_auth_wrong_password_returns_401(client: AsyncClient) -> None:
    bad = base64.b64encode(b"manager:wrongpassword").decode()
    r = await client.get("/api/managers/me", headers={"Authorization": f"Basic {bad}"})
    assert r.status_code == 401


async def test_auth_missing_credentials_returns_401(client: AsyncClient) -> None:
    r = await client.get("/api/managers/me")
    assert r.status_code == 401
