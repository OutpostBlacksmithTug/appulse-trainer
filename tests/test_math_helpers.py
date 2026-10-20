from appulse.utils.math_helpers import world_to_screen

def test_behind_camera_returns_false():
    _, _, visible = world_to_screen(0, 0, -100, 0, 0, 0, 0, 0, 90, 1920, 1080)
    assert visible is False

def test_center_projection():
    sx, sy, visible = world_to_screen(0, 0, 10, 0, 0, 0, 0, 0, 90, 1920, 1080)
    assert visible is True
    assert 900 < sx < 1020
    assert 500 < sy < 580