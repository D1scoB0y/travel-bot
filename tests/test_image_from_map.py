import folium

import bot.utils as _utils


def test_image_from_map():
    test_map = folium.Map()

    map_image_bytes = _utils.map_image(test_map)
    
    assert isinstance(map_image_bytes, bytes)
