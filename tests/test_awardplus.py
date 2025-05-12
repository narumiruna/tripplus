from typing import Any
from typing import Literal
from unittest.mock import patch

import pytest

from tripplus.awardplus import RedemptionRequest


@pytest.mark.parametrize("ori", ["TPE"])
@pytest.mark.parametrize("dst", ["KIX"])
@pytest.mark.parametrize("cabin", ["y"])
@pytest.mark.parametrize("type", ["rt"])
def test_redemption_request(ori: str, dst: str, cabin: Literal["y", "c", "f"], type: Literal["ow", "rt"]) -> None:
    mock_json = {
        "meta": {"count": 1, "referral_products": []},
        "items": [
            {
                "origin": ori,
                "destination": dst,
                "type": type,
                "cabin": cabin,
                "bookmark_id": None,
                "bookmarked": False,
                "route_stop_desc": [],
                "tags": [],
                "resources": {"type": "test", "items": []},
                "miles": 10000,
                "miles_desc": "10,000",
                "program_code": "TEST",
                "program_name": "Test Program",
                "program_link": None,
                "program_link_desc": None,
                "program_tel": None,
                "program_email": None,
                "program_expiration_desc": None,
                "operating_program_code": None,
                "operating_program_name": "",
                "level": "basic",
                "systems": [],
                "routes": [],
            }
        ],
    }

    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> dict[str, Any]:
            return mock_json

    with patch("tripplus.awardplus.cloudscraper.create_scraper") as mock_create_scraper:
        mock_scraper = mock_create_scraper.return_value
        mock_scraper.get.return_value = MockResponse()
        req = RedemptionRequest(ori=ori, dst=dst, cabin=cabin, type=type)
        resp = req.do()
        assert len(resp.items) > 0
        for item in resp.items:
            assert item.origin == ori
            assert item.destination == dst
            assert item.cabin == cabin
            assert item.type == type
