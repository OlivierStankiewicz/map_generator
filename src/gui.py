from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QSpinBox,
    QGroupBox,
    QFormLayout,
    QComboBox,
)
from PySide6.QtGui import QImage, QPixmap
import sys
import os
import json
import subprocess
import shutil
import traceback

# Ensure the `src` directory is on sys.path so imports work whether the script is
# run from project root (`python src/gui.py`) or from inside `src`.
project_src = os.path.abspath(os.path.dirname(__file__))
if project_src not in sys.path:
    sys.path.insert(0, project_src)

generate_voronoi_map = None
try:
    from generation.map_gen.map_gen import generate_voronoi_map
except Exception:
    try:
        from src.generation.map_gen.map_gen import generate_voronoi_map
    except Exception:
        generate_voronoi_map = None

try:
    from classes.tile.Tile import TerrainType
except Exception:
    try:
        from src.classes.tile.Tile import TerrainType
    except Exception:
        TerrainType = None


def filter_none_values(obj):
    """Recursively remove keys with None values from dictionaries"""
    if isinstance(obj, dict):
        return {k: filter_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [filter_none_values(item) for item in obj if item is not None]
    else:
        return obj


class GeneratorWorker(QtCore.QObject):
    finished = QtCore.Signal(object)
    error = QtCore.Signal(str)
    status = QtCore.Signal(str)

    @QtCore.Slot()
    def run(self):
        try:
            self.status.emit("Starting generation...")
            if generate_voronoi_map is None:
                raise ImportError("Map generator function not available (import failed).")
            map_obj = generate_voronoi_map()
            self.finished.emit(map_obj)
        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(f"{e}\n{tb}")


class MapGeneratorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Generator GUI")
        self.resize(540, 160)

        # Widgets
        self.folder_label = QLabel("Save folder:")
        self.folder_path_edit = QLineEdit()
        self.folder_browse_btn = QPushButton("Browse")

        self.filename_label = QLabel("File name (without extension):")
        self.filename_edit = QLineEdit()

        # Map size selector
        self.size_label = QLabel("Map size:")
        self.size_combo = QComboBox()
        self.size_combo.addItems(["36x36", "72x72", "108x108", "144x144"])
        # default to 72x72
        self.size_combo.setCurrentText("72x72")

        # Terrain value controls (match main.py defaults)
        self.terrain_group = QGroupBox("Terrain values")
        terrain_form = QFormLayout()
        self.spin_water = QSpinBox(); self.spin_water.setRange(0, 10); self.spin_water.setValue(2)
        self.spin_grass = QSpinBox(); self.spin_grass.setRange(0, 10); self.spin_grass.setValue(3)
        self.spin_snow = QSpinBox(); self.spin_snow.setRange(0, 10); self.spin_snow.setValue(2)
        self.spin_swamp = QSpinBox(); self.spin_swamp.setRange(0, 10); self.spin_swamp.setValue(3)
        self.spin_rough = QSpinBox(); self.spin_rough.setRange(0, 10); self.spin_rough.setValue(1)
        self.spin_lava = QSpinBox(); self.spin_lava.setRange(0, 10); self.spin_lava.setValue(1)
        self.spin_sand = QSpinBox(); self.spin_sand.setRange(0, 10); self.spin_sand.setValue(1)
        self.spin_dirt = QSpinBox(); self.spin_dirt.setRange(0, 10); self.spin_dirt.setValue(3)
        self.spin_rock = QSpinBox(); self.spin_rock.setRange(0, 10); self.spin_rock.setValue(2)
        terrain_form.addRow("WATER:", self.spin_water)
        terrain_form.addRow("GRASS:", self.spin_grass)
        terrain_form.addRow("SNOW:", self.spin_snow)
        terrain_form.addRow("SWAMP:", self.spin_swamp)
        terrain_form.addRow("ROUGH:", self.spin_rough)
        terrain_form.addRow("LAVA:", self.spin_lava)
        terrain_form.addRow("SAND:", self.spin_sand)
        terrain_form.addRow("DIRT:", self.spin_dirt)
        terrain_form.addRow("ROCK:", self.spin_rock)
        self.terrain_group.setLayout(terrain_form)

        self.generate_btn = QPushButton("Generate map")
        self.status_label = QLabel("")

        # Layout
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path_edit)
        folder_layout.addWidget(self.folder_browse_btn)

        # Build left column of controls wrapped in group boxes
        left_col = QVBoxLayout()

        # Save folder group
        folder_group = QGroupBox("Save folder")
        fg_layout = QHBoxLayout()
        fg_layout.addWidget(self.folder_path_edit)
        fg_layout.addWidget(self.folder_browse_btn)
        folder_group.setLayout(fg_layout)
        left_col.addWidget(folder_group)

        # File group (filename + size)
        file_group = QGroupBox("File")
        file_layout = QVBoxLayout()
        file_layout.addWidget(self.filename_label)
        file_layout.addWidget(self.filename_edit)
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_combo)
        file_layout.addLayout(size_layout)
        file_group.setLayout(file_layout)
        left_col.addWidget(file_group)

        # Terrain group (already a QGroupBox)
        left_col.addWidget(self.terrain_group)

        # Actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout()
        actions_layout.addWidget(self.generate_btn)
        actions_group.setLayout(actions_layout)
        left_col.addWidget(actions_group)

        # Right column: preview (center vertically, title directly above the preview)
        right_col = QVBoxLayout()
        right_col.setSpacing(6)
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.addStretch(1)

        inner_preview = QVBoxLayout()
        inner_preview.setSpacing(4)
        self.preview_title = QLabel("Podgląd wygenerowanej mapy")
        self.preview_title.setAlignment(QtCore.Qt.AlignHCenter)
        inner_preview.addWidget(self.preview_title, alignment=QtCore.Qt.AlignHCenter)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(300, 300)
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        # placeholder text until a map is generated
        self.preview_label.setText("tu będzie podgląd wygenerowanej mapy")
        self.preview_label.setStyleSheet("color: #666; border: 1px solid #ccc; padding: 6px;")
        inner_preview.addWidget(self.preview_label, alignment=QtCore.Qt.AlignHCenter)

        right_col.addLayout(inner_preview)
        right_col.addStretch(1)

        # Combine into main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_col)
        main_layout.addLayout(right_col)

        # Overall wrapper to include status at bottom
        wrapper = QVBoxLayout()
        wrapper.addLayout(main_layout)
        wrapper.addWidget(self.status_label)

        self.setLayout(wrapper)

        # Signals
        self.folder_browse_btn.clicked.connect(self.browse_folder)
        self.generate_btn.clicked.connect(self.on_generate)

        # Thread holder
        self._worker_thread = None

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select a folder to save the file")
        if folder:
            self.folder_path_edit.setText(folder)

    def on_generate(self):
        folder = self.folder_path_edit.text().strip()
        filename = self.filename_edit.text().strip()

        if not folder:
            QMessageBox.warning(self, "Missing folder", "Please select a folder to save the files.")
            return
        if not filename:
            QMessageBox.warning(self, "Missing filename", "Please enter a file name.")
            return

        # Disable UI while working
        self.generate_btn.setEnabled(False)

        # Follow same steps, variable names and order as in main.py
        self.status_label.setText("Generating map representation...")
        QApplication.processEvents()

        if generate_voronoi_map is None:
            QMessageBox.critical(self, "Import error", "Could not import map generator function. Run from project root or adjust imports.")
            self.status_label.setText("Failed: generator not available")
            self.generate_btn.setEnabled(True)
            return

        try:
            # terrain_values as in main.py (take values from spinboxes)
            if TerrainType is None:
                raise ImportError("TerrainType enum not available (failed to import classes.tile.Tile).")

            terrain_values = {
                TerrainType.WATER: self.spin_water.value(),
                TerrainType.GRASS: self.spin_grass.value(),
                TerrainType.SNOW: self.spin_snow.value(),
                TerrainType.SWAMP: self.spin_swamp.value(),
                TerrainType.ROUGH: self.spin_rough.value(),
                TerrainType.LAVA: self.spin_lava.value(),
                TerrainType.SAND: self.spin_sand.value(),
                TerrainType.DIRT: self.spin_dirt.value(),
                TerrainType.ROCK: self.spin_rock.value(),
            }

            # parse selected size (e.g. "72x72")
            size_text = self.size_combo.currentText()
            try:
                w_str, h_str = size_text.split('x')
                width = int(w_str)
                height = int(h_str)
            except Exception:
                width = 72
                height = 72

            map = generate_voronoi_map(terrain_values, width=width, height=height)
            # store last generated map and size for preview
            try:
                self._last_map = map
                self._last_size = (width, height)
                # build and display preview image
                tile_px = max(1, 300 // max(width, height))
                qimg = self._build_preview_qimage(self._last_map, width, height, tile_px)
                pix = QPixmap.fromImage(qimg)
                self.preview_label.setPixmap(pix.scaled(self.preview_label.size(), QtCore.Qt.KeepAspectRatio))
                # clear placeholder styling
                self.preview_label.setStyleSheet("")
                self.preview_label.setText("")
            except Exception:
                self._last_map = None
                self._last_size = None
        except Exception as e:
            QMessageBox.critical(self, "Generation error", f"Map generation failed: {e}")
            self.status_label.setText("Failed: generation error")
            self.generate_btn.setEnabled(True)
            return

        try:
            map_dict = filter_none_values(map.to_dict())
            json_map_representation = json.dumps(map_dict, indent=2)
            self.status_label.setText("Map representation generated successfully")
            QApplication.processEvents()
        except Exception as e:
            QMessageBox.critical(self, "Serialize error", f"Failed to serialize map: {e}")
            self.status_label.setText("Failed: serialize error")
            self.generate_btn.setEnabled(True)
            return

        json_file_path = os.path.join(folder, f"{filename}.json")
        h3m_file_path = os.path.join(folder, f"{filename}.h3m")

        try:
            self.status_label.setText(f"Saving map representation to: {json_file_path}")
            QApplication.processEvents()
            with open(json_file_path, 'w', encoding='utf-8') as f:
                f.write(json_map_representation)
        except Exception as e:
            QMessageBox.critical(self, "File error", f"Failed to write JSON file: {e}")
            self.status_label.setText("Failed: file write error")
            self.generate_btn.setEnabled(True)
            return

        # Conversion using os.system to match main.py
        try:
            self.status_label.setText("Converting JSON to h3m...")
            QApplication.processEvents()
            ret = os.system(f'h3mtxt.exe "{json_file_path}" "{h3m_file_path}"')
            if ret == 0:
                QMessageBox.information(self, "Success", f"New file created at: {h3m_file_path}")
                self.status_label.setText("Done")
            else:
                QMessageBox.information(self, "Conversion", f"Conversion finished with code {ret}. JSON saved to {json_file_path}")
                self.status_label.setText("Saved JSON (converter returned non-zero)")
        except Exception as e:
            QMessageBox.warning(self, "Conversion error", f"Failed to convert file: {e}")
            self.status_label.setText("Converter failed")

        self.generate_btn.setEnabled(True)

    def _set_status_text(self, text):
        self.status_label.setText(text)
        QApplication.processEvents()

    def _on_worker_error(self, msg):
        QMessageBox.critical(self, "Generation error", f"Map generation failed:\n{msg}")
        self.status_label.setText("Failed: generation error")
        self.generate_btn.setEnabled(True)
        # clean up thread reference
        self._worker_thread = None

    def on_save_preview(self):
        # Save a simple BMP preview of the last generated map (surface layer)
        if not hasattr(self, '_last_map') or self._last_map is None:
            QMessageBox.warning(self, "No map", "No generated map available. Generate a map first.")
            return

        default_path = os.path.join(os.getcwd(), "map_preview.bmp")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save preview BMP", default_path, "Bitmap Files (*.bmp)")
        if not file_path:
            return

        try:
            width, height = self._last_size
            tile_px = max(1, 600 // max(width, height))
            self._write_preview_bmp(file_path, self._last_map, width, height, tile_px)
            QMessageBox.information(self, "Saved", f"Preview saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Preview error", f"Failed to save preview: {e}")

    def _write_preview_bmp(self, path: str, map_obj, width: int, height: int, tile_px: int = 6):
        # color map for terrain types (by TerrainType.value)
        color_map = {
            # DIRT, SAND, GRASS, SNOW, SWAMP, ROUGH, SUBTERRANEAN, LAVA, WATER, ROCK
            0: (153, 102, 51),   # DIRT
            1: (210, 180, 140),  # SAND
            2: (34, 139, 34),    # GRASS
            3: (240, 240, 240),  # SNOW
            4: (85, 107, 47),    # SWAMP
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

    def _build_preview_qimage(self, map_obj, width: int, height: int, tile_px: int = 6) -> QImage:
        # color map for terrain types (by TerrainType.value)
        color_map = {
            0: (153, 102, 51),   # DIRT
            1: (210, 180, 140),  # SAND
            2: (34, 139, 34),    # GRASS
            3: (240, 240, 240),  # SNOW
            4: (85, 107, 47),    # SWAMP
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

        # QImage expects bytes in top-down order for Format_RGB888
        return QImage(bytes(data), img_w, img_h, QImage.Format_RGB888)

    def _on_worker_finished(self, map_obj, folder, filename):
        try:
            self.status_label.setText("Serializing map...")
            QApplication.processEvents()

            if hasattr(map_obj, 'to_dict'):
                data = map_obj.to_dict()
            else:
                data = map_obj

            json_map = json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Serialize error", f"Failed to serialize map: {e}")
            self.status_label.setText("Failed: serialize error")
            self.generate_btn.setEnabled(True)
            self._worker_thread = None
            return

        json_file_path = os.path.join(folder, f"{filename}.json")
        h3m_file_path = os.path.join(folder, f"{filename}.h3m")

        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                f.write(json_map)
        except Exception as e:
            QMessageBox.critical(self, "File error", f"Failed to write JSON file: {e}")
            self.status_label.setText("Failed: file write error")
            self.generate_btn.setEnabled(True)
            self._worker_thread = None
            return

        # Try running the external converter if available.
        converter = shutil.which('h3mtxt.exe')
        if not converter:
            cwd_candidate = os.path.join(os.getcwd(), 'h3mtxt.exe')
            if os.path.exists(cwd_candidate):
                converter = cwd_candidate
        if not converter:
            project_root_candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'h3mtxt.exe'))
            if os.path.exists(project_root_candidate):
                converter = project_root_candidate

        if converter and os.path.exists(converter):
            try:
                self.status_label.setText("Running converter...")
                QApplication.processEvents()
                converter_dir = os.path.dirname(converter) or os.getcwd()
                result = subprocess.run([converter, json_file_path, h3m_file_path], cwd=converter_dir, capture_output=True, text=True)
                if result.returncode != 0:
                    msg = f'Converter returned code {result.returncode}\n\nstdout:\n{result.stdout}\n\nstderr:\n{result.stderr}'
                    QMessageBox.warning(self, "Converter returned non-zero", msg)
                    self.status_label.setText("Converter error")
                else:
                    QMessageBox.information(self, "Success", f"Map saved to {h3m_file_path}")
                    self.status_label.setText("Done")
            except Exception as e:
                QMessageBox.warning(self, "Converter error", f"Failed to run converter: {e}")
                self.status_label.setText("Converter failed")
        else:
            QMessageBox.information(self, "Saved JSON", f"JSON saved to {json_file_path}. Converter not found; .h3m not created.")
            self.status_label.setText("Saved JSON (no converter)")

        self.generate_btn.setEnabled(True)
        self._worker_thread = None


def main():
    app = QApplication(sys.argv)
    win = MapGeneratorGUI()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
