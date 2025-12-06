from PySide6.QtGui import QImage, QPainter, QColor
from PySide6 import QtCore


def write_preview_bmp(path: str, map_obj, width: int, height: int, tile_px: int = 6, neutral_towns=None):
    # color map for terrain types (by TerrainType.value)
    color_map = {
        # DIRT, SAND, GRASS, SNOW, SWAMP, ROUGH, SUBTERRANEAN, LAVA, WATER, ROCK
        0: (153, 102, 51),   # DIRT
        1: (201, 152, 88),  # SAND
        2: (12, 186, 12),    # GRASS
        3: (240, 240, 240),  # SNOW
        4: (55, 69, 31),    # SWAMP
        5: (128, 128, 128),  # ROUGH
        6: (0, 0, 0),        # SUBTERRANEAN
        7: (64, 64, 64),      # LAVA (dark gray)
        8: (28, 107, 160),    # WATER
        9: (0, 0, 0),         # ROCK (black)
    }

    # build pixel rows (top-down)
    img_w = width * tile_px
    img_h = height * tile_px
    rows = []
    # surface tiles are the first width*height tiles in map_obj.tiles
    tiles = map_obj.tiles[:width * height]
    for y in range(height):
        # build one row of pixels (tile_px height)
        row_pixels = []
        for x in range(width):
            tile = tiles[y * width + x]
            # tile.terrain_type is an int
            t = tile.terrain_type if hasattr(tile, 'terrain_type') else (tile.get('terrain_type') if isinstance(tile, dict) else 0)
            rgb = color_map.get(t, (192, 192, 192))
            # append tile_px copies horizontally
            row_pixels.extend([rgb] * tile_px)
        # duplicate this row tile_px times vertically
        for _ in range(tile_px):
            rows.append(row_pixels[:])

    # Overlay player main towns (if present) as colored tiles
    try:
        player_colors = [
            (255, 0, 0),    # red
            (0, 0, 255),    # blue
            (210, 180, 140),# tan
            (0, 128, 0),    # green
            (255, 165, 0),  # orange
            (128, 0, 128),  # purple
            (0, 128, 128),  # teal
            (255, 192, 203) # pink
        ]
        for p_idx, p in enumerate(getattr(map_obj, 'players', []) or []):
            mt = getattr(p, 'main_town', None)
            if not mt:
                continue
            # recover grid city coordinates: generator stored main_town.x = final_x - 2
            try:
                city_x = int(mt.x + 2)
                city_y = int(mt.y)
            except Exception:
                continue

            tile_coords = [
                (city_x - 1, city_y),
                (city_x, city_y),
                (city_x + 1, city_y),
                (city_x, city_y - 1),
            ]

            color = player_colors[p_idx] if p_idx < len(player_colors) else (0, 0, 0)

            # paint whole tiles (tile_px x tile_px) in the rows array
            for tx, ty in tile_coords:
                if tx < 0 or tx >= width or ty < 0 or ty >= height:
                    continue
                # pixel ranges for this tile
                px0 = tx * tile_px
                py0 = ty * tile_px
                px1 = px0 + tile_px - 1
                py1 = py0 + tile_px - 1
                for ry in range(py0, py1 + 1):
                    if ry < 0 or ry >= img_h:
                        continue
                    row = rows[ry]
                    for rx in range(px0, px1 + 1):
                        if rx < 0 or rx >= img_w:
                            continue
                        row[rx] = color
    except Exception:
        # don't fail the whole save if overlay fails
        pass

    # Overlay neutral towns (gray) if provided
    try:
        towns = neutral_towns or []
        if towns:
            gray = (191, 191, 191)
            for town in towns:
                try:
                    if isinstance(town, (list, tuple)):
                        tx = int(town[0])
                        ty = int(town[1])
                    else:
                        # object-like
                        tx = int(getattr(town, 'x', 0))
                        ty = int(getattr(town, 'y', 0))
                except Exception:
                    continue

                tile_coords = [
                    (tx - 1, ty),
                    (tx, ty),
                    (tx + 1, ty),
                    (tx, ty - 1),
                ]

                for txx, tyy in tile_coords:
                    if txx < 0 or txx >= width or tyy < 0 or tyy >= height:
                        continue
                    px0 = txx * tile_px
                    py0 = tyy * tile_px
                    px1 = px0 + tile_px - 1
                    py1 = py0 + tile_px - 1
                    for ry in range(py0, py1 + 1):
                        if ry < 0 or ry >= img_h:
                            continue
                        row = rows[ry]
                        for rx in range(px0, px1 + 1):
                            if rx < 0 or rx >= img_w:
                                continue
                            row[rx] = gray
    except Exception:
        pass

    # write 24-bit BMP
    import struct

    row_size = img_w * 3
    padding = (4 - (row_size % 4)) % 4
    bmp_data_size = (row_size + padding) * img_h
    file_size = 14 + 40 + bmp_data_size

    with open(path, 'wb') as f:
        # BITMAPFILEHEADER
        f.write(b'BM')
        f.write(struct.pack('<I', file_size))
        f.write(struct.pack('<H', 0))
        f.write(struct.pack('<H', 0))
        f.write(struct.pack('<I', 14 + 40))

        # BITMAPINFOHEADER
        f.write(struct.pack('<I', 40))
        f.write(struct.pack('<i', img_w))
        f.write(struct.pack('<i', img_h))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', 24))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', bmp_data_size))
        f.write(struct.pack('<i', 2835))
        f.write(struct.pack('<i', 2835))
        f.write(struct.pack('<I', 0))
        f.write(struct.pack('<I', 0))

        # pixel data (bottom-up)
        for row in reversed(rows):
            for (r, g, b) in row:
                # BMP stores in BGR order
                f.write(struct.pack('B', b))
                f.write(struct.pack('B', g))
                f.write(struct.pack('B', r))
            # padding
            for _ in range(padding):
                f.write(b'\x00')


def build_preview_qimage(map_obj, width: int, height: int, tile_px: int = 6, neutral_towns=None) -> QImage:
    # color map for terrain types (by TerrainType.value)
    color_map = {
        0: (153, 102, 51),   # DIRT
        1: (201, 152, 88),  # SAND
        2: (12, 186, 12),    # GRASS
        3: (240, 240, 240),  # SNOW
        4: (55, 69, 31),    # SWAMP
        5: (128, 128, 128),  # ROUGH
        6: (0, 0, 0),        # SUBTERRANEAN
        7: (64, 64, 64),     # LAVA (dark gray)
        8: (28, 107, 160),   # WATER
        9: (0, 0, 0),        # ROCK (black)
    }

    img_w = width * tile_px
    img_h = height * tile_px
    data = bytearray(img_w * img_h * 3)
    tiles = map_obj.tiles[:width * height]
    idx = 0
    for y in range(height):
        for ty in range(tile_px):
            for x in range(width):
                tile = tiles[y * width + x]
                t = tile.terrain_type if hasattr(tile, 'terrain_type') else (tile.get('terrain_type') if isinstance(tile, dict) else 0)
                r, g, b = color_map.get(t, (192, 192, 192))
                for tx in range(tile_px):
                    data[idx] = r
                    data[idx + 1] = g
                    data[idx + 2] = b
                    idx += 3

    qimg = QImage(bytes(data), img_w, img_h, QImage.Format_RGB888)

    # Paint player main towns on top of generated image
    try:
        painter = QPainter(qimg)
        painter.setRenderHint(QPainter.Antialiasing)
        player_colors = [
            QColor(255, 0, 0),    # red
            QColor(0, 0, 255),    # blue
            QColor(210, 180, 140),# tan
            QColor(0, 128, 0),    # green
            QColor(255, 165, 0),  # orange
            QColor(128, 0, 128),  # purple
            QColor(0, 128, 128),  # teal
            QColor(255, 192, 203) # pink
        ]
        for p_idx, p in enumerate(getattr(map_obj, 'players', []) or []):
            mt = getattr(p, 'main_town', None)
            if not mt:
                continue
            try:
                city_x = int(mt.x + 2)
                city_y = int(mt.y)
            except Exception:
                continue

            tile_coords = [
                (city_x - 1, city_y),
                (city_x, city_y),
                (city_x + 1, city_y),
                (city_x, city_y - 1),
            ]

            color = player_colors[p_idx] if p_idx < len(player_colors) else QColor(0, 0, 0)
            painter.setPen(QtCore.Qt.NoPen)
            for tx, ty in tile_coords:
                if tx < 0 or tx >= width or ty < 0 or ty >= height:
                    continue
                x_px = int(tx * tile_px)
                y_px = int(ty * tile_px)
                rect = QtCore.QRect(x_px, y_px, int(tile_px), int(tile_px))
                painter.fillRect(rect, color)
        painter.end()
    except Exception:
        pass

    if neutral_towns:
        try:
            painter = QPainter(qimg)
            painter.setRenderHint(QPainter.Antialiasing)
            gray_color = QColor(191, 191, 191)
            for town in neutral_towns:
                try:
                    tx = int(town[0])
                    ty = int(town[1])
                except Exception:
                    continue

                tile_coords = [
                    (tx - 1, ty),
                    (tx, ty),
                    (tx + 1, ty),
                    (tx, ty - 1),
                ]

                painter.setPen(QtCore.Qt.NoPen)
                for txx, tyy in tile_coords:
                    if txx < 0 or txx >= width or tyy < 0 or tyy >= height:
                        continue
                    x_px = int(txx * tile_px)
                    y_px = int(tyy * tile_px)
                    rect = QtCore.QRect(x_px, y_px, int(tile_px), int(tile_px))
                    painter.fillRect(rect, gray_color)
            painter.end()
        except Exception:
            pass

    return qimg