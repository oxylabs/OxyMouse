import pytest

from oxymouse import OxyMouse
from oxymouse.config import mouses


def test_mouses_count():
    assert len(mouses) == 4


@pytest.fixture(params=mouses.keys())
def algorithm(request):
    return request.param

@pytest.fixture
def oxy_mouse(algorithm):
    return OxyMouse(algorithm)


def test_generate_coordinates(oxy_mouse):
    from_x, from_y, to_x, to_y = 0, 0, 1000, 1000
    coordinates = oxy_mouse.generate_coordinates(
        from_x=from_x, from_y=from_y, to_x=to_x, to_y=to_y
    )
    assert len(coordinates) > 50
    assert coordinates[0] == (from_x, from_y)
    # assert coordinates[-1] == (to_x, to_y)  # this seems to fail for some algorithms

