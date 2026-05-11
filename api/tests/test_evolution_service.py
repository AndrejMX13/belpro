import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services.evolution import EvolutionClient

CLIENT = EvolutionClient(
    base_url="http://localhost:8180",
    api_key="testkey",
    instance_name="belpro",
)

OPEN_RESPONSE = [
    {
        "instance": {
            "instanceName": "belpro",
            "status": "open",
            "owner": "38640123456@s.whatsapp.net",
        }
    }
]
CLOSE_RESPONSE = [
    {"instance": {"instanceName": "belpro", "status": "close"}}
]
LID_RESPONSE = [
    {
        "instance": {
            "instanceName": "belpro",
            "status": "open",
            "owner": "245616546422929@lid",
        }
    }
]
EMPTY_RESPONSE: list = []


def _make_mock_http(json_data: list) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status = MagicMock()
    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=False)
    mock_http.get = AsyncMock(return_value=mock_resp)
    return mock_http


@pytest.mark.asyncio
async def test_connected_returns_normalized_phone_and_open_state():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(OPEN_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone == "38640123456"
    assert state == "open"


@pytest.mark.asyncio
async def test_disconnected_returns_none_and_close_state():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(CLOSE_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "close"


@pytest.mark.asyncio
async def test_network_error_returns_unreachable():
    with patch("httpx.AsyncClient", side_effect=Exception("connection refused")):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "unreachable"


@pytest.mark.asyncio
async def test_lid_jid_returns_lid_unsupported():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(LID_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "lid_unsupported"


@pytest.mark.asyncio
async def test_instance_not_in_response_returns_close():
    with patch("httpx.AsyncClient", return_value=_make_mock_http(EMPTY_RESPONSE)):
        phone, state = await CLIENT.get_connected_phone()
    assert phone is None
    assert state == "close"
