from typing import Literal

import pytest

from tripplus.awardplus import RedemptionRequest


@pytest.mark.parametrize("ori", ["TPE"])
@pytest.mark.parametrize("dst", ["KIX"])
@pytest.mark.parametrize("cabin", ["y"])
@pytest.mark.parametrize("type", ["rt"])
def test_redemption_request(ori: str, dst: str, cabin: Literal["y", "c", "f"], type: Literal["ow", "rt"]) -> None:
    req = RedemptionRequest(ori=ori, dst=dst, cabin=cabin, type=type)
    resp = req.do()
    assert len(resp.items) > 0
    for item in resp.items:
        assert item.origin == ori
        assert item.destination == dst
        assert item.cabin == cabin
        assert item.type == type
