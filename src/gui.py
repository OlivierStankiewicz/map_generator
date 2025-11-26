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
    QPlainTextEdit,
    QSizePolicy,
)
from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath, QPen, QColor, QFontMetrics
import sys
import os
import json
import subprocess
import shutil
import traceback
from datetime import datetime

# Ensure the `src` directory is on sys.path so imports work whether the script is
# run from project root (`python src/gui.py`) or from inside `src`.
# project_src = os.path.abspath(os.path.dirname(__file__))
# if project_src not in sys.path:
#     sys.path.insert(0, project_src)

# generate_voronoi_map = None
# try:
#     from generation.map_gen.map_gen import generate_voronoi_map
# except Exception:
#     try:
#         from src.generation.map_gen.map_gen import generate_voronoi_map
#     except Exception:
#         generate_voronoi_map = None

# try:
#     from classes.tile.Tile import TerrainType
# except Exception:
#     try:
#         from src.classes.tile.Tile import TerrainType
#     except Exception:
#         TerrainType = None

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from generation.map_gen.map_gen import generate_voronoi_map
from classes.tile.Tile import TerrainType
from generation.additional_info_gen.teams_gen import TeamsParams
from generation.additional_info_gen.victory_condition_gen import VictoryConditionParams
from generation.additional_info_gen.loss_condition_gen import LossConditionParams
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.ArtifactType import ArtifactType
from classes.Enums.CreatureType import CreatureType
from classes.Enums.ResourceType import ResourceType
from classes.Enums.LossConditions import LossConditions

def filter_none_values(obj):
    """Recursively remove keys with None values from dictionaries"""
    if isinstance(obj, dict):
        return {k: filter_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [filter_none_values(item) for item in obj if item is not None]
    else:
        return obj


class LimitedPlainTextEdit(QPlainTextEdit):
    """QPlainTextEdit that enforces a maximum character length on insert and paste.

    This prevents typing or pasting more than `max_length` characters.
    """
    def __init__(self, max_length: int = 300, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = int(max_length)

    def insertPlainText(self, text: str) -> None:
        cur = self.toPlainText()
        # account for selected text which will be replaced
        cursor = self.textCursor()
        sel_len = len(cursor.selectedText()) if cursor is not None else 0
        allowed = self.max_length - (len(cur) - sel_len)
        if allowed <= 0:
            return
        if len(text) > allowed:
            text = text[:allowed]
        super().insertPlainText(text)

    def insertFromMimeData(self, source) -> None:
        # handle paste operations
        try:
            text = source.text()
        except Exception:
            text = ''
        cur = self.toPlainText()
        cursor = self.textCursor()
        sel_len = len(cursor.selectedText()) if cursor is not None else 0
        allowed = self.max_length - (len(cur) - sel_len)
        if allowed <= 0:
            return
        if len(text) > allowed:
            text = text[:allowed]
        md = QtCore.QMimeData()
        md.setText(text)
        super().insertFromMimeData(md)

    def keyPressEvent(self, event):
        # Allow navigation and editing keys (so backspace/delete still work)
        key = event.key()
        navigation_keys = {
            QtCore.Qt.Key_Backspace,
            QtCore.Qt.Key_Delete,
            QtCore.Qt.Key_Left,
            QtCore.Qt.Key_Right,
            QtCore.Qt.Key_Home,
            QtCore.Qt.Key_End,
            QtCore.Qt.Key_Up,
            QtCore.Qt.Key_Down,
            QtCore.Qt.Key_PageUp,
            QtCore.Qt.Key_PageDown,
        }
        if key in navigation_keys:
            return super().keyPressEvent(event)

        # Allow common shortcuts (Ctrl+C/X/V/A/Z/Y etc.) to be handled normally
        if event.modifiers() & (QtCore.Qt.ControlModifier | QtCore.Qt.AltModifier):
            return super().keyPressEvent(event)

        # For printable input, enforce the remaining allowed characters (accounting for selection)
        text = event.text()
        if not text:
            return super().keyPressEvent(event)

        cur = self.toPlainText()
        cursor = self.textCursor()
        sel_len = len(cursor.selectedText()) if cursor is not None else 0
        allowed = self.max_length - (len(cur) - sel_len)
        if allowed <= 0:
            # nothing allowed — ignore printable input
            return
        if len(text) > allowed:
            # insert truncated text
            self.insertPlainText(text[:allowed])
            return

        return super().keyPressEvent(event)


class OutlinedLabel(QtWidgets.QLabel):
    """QLabel that draws a hard outline around the text using QPainterPath.

    This produces a solid sharp border (miter join) around the text rather
    than a soft blurred shadow.
    """
    def __init__(self, *args, outline_width: int = 2, outline_color: str = 'black', **kwargs):
        super().__init__(*args, **kwargs)
        self._outline_width = int(outline_width)
        self._outline_color = QColor(outline_color)

    def paintEvent(self, event):
        text = self.text() or ''
        if not text:
            return super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        font = self.font()
        fm = QFontMetrics(font)
        rect = self.rect()

        # Compute coordinates for left-aligned, vertically centered text
        tw = fm.horizontalAdvance(text)
        th = fm.height()
        x = 0
        y = int((rect.height() + fm.ascent() - fm.descent()) / 2)

        path = QPainterPath()
        path.addText(x, y, font, text)

        pen = QPen(self._outline_color)
        pen.setWidth(self._outline_width)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        painter.setPen(pen)
        painter.drawPath(path)

        # draw filled text on top using the widget's palette/stylesheet color
        # Use drawText to respect alignment and eliding behavior
        painter.setPen(self.palette().color(self.foregroundRole()))
        painter.drawText(rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, text)

        painter.end()


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
        self.resize(820, 300)

        # Widgets
        self.folder_label = QLabel("Save folder:")
        self.folder_path_edit = QLineEdit()
        self.folder_browse_btn = QPushButton("Browse")

        self.filename_label = QLabel("File name (without extension):")
        self.filename_edit = QLineEdit()

        # Map metadata: name and description
        self.map_name_label = QLabel("Map name:")
        self.map_name_edit = QLineEdit()
        # limit to 30 characters
        self.map_name_edit.setMaxLength(30)
        # default name with current date/time
        now = datetime.now()
        default_name = f"My Map {now.day}/{now.month}/{now.year} {now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        self.map_name_edit.setText(default_name)
        # default filename in snake_case with zero-padded numbers
        filename_default = f"my_map_{now.day:02d}_{now.month:02d}_{now.year}_{now.hour:02d}_{now.minute:02d}_{now.second:02d}"
        self.filename_edit.setText(filename_default)

        self.map_desc_label = QLabel("Map description:")
        self.map_desc_max = 300
        # use LimitedPlainTextEdit to prevent typing/pasting more than allowed
        self.map_desc_edit = LimitedPlainTextEdit(self.map_desc_max)
        self.map_desc_edit.setFixedHeight(80)
        # default description
        description_default = f"Map generated on {now.day}/{now.month}/{now.year} at {now.hour:02d}:{now.minute:02d}:{now.second:02d}."
        self.map_desc_edit.setPlainText(description_default)

        # Map size selector (fixed preset sizes)
        self.size_label = QLabel("Map size:")
        self.size_combo = QComboBox()
        self.size_combo.addItems(["36x36", "72x72", "108x108", "144x144"])
        # default to 72x72
        self.size_combo.setCurrentText("72x72")

        # Terrain value controls (dynamic list)
        self.terrain_group = QGroupBox("Terrain values")
        self.terrain_layout = QVBoxLayout()

        # Container for rows: each entry will be a QWidget with HBox (label, spinner, remove btn)
        self.terrain_rows_container = QWidget()
        self.terrain_rows_layout = QVBoxLayout()
        self.terrain_rows_layout.setContentsMargins(0, 0, 0, 0)
        self.terrain_rows_container.setLayout(self.terrain_rows_layout)

        # controls for adding terrains
        add_layout = QHBoxLayout()
        self.terrain_add_combo = QComboBox()
        # populate with TerrainType names, but exclude SUBTERRANEAN and ROCK
        for t in TerrainType:
            try:
                if t.name in ("SUBTERRANEAN", "ROCK"):
                    continue
            except Exception:
                pass
            self.terrain_add_combo.addItem(t.name)
        self.terrain_add_btn = QPushButton("Add terrain")
        self.terrain_add_btn.clicked.connect(self._on_add_terrain_clicked)
        add_layout.addWidget(self.terrain_add_combo)
        add_layout.addWidget(self.terrain_add_btn)

        self.terrain_layout.addWidget(self.terrain_rows_container)
        self.terrain_layout.addLayout(add_layout)
        self.terrain_group.setLayout(self.terrain_layout)

        # storage for active terrain widgets: TerrainType -> {'row': QWidget, 'spin': QSpinBox}
        self.terrain_widgets = {}
        # ensure at least one terrain (DIRT) present by default
        try:
            self._add_terrain(TerrainType.DIRT)
        except Exception:
            # fallback: if TerrainType.DIRT not available, add first member
            try:
                first = list(TerrainType)[0]
                self._add_terrain(first)
            except Exception:
                pass

        self.generate_btn = QPushButton("Generate map")
        self.status_label = QLabel("")

        # Layout
        # Build File group (now contains Save folder as a sub-group)
        file_group = QGroupBox("File")
        file_layout = QVBoxLayout()

        # Save folder subgroup inside File
        folder_group = QGroupBox("Save folder")
        fg_layout = QHBoxLayout()
        fg_layout.addWidget(self.folder_path_edit)
        fg_layout.addWidget(self.folder_browse_btn)
        folder_group.setLayout(fg_layout)
        file_layout.addWidget(folder_group)

        # Filename
        file_layout.addWidget(self.filename_label)
        file_layout.addWidget(self.filename_edit)
        # Map info (name + description)
        map_info_group = QGroupBox("Map info")
        map_info_layout = QFormLayout()
        map_info_layout.addRow(self.map_name_label, self.map_name_edit)
        map_info_layout.addRow(self.map_desc_label, self.map_desc_edit)
        map_info_group.setLayout(map_info_layout)
        file_layout.addWidget(map_info_group)
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_combo)
        file_layout.addLayout(size_layout)
        file_group.setLayout(file_layout)

        # Players group: player count (synced with player cities) and neutral cities
        players_group = QGroupBox("Players / Cities")
        pg_layout = QFormLayout()
        self.player_cities_spin = QSpinBox()
        self.player_cities_spin.setRange(0, 8)
        self.player_cities_spin.setValue(5)
        self.players_spin = QSpinBox()
        self.players_spin.setRange(0, 8)
        self.players_spin.setValue(5)
        # sync flag to avoid recursion
        self._syncing_player_counts = False
        def _on_player_cities_changed(val):
            if self._syncing_player_counts:
                return
            self._syncing_player_counts = True
            try:
                self.players_spin.setValue(val)
                # update teams max and rebuild grid (cap at 7 teams)
                self.teams_spin.setMaximum(min(7, max(0, val - 1)))
                self._rebuild_teams_grid_needed = True
            finally:
                self._syncing_player_counts = False

        def _on_players_changed(val):
            if self._syncing_player_counts:
                return
            self._syncing_player_counts = True
            try:
                self.player_cities_spin.setValue(val)
                # update teams max and rebuild grid (cap at 7 teams)
                self.teams_spin.setMaximum(min(7, max(0, val - 1)))
                self._rebuild_teams_grid_needed = True
            finally:
                self._syncing_player_counts = False

        self.player_cities_spin.valueChanged.connect(_on_player_cities_changed)
        self.players_spin.valueChanged.connect(_on_players_changed)

        self.neutral_cities_spin = QSpinBox()
        self.neutral_cities_spin.setRange(0, 50)
        self.neutral_cities_spin.setValue(2)

        # Difficulty selector (0..4)
        self.difficulty_spin = QSpinBox()
        self.difficulty_spin.setRange(0, 4)
        self.difficulty_spin.setValue(1)

        pg_layout.addRow("Player cities:", self.player_cities_spin)
        pg_layout.addRow("Players:", self.players_spin)
        pg_layout.addRow("Neutral cities:", self.neutral_cities_spin)
        pg_layout.addRow("Difficulty:", self.difficulty_spin)
        # Teams: number of teams and per-player assignments
        # Allow up to 7 teams (columns) in the fixed grid; actual enabled teams
        # will be min(7, players-1) and adjusted when players change.
        self.teams_spin = QSpinBox()
        self.teams_spin.setRange(0, 7)
        # initial max: min(7, players-1)
        self.teams_spin.setMaximum(min(7, max(0, int(self.players_spin.value()) - 1)))
        self.teams_spin.setValue(0)
        pg_layout.addRow("Teams:", self.teams_spin)

        # Teams grid area: shows per-player radio buttons for selecting team
        self.teams_group = QGroupBox("Teams assignment")
        self.teams_grid_widget = QWidget()
        self.teams_grid_layout = QtWidgets.QGridLayout()
        self.teams_grid_layout.setContentsMargins(6, 6, 6, 6)
        self.teams_grid_widget.setLayout(self.teams_grid_layout)
        tg_layout = QVBoxLayout()
        tg_layout.addWidget(self.teams_grid_widget)
        self.teams_group.setLayout(tg_layout)

        # Victory and Loss conditions split into separate groups
        victory_group = QGroupBox("Victory condition")
        victory_layout = QFormLayout()

        loss_group = QGroupBox("Loss condition")
        loss_layout = QFormLayout()

        # Victory condition selector
        self.victory_combo = QComboBox()
        # options: Normal + requested special ones
        self.victory_combo.addItem("Normal", VictoryConditions.NORMAL)
        self.victory_combo.addItem("Acquire specific artifact", VictoryConditions.ACQUIRE_ARTIFACT)
        self.victory_combo.addItem("Accumulate creatures", VictoryConditions.ACCUMULATE_CREATURES)
        self.victory_combo.addItem("Accumulate resources", VictoryConditions.ACCUMULATE_RESOURCES)
        self.victory_combo.addItem("Flag all dwellings", VictoryConditions.FLAG_DWELLINGS)
        self.victory_combo.addItem("Flag all mines", VictoryConditions.FLAG_MINES)

        # extra controls for victory types (create explicit labels so we can
        # hide/show both label + control in the form layout)
        self.artifact_combo = QComboBox()
        for a in ArtifactType:
            self.artifact_combo.addItem(a.name, a)
        self.artifact_label = QLabel("Artifact:")

        self.creature_combo = QComboBox()
        for c in CreatureType:
            self.creature_combo.addItem(c.name, c)
        self.creature_label = QLabel("Creature type:")
        self.creature_count_spin = QSpinBox()
        self.creature_count_spin.setRange(1, 10000)
        self.creature_count_spin.setValue(50)
        self.creature_count_label = QLabel("Creature count:")

        self.resource_combo = QComboBox()
        for r in ResourceType:
            self.resource_combo.addItem(r.name, r)
        self.resource_label = QLabel("Resource:")
        self.resource_amount_spin = QSpinBox()
        self.resource_amount_spin.setRange(1, 1000000)
        self.resource_amount_spin.setValue(100)
        self.resource_amount_label = QLabel("Resource amount:")

        # Loss condition selector
        self.loss_combo = QComboBox()
        self.loss_combo.addItem("Normal", LossConditions.NORMAL)
        self.loss_combo.addItem("Time expires", LossConditions.TIME_EXPIRES)
        self.loss_days_spin = QSpinBox()
        self.loss_days_spin.setRange(0, 1000)
        self.loss_days_spin.setValue(6)

        # create explicit labels for the Victory/Loss rows so we can color them
        self.victory_label = QLabel("Victory:")
        try:
            self.victory_label.setStyleSheet("color: green; font-weight: bold;")
        except Exception:
            pass
        self.loss_label = QLabel("Loss:")
        try:
            self.loss_label.setStyleSheet("color: red; font-weight: bold;")
        except Exception:
            pass

        # Add victory-related rows
        victory_layout.addRow(self.victory_label, self.victory_combo)
        victory_layout.addRow(self.artifact_label, self.artifact_combo)
        victory_layout.addRow(self.creature_label, self.creature_combo)
        victory_layout.addRow(self.creature_count_label, self.creature_count_spin)
        victory_layout.addRow(self.resource_label, self.resource_combo)
        victory_layout.addRow(self.resource_amount_label, self.resource_amount_spin)
        victory_group.setLayout(victory_layout)

        # Add loss-related rows
        loss_layout.addRow(self.loss_label, self.loss_combo)
        # loss days with explicit label for toggling
        self.loss_days_label = QLabel("Loss days:")
        loss_layout.addRow(self.loss_days_label, self.loss_days_spin)
        loss_group.setLayout(loss_layout)

        # Visibility logic: show only controls relevant to chosen victory type
        def _on_victory_changed(_):
            v = self.victory_combo.currentData()
            is_art = (v == VictoryConditions.ACQUIRE_ARTIFACT)
            is_cre = (v == VictoryConditions.ACCUMULATE_CREATURES)
            is_res = (v == VictoryConditions.ACCUMULATE_RESOURCES)
            # artifact
            self.artifact_label.setVisible(is_art)
            self.artifact_combo.setVisible(is_art)
            # creatures
            self.creature_label.setVisible(is_cre)
            self.creature_combo.setVisible(is_cre)
            self.creature_count_label.setVisible(is_cre)
            self.creature_count_spin.setVisible(is_cre)
            # resources
            self.resource_label.setVisible(is_res)
            self.resource_combo.setVisible(is_res)
            self.resource_amount_label.setVisible(is_res)
            self.resource_amount_spin.setVisible(is_res)

        def _on_loss_changed(_):
            l = self.loss_combo.currentData()
            is_time = (l == LossConditions.TIME_EXPIRES)
            self.loss_days_label.setVisible(is_time)
            self.loss_days_spin.setVisible(is_time)

        self.victory_combo.currentIndexChanged.connect(_on_victory_changed)
        self.loss_combo.currentIndexChanged.connect(_on_loss_changed)
        # initialize visibility for both victory and loss
        _on_victory_changed(None)
        _on_loss_changed(None)

        # internal structures to manage radio buttons per player
        self.team_button_groups = []  # list of QButtonGroup, one per player (row)
        self.team_radio_buttons = []  # matrix: [player_index][team_index] -> QRadioButton

        # ensure teams grid reflects initial players/teams
        self._rebuild_teams_grid_needed = True
        # connect signals to rebuild teams grid when players or teams change
        self.teams_spin.valueChanged.connect(lambda _: self._rebuild_teams_grid())
        self.players_spin.valueChanged.connect(lambda _: self._rebuild_teams_grid())
        # build initial grid
        self._rebuild_teams_grid()
        players_group.setLayout(pg_layout)

        # Terrain group (already a QGroupBox)

        # Actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout()
        actions_layout.addWidget(self.generate_btn)
        actions_group.setLayout(actions_layout)
        # gentle color for Actions to make it stand out pleasantly
        # try:
        #     actions_group.setStyleSheet("background-color: rgba(200, 240, 200, 0.9); border: 1px solid rgba(0,0,0,0.08);")
        # except Exception:
        #     pass

        # Right column: preview (top) and Terrain values under it
        right_v = QVBoxLayout()
        right_v.setSpacing(6)
        right_v.setContentsMargins(0, 0, 0, 0)

        inner_preview = QVBoxLayout()
        inner_preview.setSpacing(4)
        self.preview_title = QLabel("Preview of the generated map")
        self.preview_title.setAlignment(QtCore.Qt.AlignHCenter)
        inner_preview.addWidget(self.preview_title, alignment=QtCore.Qt.AlignHCenter)

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(300, 300)
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        # placeholder text until a map is generated
        self.preview_label.setText("After generating a map, its preview will appear here.")
        self.preview_label.setStyleSheet("color: #666; border: 1px solid #ccc; padding: 6px;")
        inner_preview.addWidget(self.preview_label, alignment=QtCore.Qt.AlignHCenter)

        right_v.addLayout(inner_preview)

        # Top area: File (left) and Preview+Terrain (right)
        top_h = QHBoxLayout()
        top_h.addWidget(file_group, stretch=1)
        top_h.addLayout(right_v)

        # Bottom area: arrange Players, Win/Lose and Terrain in three columns
        bottom_area = QVBoxLayout()
        grid = QtWidgets.QGridLayout()

        # Row 0: composite area (Players side-by-side with Victory/Loss), and
        # Terrain & Actions on the right.
        # stack victory and loss groups vertically so grid layout doesn't change
        wl_widget = QWidget()
        wl_v = QVBoxLayout()
        # give some spacing between victory and loss so they don't visually overlap
        wl_v.setContentsMargins(4, 4, 4, 4)
        wl_v.setSpacing(8)
        wl_v.addWidget(victory_group)
        wl_v.addWidget(loss_group)
        wl_widget.setLayout(wl_v)

        # Composite group that places Players and Win/Lose side-by-side, with
        # Win/Lose given more horizontal space. Teams sits below them.
        composite_group = QGroupBox("Players & Win/Lose")
        comp_layout = QVBoxLayout()
        top_h_comp = QHBoxLayout()
        top_h_comp.addWidget(players_group, 1)
        top_h_comp.addWidget(wl_widget, 2)
        comp_layout.addLayout(top_h_comp)
        comp_layout.addWidget(self.teams_group)
        composite_group.setLayout(comp_layout)

        # Combine Terrain values and Actions into a single stacked group on the right
        terrain_actions_group = QGroupBox("Terrain & Actions")
        ta_layout = QVBoxLayout()
        ta_layout.setContentsMargins(6, 6, 6, 6)
        ta_layout.addWidget(self.terrain_group)
        ta_layout.addWidget(actions_group)
        terrain_actions_group.setLayout(ta_layout)
        # try:
        #     terrain_actions_group.setStyleSheet("background-color: rgba(220, 235, 255, 0.85); border: 1px solid rgba(0,0,0,0.06);")
        # except Exception:
        #     pass

        # Place composite on the left spanning columns 0..1 and rows 0..1
        grid.addWidget(composite_group, 0, 0, 2, 2)
        # Place terrain/actions on the right spanning both rows
        grid.addWidget(terrain_actions_group, 0, 2, 2, 1)

        # Make Players and Victory/Loss groups fixed-height so Terrain column
        # can expand vertically without affecting their heights. Give column 2
        # (Terrain) the stretch so extra vertical space is assigned there.
        players_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # allow victory/loss groups to request preferred heights so the vertical
        # layout can allocate space and avoid overlapping
        victory_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        loss_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.teams_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # Terrain should expand vertically and can push Actions down in column 2
        self.terrain_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        actions_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # Make Terrain and Actions match preview width and avoid them
        # taking excessive horizontal space. Use column stretches so columns
        # 0 and 1 receive extra width while column 2 stays compact.
        # Use preview width (fixed) for Terrain/Actions.
        try:
            preview_w = self.preview_label.width()
        except Exception:
            preview_w = 300
        self.terrain_group.setFixedWidth(preview_w)
        actions_group.setFixedWidth(preview_w)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        # Give the top row (where Terrain lives) the vertical stretch so
        # Terrain (3) can expand vertically while the bottom row (Teams +
        # Actions) remains compact.
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 0)

        bottom_area.addLayout(grid)

        # Overall wrapper: top row then bottom area then status
        wrapper = QVBoxLayout()
        wrapper.addLayout(top_h)
        wrapper.addLayout(bottom_area)
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

    def _on_add_terrain_clicked(self):
        txt = self.terrain_add_combo.currentText()
        if not txt:
            return
        try:
            t = TerrainType[txt]
        except Exception:
            return
        # add terrain row
        self._add_terrain(t)
        self._refresh_available_terrains()

    def _add_terrain(self, terrain: TerrainType):
        # if already present, ignore
        if terrain in self.terrain_widgets:
            return
        row = QWidget()
        hl = QHBoxLayout()
        hl.setContentsMargins(0, 0, 0, 0)
        row.setLayout(hl)

        label = QLabel(terrain.name)
        spin = QSpinBox()
        spin.setRange(1, 5)
        spin.setValue(1)
        remove_btn = QPushButton("Remove")

        def _remove_here():
            # prevent removing last terrain
            if len(self.terrain_widgets) <= 1:
                QMessageBox.warning(self, "Minimum terrains", "At least one terrain must be present.")
                return
            self._remove_terrain(terrain)
            self._refresh_available_terrains()

        remove_btn.clicked.connect(_remove_here)

        hl.addWidget(label)
        hl.addWidget(spin)
        hl.addWidget(remove_btn)

        self.terrain_rows_layout.addWidget(row)
        self.terrain_widgets[terrain] = {'row': row, 'spin': spin}

    def _remove_terrain(self, terrain: TerrainType):
        info = self.terrain_widgets.get(terrain)
        if not info:
            return
        row = info['row']
        # remove widget from layout and delete
        self.terrain_rows_layout.removeWidget(row)
        row.setParent(None)
        row.deleteLater()
        del self.terrain_widgets[terrain]

    def _refresh_available_terrains(self):
        # update add combo to show only terrains not yet added
        current = self.terrain_add_combo.currentText()
        self.terrain_add_combo.clear()
        for t in TerrainType:
            if t == TerrainType.SUBTERRANEAN or t == TerrainType.ROCK:
                continue
            if t not in self.terrain_widgets:
                self.terrain_add_combo.addItem(t.name)
        # if no available terrains left, disable add
        self.terrain_add_combo.setEnabled(self.terrain_add_combo.count() > 0)
        self.terrain_add_btn.setEnabled(self.terrain_add_combo.count() > 0)
        # try to restore previous selection if still present
        idx = self.terrain_add_combo.findText(current)
        if idx >= 0:
            self.terrain_add_combo.setCurrentIndex(idx)

    def _rebuild_teams_grid(self):
        # Build a fixed 8x7 grid (8 players rows x 7 team columns). Cells that are
        # outside the active player count or active team count will be disabled
        # (greyed out) and not clickable. This ensures a stable visual layout.
        # Clear existing grid widgets
        for i in reversed(range(self.teams_grid_layout.count())):
            item = self.teams_grid_layout.itemAt(i)
            w = item.widget()
            if w:
                self.teams_grid_layout.removeWidget(w)
                w.setParent(None)

        players_active = int(self.players_spin.value())
        num_teams_active = int(self.teams_spin.value())

        MAX_PLAYERS = 8
        MAX_TEAMS = 7

        self.team_button_groups = []
        self.team_radio_buttons = []

        # Header row (team labels)
        self.teams_grid_layout.addWidget(QLabel("Player"), 0, 0)
        self._team_header_labels = []
        for c in range(MAX_TEAMS):
            lbl = QLabel(f"Team {c+1}")
            # disable header if this team index is not active
            enabled_col = (c < num_teams_active)
            lbl.setEnabled(enabled_col)
            self.teams_grid_layout.addWidget(lbl, 0, c+1)
            self._team_header_labels.append(lbl)

        # Rows for players 1..8
        for r in range(MAX_PLAYERS):
            p_label = OutlinedLabel(f"Player {r+1}")
            # disable entire row if player index is not active
            enabled_row = (r < players_active)
            p_label.setEnabled(enabled_row)
            # color player label according to player index
            try:
                _player_colors = [
                    'red',    # 1
                    'blue',   # 2
                    'tan',    # 3
                    'green',  # 4
                    'orange', # 5
                    'purple', # 6
                    'teal',   # 7
                    'pink',   # 8
                ]
                col = _player_colors[r] if r < len(_player_colors) else 'black'
                p_label.setStyleSheet(f"color: {col};")
                # add a subtle black outline using a drop shadow effect with zero offset
                try:
                    effect = QtWidgets.QGraphicsDropShadowEffect(self)
                    effect.setBlurRadius(6)
                    effect.setColor(QtCore.Qt.black)
                    effect.setOffset(0, 0)
                    p_label.setGraphicsEffect(effect)
                except Exception:
                    pass
            except Exception:
                pass
            self.teams_grid_layout.addWidget(p_label, r+1, 0)

            btn_group = QtWidgets.QButtonGroup(self)
            btn_group.setExclusive(True)
            row_buttons = []
            for c in range(MAX_TEAMS):
                rb = QtWidgets.QRadioButton()
                # determine whether this cell should be enabled: both the row
                # (player used) and the column (team enabled)
                enabled_cell = enabled_row and (c < num_teams_active)
                rb.setEnabled(enabled_cell)
                # If the cell is disabled, ensure it's unchecked
                if not enabled_cell:
                    rb.setChecked(False)
                self.teams_grid_layout.addWidget(rb, r+1, c+1)
                btn_group.addButton(rb, c)
                row_buttons.append(rb)

            # default selection for active rows: assign to team 0 if team 0 exists
            if enabled_row and num_teams_active > 0:
                # ensure team 0 is enabled
                if row_buttons and row_buttons[0].isEnabled():
                    row_buttons[0].setChecked(True)

            self.team_button_groups.append(btn_group)
            self.team_radio_buttons.append(row_buttons)

        self._rebuild_teams_grid_needed = False

    def on_generate(self):
        folder = self.folder_path_edit.text().strip()
        filename = self.filename_edit.text().strip()

        if not folder:
            QMessageBox.warning(self, "Missing folder", "Please select a folder to save the file.")
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

            # collect terrain values from dynamic terrain_widgets
            terrain_values = {}
            for t, info in self.terrain_widgets.items():
                try:
                    terrain_values[t] = int(info['spin'].value())
                except Exception:
                    pass

            # Constraint: WATER value cannot be more than 1/3 of total terrain values
            try:
                total_val = sum(terrain_values.values())
                water_val = terrain_values.get(TerrainType.WATER, 0)
                if total_val > 0 and water_val > (total_val / 3.0):
                    QMessageBox.warning(self, "Terrain constraint", "Water value cannot be more than one third of the sum of all terrain values.")
                    self.generate_btn.setEnabled(True)
                    return
            except Exception:
                # if anything goes wrong, don't block generation here
                pass

            # parse selected size (e.g. "72x72") from closed list
            size_text = self.size_combo.currentText()
            try:
                w_str, h_str = size_text.split('x')
                size_val = int(w_str)
            except Exception:
                size_val = 72
            width = height = size_val
            # Build teams_params according to UI
            num_teams = int(self.teams_spin.value())
            players_count = int(self.players_spin.value())
            teams_params = None
            if num_teams > 0:
                # collect per-player team assignments
                team_for_player = []
                # collect team assignments for existing players only (0..players_count-1)
                for p_idx in range(players_count):
                    # if radio groups not present (e.g., UI mismatch) default to team 0
                    if p_idx < len(self.team_button_groups):
                        gid = self.team_button_groups[p_idx].checkedId()
                        if gid is None or gid < 0:
                            QMessageBox.warning(self, "Teams", f"Player {p_idx+1} has no team selected. Please assign a team.")
                            self.generate_btn.setEnabled(True)
                            return
                        team_for_player.append(int(gid))
                    else:
                        team_for_player.append(0)

                # validate: every team must have at least one REAL player assigned
                counts = [0] * num_teams
                for t in team_for_player[:players_count]:
                    if 0 <= t < num_teams:
                        counts[t] += 1
                empty = [i for i, c in enumerate(counts) if c == 0]
                if empty:
                    QMessageBox.warning(self, "Teams", f"Each team must have at least one player. Teams without players: {', '.join(str(i+1) for i in empty)}")
                    self.generate_btn.setEnabled(True)
                    return

                # H3M/JSON format expects team_for_player to be length 8 — pad with zeros for unused slots
                while len(team_for_player) < 8:
                    team_for_player.append(0)

                teams_params = TeamsParams(num_teams=num_teams, team_for_player=team_for_player)

            # Build victory / loss params from UI
            vc_params = None
            lc_params = None

            v_choice = self.victory_combo.currentData()
            if v_choice is not None and v_choice != VictoryConditions.NORMAL:
                vc_params = VictoryConditionParams()
                vc_params.victory_condition = v_choice
                # fill specific fields
                if v_choice == VictoryConditions.ACQUIRE_ARTIFACT:
                    vc_params.artifact_type = self.artifact_combo.currentData()
                elif v_choice == VictoryConditions.ACCUMULATE_CREATURES:
                    vc_params.creature_type = self.creature_combo.currentData()
                    vc_params.count = int(self.creature_count_spin.value())
                elif v_choice == VictoryConditions.ACCUMULATE_RESOURCES:
                    vc_params.resource_type = self.resource_combo.currentData()
                    vc_params.amount = int(self.resource_amount_spin.value())

            l_choice = self.loss_combo.currentData()
            if l_choice is not None and l_choice != LossConditions.NORMAL:
                lc_params = LossConditionParams()
                lc_params.loss_condition = l_choice
                if l_choice == LossConditions.TIME_EXPIRES:
                    lc_params.days = int(self.loss_days_spin.value())

            map = generate_voronoi_map(
                terrain_values,
                size=size_val,
                players_count=int(self.players_spin.value()),
                player_cities=int(self.player_cities_spin.value()),
                neutral_cities=int(self.neutral_cities_spin.value()),
                difficulty=int(self.difficulty_spin.value()),
                victory_condition_params=vc_params,
                loss_condition_params=lc_params,
                teams_params=teams_params,
            )
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
            # Inject user-provided basic info if present
            try:
                name_val = self.map_name_edit.text().strip()
                desc_val = self.map_desc_edit.toPlainText().strip()
                # enforce limits again
                if len(name_val) > 30:
                    name_val = name_val[:30]
                if len(desc_val) > self.map_desc_max:
                    desc_val = desc_val[: self.map_desc_max]
                if hasattr(map, 'basic_info') and map.basic_info is not None:
                    try:
                        map.basic_info.name = name_val
                        map.basic_info.description = desc_val
                    except Exception:
                        # basic_info may be plain dict-like
                        try:
                            map.basic_info['name'] = name_val
                            map.basic_info['description'] = desc_val
                        except Exception:
                            pass
                # re-serialize after injection
                map_dict = filter_none_values(map.to_dict())
            except Exception:
                pass
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
                try:
                    print("successfully generated a map using GUI")
                except Exception:
                    pass
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
                    try:
                        print("successfully generated a map using GUI")
                    except Exception:
                        pass
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
