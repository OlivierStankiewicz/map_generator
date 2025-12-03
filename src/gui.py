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
    QGridLayout
)
from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath, QPen, QColor, QFontMetrics
import sys
import os
import json
import subprocess
import shutil
import traceback
from datetime import datetime

H3MTXT_NAME = 'h3mtxt.exe'
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
H3MTXT_DEFAULT_PATH = os.path.join(_PROJECT_ROOT, H3MTXT_NAME)

MAX_TOTAL_TOWNS = 48

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
from classes.Enums.HallLevel import HallLevel
from classes.Enums.CastleLevel import CastleLevel
from classes.additional_info.VictoryConditions.UpgradeTown import UpgradeTown
from classes.additional_info.VictoryConditions.CaptureTown import CaptureTown
from classes.additional_info.VictoryConditions.DefeatHero import DefeatHero
from classes.additional_info.VictoryConditions.DefeatMonster import DefeatMonster
from classes.additional_info.LossConditions.LoseTown import LoseTown
from classes.additional_info.LossConditions.LoseHero import LoseHero
from classes.additional_info.VictoryConditions.DefeatHero import DefeatHero

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
        # Make the default window a bit taller so more controls fit vertically
        self.resize(820, 820)

        # Widgets
        self.folder_label = QLabel("Save folder:")
        self.folder_path_edit = QLineEdit()
        self.folder_browse_btn = QPushButton("Browse")
        self.folder_browse_btn.setCursor(QtCore.Qt.PointingHandCursor)

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
        self.size_combo.addItems(["36x36 (Small)", "72x72 (Medium)", "108x108 (Large)", "144x144 (Extra Large)"])
        # default to 72x72
        self.size_combo.setCurrentText("72x72 (Medium)")

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
        self.terrain_add_btn.setCursor(QtCore.Qt.PointingHandCursor)
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

        # Ensure the add-combo does not contain terrains already added (DIRT)
        # and default the selection to SAND for convenience.
        try:
            self._refresh_available_terrains()
            idx_sand = self.terrain_add_combo.findText("SAND")
            if idx_sand >= 0:
                self.terrain_add_combo.setCurrentIndex(idx_sand)
        except Exception:
            pass

        self.generate_btn = QPushButton("Generate map")
        self.generate_btn.setToolTip("Generate the map with the specified parameters")
        self.generate_btn.setStyleSheet("font-weight: bold;")
        try:
            # match height with the Manual QToolButton for consistent appearance
            self.generate_btn.setFixedHeight(34)
        except Exception:
            pass
        self.status_label = QLabel("")

        # Layout
        # Build File group (now contains Save folder as a sub-group)
        # Use a titled, framed group for file-related info per user request
        file_group = QGroupBox("File info")
        file_layout = QVBoxLayout()

        # Save widget: combine Save folder and Filename into one plain widget
        save_widget = QWidget()
        save_layout = QVBoxLayout()
        save_layout.setContentsMargins(0, 0, 0, 0)

        # Folder row (label, path edit, browse)
        folder_row = QHBoxLayout()
        folder_row.setContentsMargins(0, 0, 0, 0)
        folder_row.addWidget(self.folder_label)
        folder_row.addWidget(self.folder_path_edit)
        folder_row.addWidget(self.folder_browse_btn)

        # Filename row (label, edit)
        filename_row = QHBoxLayout()
        filename_row.setContentsMargins(0, 0, 0, 0)
        filename_row.addWidget(self.filename_label)
        filename_row.addWidget(self.filename_edit)
        # Reset button to restore filename to a timestamped default
        self.filename_reset_btn = QPushButton("Default")
        self.filename_reset_btn.setCursor(QtCore.Qt.PointingHandCursor)
        try:
            self.filename_reset_btn.setToolTip("Reset file name to a timestamped default")
            self.filename_reset_btn.clicked.connect(lambda: self._reset_filename())
        except Exception:
            pass
        filename_row.addWidget(self.filename_reset_btn)

        save_layout.addLayout(folder_row)
        save_layout.addLayout(filename_row)
        save_widget.setLayout(save_layout)

        file_layout.addWidget(save_widget)
        file_group.setLayout(file_layout)

        # Map info (name + description + size) — keep as a separate boxed section
        map_info_group = QGroupBox("Map info")
        map_info_layout = QFormLayout()
        # Map name row with Reset button
        name_row = QWidget()
        name_h = QHBoxLayout()
        name_h.setContentsMargins(0, 0, 0, 0)
        name_h.addWidget(self.map_name_edit)
        self.map_name_reset_btn = QPushButton("Default")
        self.map_name_reset_btn.setCursor(QtCore.Qt.PointingHandCursor)
        try:
            self.map_name_reset_btn.setToolTip("Reset map name to a timestamped default")
            self.map_name_reset_btn.clicked.connect(lambda: self._reset_map_name())
        except Exception:
            pass
        name_h.addWidget(self.map_name_reset_btn)
        name_row.setLayout(name_h)
        map_info_layout.addRow(self.map_name_label, name_row)

        # Map description row with Reset button
        desc_row = QWidget()
        desc_h = QHBoxLayout()
        desc_h.setContentsMargins(0, 0, 0, 0)
        desc_h.addWidget(self.map_desc_edit)
        self.map_desc_reset_btn = QPushButton("Default")
        self.map_desc_reset_btn.setCursor(QtCore.Qt.PointingHandCursor)
        try:
            self.map_desc_reset_btn.setToolTip("Reset description to a timestamped default")
            self.map_desc_reset_btn.clicked.connect(lambda: self._reset_map_desc())
        except Exception:
            pass
        desc_h.addWidget(self.map_desc_reset_btn)
        desc_row.setLayout(desc_h)
        map_info_layout.addRow(self.map_desc_label, desc_row)

        # place size warning under the Map description (Map info section)
        try:
            # inline QLabel warning (no dialogs) — created here so it's in Map info
            self.size_warning_label = QLabel("")
            self.size_warning_label.setWordWrap(True)
            try:
                self.size_warning_label.setStyleSheet("color: #b35; font-style: italic;")
            except Exception:
                pass
            self.size_warning_label.setVisible(False)
            map_info_layout.addRow("", self.size_warning_label)
        except Exception:
            pass
        # Include Map size in the Map info group
        map_info_layout.addRow(self.size_label, self.size_combo)
        map_info_group.setLayout(map_info_layout)

        # Left column container: stack File info and Map info vertically
        left_column = QWidget()
        left_column_layout = QVBoxLayout()
        left_column_layout.setContentsMargins(0, 0, 0, 0)
        left_column_layout.setSpacing(8)
        left_column_layout.addWidget(file_group)
        left_column_layout.addWidget(map_info_group)
        left_column.setLayout(left_column_layout)

        # Players group: player count (synced with player cities) and neutral cities
        players_group = QGroupBox("Players / Cities")
        pg_layout = QFormLayout()
        self.player_cities_spin = QSpinBox()
        # Require at least 1 player city (1..8)
        self.player_cities_spin.setRange(1, 8)
        self.player_cities_spin.setValue(5)
        self.players_spin = QSpinBox()
        # Require at least 1 player (1..8)
        self.players_spin.setRange(1, 8)
        self.players_spin.setValue(5)
        try:
            self._style_spinbox_no_caret(self.player_cities_spin)
        except Exception:
            pass
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

            # Ensure neutral cities respect total cap (MAX_TOTAL_TOWNS - 1). Player cities take priority.
            try:
                try:
                    neutral_val = int(self.neutral_cities_spin.value())
                except Exception:
                    neutral_val = 0
                allowed = max(0, MAX_TOTAL_TOWNS - 1 - int(val))
                if neutral_val > allowed:
                    # reduce neutral cities to allowed maximum
                    self.neutral_cities_spin.blockSignals(True)
                    try:
                        self.neutral_cities_spin.setValue(allowed)
                    finally:
                        self.neutral_cities_spin.blockSignals(False)
                # also update the neutral spin maximum so user cannot increase beyond allowed
                try:
                    self.neutral_cities_spin.setMaximum(allowed)
                except Exception:
                    pass
            except Exception:
                pass

            # refresh size/players warning
            try:
                self._update_size_players_warning()
            except Exception:
                pass

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

            # refresh size/players warning
            try:
                self._update_size_players_warning()
            except Exception:
                pass

        self.player_cities_spin.valueChanged.connect(_on_player_cities_changed)
        self.players_spin.valueChanged.connect(_on_players_changed)

        # update warning when map size changes as well
        try:
            self.size_combo.currentIndexChanged.connect(lambda _: self._update_size_players_warning())
        except Exception:
            pass

        self.neutral_cities_spin = QSpinBox()
        # neutral cities initial allowed range; actual max is adjusted dynamically
        self.neutral_cities_spin.setRange(0, MAX_TOTAL_TOWNS - 1)
        # ensure neutral initial value is reasonable
        self.neutral_cities_spin.setValue(2)
        try:
            self._style_spinbox_no_caret(self.neutral_cities_spin)
        except Exception:
            pass

        # adjust neutral maximum according to current player_cities
        try:
            try:
                pc = int(self.player_cities_spin.value())
            except Exception:
                pc = 0
            allowed = max(0, 47 - pc)
            self.neutral_cities_spin.setMaximum(allowed)
        except Exception:
            pass

        # handler: prevent increasing neutral beyond allowed total (MAX_TOTAL_TOWNS - 1)
        def _on_neutral_changed(val):
            try:
                try:
                    pc = int(self.player_cities_spin.value())
                except Exception:
                    pc = 0
                allowed = max(0, MAX_TOTAL_TOWNS - 1 - pc)
                if val > allowed:
                    # revert to allowed
                    self.neutral_cities_spin.blockSignals(True)
                    try:
                        self.neutral_cities_spin.setValue(allowed)
                    finally:
                        self.neutral_cities_spin.blockSignals(False)
            except Exception:
                pass

        self.neutral_cities_spin.valueChanged.connect(_on_neutral_changed)

        # Difficulty selector (0..4)
        self.difficulty_spin = QSpinBox()
        self.difficulty_spin.setRange(0, 4)
        self.difficulty_spin.setValue(1)
        try:
            self._style_spinbox_no_caret(self.difficulty_spin)
        except Exception:
            pass

        pg_layout.addRow("Player cities:", self.player_cities_spin)
        pg_layout.addRow("Players:", self.players_spin)
        pg_layout.addRow("Neutral cities:", self.neutral_cities_spin)
        pg_layout.addRow("Difficulty:", self.difficulty_spin)
        # (size warning label is defined in Map info section)
        # Teams: number of teams and per-player assignments
        # Allow up to 7 teams (columns) in the fixed grid; actual enabled teams
        # will be min(7, players-1) and adjusted when players change.
        self.teams_spin = QSpinBox()
        self.teams_spin.setRange(0, 7)
        # initial max: min(7, players-1)
        self.teams_spin.setMaximum(min(7, max(0, int(self.players_spin.value()) - 1)))
        self.teams_spin.setValue(0)
        try:
            self._style_spinbox_no_caret(self.teams_spin)
        except Exception:
            pass
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
        # New options that require selecting a town after generation
        self.victory_combo.addItem("Build the grail structure", VictoryConditions.BUILD_GRAIL)
        self.victory_combo.addItem("Transport artifact", VictoryConditions.TRANSPORT_ARTIFACT)
        # Upgrade town option (opens UpgradeTownDialog after generation)
        self.victory_combo.addItem("Upgrade town", VictoryConditions.UPGRADE_TOWN)
        # Capture specific town (opens CaptureTownDialog after generation)
        self.victory_combo.addItem("Capture town", VictoryConditions.CAPTURE_TOWN)
        # Defeat a specific hero
        self.victory_combo.addItem("Defeat a specific hero", VictoryConditions.DEFEAT_HERO)
        # Defeat a specific monster (opens monster picker after generation)
        self.victory_combo.addItem("Defeat a specific monster", VictoryConditions.DEFEAT_MONSTER)

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
        # Lose specific town option
        self.loss_combo.addItem("Lose a specific town", LossConditions.LOSE_TOWN)
        # Lose specific hero option
        self.loss_combo.addItem("Lose a specific hero", LossConditions.LOSE_HERO)
        # Dropdown for time-based loss parameters. Each item stores the
        # corresponding number of days as its data value.
        self.loss_days_combo = QComboBox()
        # single-day options (2..6 days)
        for d in range(2, 7):
            self.loss_days_combo.addItem(f"{d} days", d)
        # weeks: 1..7 -> 7,14,...,49
        for w in range(1, 8):
            days = w * 7
            label = f"{w} week" if w == 1 else f"{w} weeks"
            self.loss_days_combo.addItem(label, days)
        # months: 2..12 months, each month == 4 weeks == 28 days
        for m in range(2, 13):
            days = m * 4 * 7
            label = f"{m} months"
            self.loss_days_combo.addItem(label, days)
        # default selection to 2 days (like in map editor)
        idx = self.loss_days_combo.findData(2)
        if idx >= 0:
            self.loss_days_combo.setCurrentIndex(idx)

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
        # informational text shown when a victory type requires user selection
        self.victory_info_label = QLabel("")
        self.victory_info_label.setWordWrap(True)
        try:
            self.victory_info_label.setStyleSheet("color: #444; font-style: italic;")
        except Exception:
            pass
        victory_layout.addRow(self.victory_info_label)
        victory_group.setLayout(victory_layout)

        # Add loss-related rows
        loss_layout.addRow(self.loss_label, self.loss_combo)
        # loss days with explicit label for toggling
        self.loss_days_label = QLabel("Loss days:")
        loss_layout.addRow(self.loss_days_label, self.loss_days_combo)
        # informational text shown when a loss type requires user selection
        self.loss_info_label = QLabel("")
        self.loss_info_label.setWordWrap(True)
        try:
            self.loss_info_label.setStyleSheet("color: #444; font-style: italic;")
        except Exception:
            pass
        loss_layout.addRow(self.loss_info_label)
        loss_group.setLayout(loss_layout)

        # Visibility logic: show only controls relevant to chosen victory type
        def _on_victory_changed(_):
            v = self.victory_combo.currentData()
            # artifact parameter is required for both Acquire and Transport
            is_art = (v == VictoryConditions.ACQUIRE_ARTIFACT or v == VictoryConditions.TRANSPORT_ARTIFACT)
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
            # update informational text for victory types that require a post-generation selection
            try:
                info_msg = ""
                if v == VictoryConditions.BUILD_GRAIL:
                    info_msg = "After generation you will be asked to select a town where the grail structure must be built."
                elif v == VictoryConditions.TRANSPORT_ARTIFACT:
                    info_msg = "After generation you will be asked to select a town to receive the transported artifact."
                elif v == VictoryConditions.UPGRADE_TOWN:
                    info_msg = "After generation you will be asked to select a town to be upgraded and its parameters."
                elif v == VictoryConditions.CAPTURE_TOWN:
                    info_msg = "After generation you will be asked to select a town to be captured for the victory condition."
                elif v == VictoryConditions.DEFEAT_HERO:
                    info_msg = "After generation you will be asked to select a hero to be defeated for the victory condition."
                elif v == VictoryConditions.DEFEAT_MONSTER:
                    info_msg = "After generation you will be asked to select a monster to be defeated for the victory condition."
                else:
                    info_msg = ""
                self.victory_info_label.setText(info_msg)
                self.victory_info_label.setVisible(bool(info_msg))
            except Exception:
                pass

        def _on_loss_changed(_):
            l = self.loss_combo.currentData()
            is_time = (l == LossConditions.TIME_EXPIRES)
            self.loss_days_label.setVisible(is_time)
            self.loss_days_combo.setVisible(is_time)
            # update informational text for loss types that require a post-generation selection
            try:
                info_msg = ""
                if l == LossConditions.LOSE_TOWN:
                    info_msg = "After generation you will be asked to select a town that the player will lose."
                elif l == LossConditions.LOSE_HERO:
                    info_msg = "After generation you will be asked to select a hero that the player will lose."
                else:
                    info_msg = ""
                self.loss_info_label.setText(info_msg)
                self.loss_info_label.setVisible(bool(info_msg))
            except Exception:
                pass

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
        # 123456
        # Actions group
        # Layout: Generate button on the left (wide, ~4x), other buttons stacked on the right
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(6, 6, 6, 6)
        actions_layout.setSpacing(8)

        # Determine a sensible height for buttons (fallback to 34)
        try:
            btn_h = self.generate_btn.sizeHint().height()
            if not btn_h or btn_h <= 0:
                btn_h = 34
        except Exception:
            btn_h = 34

        # Configure Generate button: make it taller (4x height)
        try:
            self.generate_btn.setFixedHeight(btn_h * 4)
            self.generate_btn.setStyleSheet("background-color:rgb(219, 255, 214); font-weight: bold;")
            self.generate_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.generate_btn.setCursor(QtCore.Qt.PointingHandCursor)
        except Exception:
            pass

        # Manual/info button
        self.info_btn = QPushButton()
        try:
            icon = QApplication.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation)
            self.info_btn.setIcon(icon)
        except Exception:
            pass
        self.info_btn.setToolTip("Show manual / how-to")
        try:
            self.info_btn.setText("Manual")
            self.info_btn.setIconSize(QtCore.QSize(18, 18))
            self.info_btn.setFixedHeight(btn_h)
            self.info_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.info_btn.setStyleSheet("padding: 4px; text-align: center;")
        except Exception:
            pass
        self.info_btn.setCursor(QtCore.Qt.PointingHandCursor)

        # Save / Load config buttons
        self.save_config_btn = QPushButton("Save config")
        try:
            self.save_config_btn.setToolTip("Save current UI configuration to a JSON file")
            self.save_config_btn.clicked.connect(self.on_save_config)
            self.save_config_btn.setFixedHeight(btn_h)
            self.save_config_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.save_config_btn.setCursor(QtCore.Qt.PointingHandCursor)
        except Exception:
            pass

        self.load_config_btn = QPushButton("Load config")
        try:
            self.load_config_btn.setToolTip("Load UI configuration from a JSON file")
            self.load_config_btn.clicked.connect(self.on_load_config)
            self.load_config_btn.setFixedHeight(btn_h)
            self.load_config_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.load_config_btn.setCursor(QtCore.Qt.PointingHandCursor)
        except Exception:
            pass

        # Right-side vertical stack for the three smaller buttons
        right_stack = QVBoxLayout()
        right_stack.setContentsMargins(0, 0, 0, 0)
        right_stack.setSpacing(6)

        # Reset all parameters button
        self.reset_all_btn = QPushButton("Reset all parameters")
        try:
            self.reset_all_btn.setToolTip("Reset all UI parameters to defaults")
            self.reset_all_btn.setFixedHeight(btn_h)
            self.reset_all_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.reset_all_btn.clicked.connect(self.on_reset_all_parameters)
            self.reset_all_btn.setCursor(QtCore.Qt.PointingHandCursor)
        except Exception:
            pass
        right_stack.addWidget(self.reset_all_btn)

        right_stack.addWidget(self.info_btn)
        right_stack.addWidget(self.save_config_btn)
        right_stack.addWidget(self.load_config_btn)
        right_stack.addStretch()

        # Add Generate on the left and the right stack on the right. Generate
        # is now taller (3x); keep width distribution balanced by using equal
        # stretch so it doesn't become overly wide.
        actions_layout.addWidget(self.generate_btn, 1)
        actions_layout.addLayout(right_stack, 1)

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

        # Wrap preview area in a titled GroupBox so it matches other sections
        preview_group = QGroupBox("Map preview")
        preview_group.setContentsMargins(6, 8, 6, 6)
        preview_group_layout = QVBoxLayout()
        preview_group_layout.setSpacing(4)
        # give a slightly larger top margin so the preview area has breathing room
        preview_group_layout.setContentsMargins(6, 12, 6, 6)

        # Top row: right-aligned info/manual button
        top_preview_h = QHBoxLayout()
        top_preview_h.setContentsMargins(0, 0, 0, 0)
        top_preview_h.addStretch()

        # keep preview title area compact (info button moved to Actions bar)

        preview_group_layout.addLayout(top_preview_h)

        self.preview_label = QLabel()
        # allow the preview to shrink when the window is smaller, but keep a
        # reasonable maximum so layout remains usable
        self.preview_label.setMinimumSize(150, 150)
        self.preview_label.setMaximumSize(300, 300)
        self.preview_label.setAlignment(QtCore.Qt.AlignCenter)
        # placeholder text until a map is generated
        self.preview_label.setText("After generating a map, its preview will appear here.")
        self.preview_label.setStyleSheet("color: #666; border: 1px solid #ccc; padding: 6px;")
        preview_group_layout.addWidget(self.preview_label, alignment=QtCore.Qt.AlignHCenter)

        # Button to save the preview BMP (uses existing on_save_preview)
        self.save_preview_btn = QPushButton("Save preview")
        self.save_preview_btn.setToolTip("Save preview BMP of last generated map")
        self.save_preview_btn.setFixedWidth(140)
        self.save_preview_btn.setCursor(QtCore.Qt.PointingHandCursor)
        try:
            self.save_preview_btn.clicked.connect(self.on_save_preview)
        except Exception:
            pass
        preview_group_layout.addWidget(self.save_preview_btn, alignment=QtCore.Qt.AlignHCenter)

        preview_group.setLayout(preview_group_layout)
        right_v.addWidget(preview_group)

        # Top area: File info + Map info stacked left and Preview+Terrain on right
        top_h = QHBoxLayout()
        # use the left column container created earlier (stacks File info and Map info)
        top_h.addWidget(left_column, stretch=1)
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
        composite_group = QWidget()
        comp_layout = QVBoxLayout()
        top_h_comp = QHBoxLayout()
        top_h_comp.addWidget(players_group, 1)
        top_h_comp.addWidget(wl_widget, 2)
        comp_layout.addLayout(top_h_comp)
        comp_layout.addWidget(self.teams_group)
        composite_group.setLayout(comp_layout)

        # Combine Terrain values and Actions into a single stacked group on the right
        terrain_actions_group = QWidget()
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
        # add spacing so sections don't visually overlap when the window is
        # resized smaller; the QScrollArea will provide scrollbars if needed
        wrapper.setSpacing(12)
        wrapper.addLayout(top_h)
        wrapper.addLayout(bottom_area)
        wrapper.addWidget(self.status_label)

        # Make the whole GUI content scrollable when the window is too small.
        content_widget = QWidget()
        content_widget.setLayout(wrapper)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)

        # Use a stacked widget so we can switch between main UI and a manual view
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(scroll)  # index 0 = main UI

        # Manual / how-to page
        manual_widget = QWidget()
        manual_layout = QVBoxLayout()
        manual_layout.setContentsMargins(8, 8, 8, 8)
        manual_title = QLabel("Manual - How to use the Map Generator")
        manual_title.setStyleSheet("font-weight: bold; font-size: 16px;")
        manual_layout.addWidget(manual_title)

        # Show manual as formatted QLabel (larger font, label-like appearance)
        manual_body = (
            "Welcome to the Heroes III: Shadow of Death map generator! This generator uses PCG algorithms to create unique maps. Below are the steps to create a map:\n"
            "1. Select the save folder and file name.\n"
            "2. Enter the map name and description.\n"
            "3. Set the map size (e.g., 72x72).\n"
            "4. Add terrain values on the right (e.g., DIRT, GRASS) and set their estimated coverage.\n"
            "5. Set the number of players and towns, and optionally teams.\n"
            "6. In the Win/Lose section, choose victory or defeat conditions and set any additional parameters.\n"
            "7. Press 'Generate map' to generate the map representation and preview.\n"
            "8. Optionally, select parameters for Win/Lose conditions that require post-generation selection.\n"
            "9. Your map will be saved as a .h3m file in the specified folder.\n\n"
            "To use the generated map, simply copy the .h3m file into your Heroes III: SoD 'Maps' folder - it will be visible in the game.\n"
            "Enjoy!\n\n"
            "Additionally:\n"
            "- You can save the map preview to a BMP file.\n"
            "- You can save and load the current configuration to/from a JSON file for easy reuse of settings (if any field is invalid, it will be ignored and a default value will be used).\n\n"
            "What if the 'h3mtxt.exe' converter is not present?\n"
            "Only a JSON representation of the map will be saved. You can then use the h3mtxt.exe tool separately to convert JSON to .h3m.\n\n"
        )
        manual_html = manual_body.replace('\n', '<br>')
        manual_label = QLabel(f"<div style='font-size:13px; line-height:1.45;'>{manual_html}</div>")
        manual_label.setWordWrap(True)
        manual_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        manual_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Try to load 'nasza_mapa.PNG' from a few likely locations. If not found,
        # show a small placeholder label with instructions.
        img_label = QLabel()
        img_label.setAlignment(QtCore.Qt.AlignCenter)
        candidates = [
            os.path.join(os.path.dirname(__file__), '..', 'nasza_mapa.PNG'),
            os.path.join(os.path.dirname(__file__), '..', 'generated_maps', 'nasza_mapa.PNG'),
            os.path.join(os.getcwd(), 'nasza_mapa.PNG'),
        ]
        img_path = None
        for p in candidates:
            try:
                p_abs = os.path.abspath(p)
            except Exception:
                p_abs = p
            if os.path.exists(p_abs):
                img_path = p_abs
                break

        if img_path:
            try:
                pix = QPixmap(img_path)
                if not pix.isNull():
                    # scale to fit manual area (max width 320, keep aspect)
                    max_w = 320
                    max_h = 320
                    pix = pix.scaled(max_w, max_h, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    img_label.setPixmap(pix)
                else:
                    img_label.setText("[Image could not be loaded]")
            except Exception:
                img_label.setText("[Image load error]")
        else:
            img_label.setText("[Add nasza_mapa.PNG to project root to show image]")
            img_label.setStyleSheet('font-style: italic; color: #666;')

        # Place text on the left and image on the right
        manual_h = QHBoxLayout()
        manual_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        img_label.setMaximumWidth(320)
        manual_h.addWidget(manual_label, 1)
        manual_h.addWidget(img_label, 0)
        manual_layout.addLayout(manual_h)

        manual_close = QPushButton("Back to editor")
        manual_close.setFixedWidth(140)
        manual_close.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        manual_layout.addWidget(manual_close, alignment=QtCore.Qt.AlignRight)
        manual_widget.setLayout(manual_layout)

        self.stack.addWidget(manual_widget)  # index 1 = manual

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        # connect info button to show manual
        try:
            self.info_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        except Exception:
            pass

        # Signals
        self.folder_browse_btn.clicked.connect(self.browse_folder)
        self.generate_btn.clicked.connect(self.on_generate)

        # Thread holder
        self._worker_thread = None

    def _style_spinbox_no_caret(self, spin: QSpinBox):
        """Apply styling to a QSpinBox to make the internal QLineEdit selection
        background transparent and hide its caret while keeping the spinbox
        itself focusable for keyboard input.
        """
        try:
            le = None
            try:
                le = spin.lineEdit()
            except Exception:
                le = None
            style = (
                "selection-background-color: rgba(0,0,0,0);"
                "selection-color: rgba(0,0,0,1);"
            )
            if le is not None:
                try:
                    le.setStyleSheet(style)
                except Exception:
                    pass
                try:
                    le.setFocusPolicy(QtCore.Qt.NoFocus)
                except Exception:
                    pass
            else:
                try:
                    spin.setStyleSheet(f"QSpinBox QLineEdit {{ {style} }}")
                except Exception:
                    pass
            try:
                # keep the spinbox itself focusable so keyboard stepping works
                spin.setFocusPolicy(QtCore.Qt.StrongFocus)
            except Exception:
                pass
        except Exception:
            pass

    def _reset_filename(self):
        try:
            now = datetime.now()
            filename_default = f"my_map_{now.day:02d}_{now.month:02d}_{now.year}_{now.hour:02d}_{now.minute:02d}_{now.second:02d}"
            self.filename_edit.setText(filename_default)
        except Exception:
            pass

    def _reset_map_name(self):
        try:
            now = datetime.now()
            default_name = f"My Map {now.day}/{now.month}/{now.year} {now.hour:02d}:{now.minute:02d}:{now.second:02d}"
            self.map_name_edit.setText(default_name)
        except Exception:
            pass

    def _reset_map_desc(self):
        try:
            now = datetime.now()
            description_default = f"Map generated on {now.day}/{now.month}/{now.year} at {now.hour:02d}:{now.minute:02d}:{now.second:02d}."
            self.map_desc_edit.setPlainText(description_default)
        except Exception:
            pass

    def on_reset_all_parameters(self):
        """Reset all UI parameters to sensible defaults (timestamped name/filename/desc,
        default size, single terrain=Dirt, default player counts, difficulty, teams,
        victory/loss defaults and preview cleared).
        """
        try:
            # textual defaults (use same helpers so timestamps update)
            try:
                self._reset_filename()
                self._reset_map_name()
                self._reset_map_desc()
            except Exception:
                pass

            # size default to 72x72 (Medium)
            try:
                idx = self.size_combo.findText("72x72 (Medium)")
                if idx >= 0:
                    self.size_combo.setCurrentIndex(idx)
            except Exception:
                pass

            # terrains: remove all and add DIRT with value 1
            try:
                for t in list(self.terrain_widgets.keys()):
                    try:
                        self._remove_terrain(t)
                    except Exception:
                        pass
                try:
                    self._add_terrain(TerrainType.DIRT)
                    info = self.terrain_widgets.get(TerrainType.DIRT)
                    if info:
                        info['spin'].setValue(1)
                except Exception:
                    try:
                        first = list(TerrainType)[0]
                        self._add_terrain(first)
                    except Exception:
                        pass
                try:
                    self._refresh_available_terrains()
                except Exception:
                    pass
            except Exception:
                pass

            # players / cities / difficulty / teams
            try:
                self.player_cities_spin.setValue(5)
            except Exception:
                pass
            try:
                self.players_spin.setValue(5)
            except Exception:
                pass
            try:
                self.neutral_cities_spin.setValue(2)
            except Exception:
                pass
            try:
                self.difficulty_spin.setValue(1)
            except Exception:
                pass
            try:
                self.teams_spin.setValue(0)
            except Exception:
                pass
            try:
                self._rebuild_teams_grid()
            except Exception:
                pass

            # refresh size/players warning after reset
            try:
                self._update_size_players_warning()
            except Exception:
                pass

            # victory / loss defaults
            try:
                for i in range(self.victory_combo.count()):
                    data = self.victory_combo.itemData(i)
                    if data == VictoryConditions.NORMAL:
                        self.victory_combo.setCurrentIndex(i)
                        break
            except Exception:
                pass
            try:
                for i in range(self.loss_combo.count()):
                    data = self.loss_combo.itemData(i)
                    if data == LossConditions.NORMAL:
                        self.loss_combo.setCurrentIndex(i)
                        break
            except Exception:
                pass

            # victory param defaults
            try:
                self.artifact_combo.setCurrentIndex(0)
            except Exception:
                pass
            try:
                self.creature_combo.setCurrentIndex(0)
                self.creature_count_spin.setValue(50)
            except Exception:
                pass
            try:
                self.resource_combo.setCurrentIndex(0)
                self.resource_amount_spin.setValue(100)
            except Exception:
                pass

            # clear last generated preview/map
            try:
                self._last_map = None
                self._last_size = None
                try:
                    self.preview_label.clear()
                except Exception:
                    pass
                try:
                    self.preview_label.setText("After generating a map, its preview will appear here.")
                    self.preview_label.setStyleSheet("color: #666; border: 1px solid #ccc; padding: 6px;")
                except Exception:
                    pass
            except Exception:
                pass

            QMessageBox.information(self, "Reset", "All parameters have been reset to defaults.")
        except Exception as e:
            QMessageBox.critical(self, "Reset error", f"Failed to reset parameters: {e}")

    def on_save_config(self):
        try:
            cfg = {}
            cfg['folder'] = self.folder_path_edit.text()
            cfg['filename'] = self.filename_edit.text()
            cfg['map_name'] = self.map_name_edit.text()
            try:
                cfg['map_desc'] = self.map_desc_edit.toPlainText()
            except Exception:
                cfg['map_desc'] = ''
            cfg['size'] = self.size_combo.currentText()

            # terrains: store as name -> value
            terrains = {}
            for t, info in self.terrain_widgets.items():
                try:
                    t_name = t.name if hasattr(t, 'name') else str(t)
                    terrains[t_name] = int(info['spin'].value())
                except Exception:
                    pass
            cfg['terrains'] = terrains

            cfg['player_cities'] = int(self.player_cities_spin.value())
            cfg['players'] = int(self.players_spin.value())
            cfg['neutral_cities'] = int(self.neutral_cities_spin.value())
            cfg['difficulty'] = int(self.difficulty_spin.value())
            cfg['teams'] = int(self.teams_spin.value())

            # team assignments: list length 8
            team_for_player = []
            for p_idx in range(8):
                try:
                    if p_idx < len(self.team_button_groups):
                        gid = self.team_button_groups[p_idx].checkedId()
                        team_for_player.append(int(gid) if gid is not None and gid >= 0 else 0)
                    else:
                        team_for_player.append(0)
                except Exception:
                    team_for_player.append(0)
            cfg['team_for_player'] = team_for_player

            # Victory / Loss settings
            try:
                vdata = self.victory_combo.currentData()
                cfg['victory'] = vdata.name if hasattr(vdata, 'name') else str(self.victory_combo.currentText())
            except Exception:
                cfg['victory'] = str(self.victory_combo.currentText())
            try:
                ldata = self.loss_combo.currentData()
                cfg['loss'] = ldata.name if hasattr(ldata, 'name') else str(self.loss_combo.currentText())
            except Exception:
                cfg['loss'] = str(self.loss_combo.currentText())

            # victory parameters - only save when a special victory is selected
            try:
                vdata = self.victory_combo.currentData()
            except Exception:
                vdata = None
            if vdata is not None and vdata != VictoryConditions.NORMAL:
                try:
                    art = self.artifact_combo.currentData()
                    cfg['artifact'] = art.name if hasattr(art, 'name') else str(self.artifact_combo.currentText())
                except Exception:
                    cfg['artifact'] = None
                try:
                    cre = self.creature_combo.currentData()
                    cfg['creature'] = cre.name if hasattr(cre, 'name') else str(self.creature_combo.currentText())
                except Exception:
                    cfg['creature'] = None
                try:
                    cfg['creature_count'] = int(self.creature_count_spin.value())
                except Exception:
                    cfg['creature_count'] = None
                try:
                    res = self.resource_combo.currentData()
                    cfg['resource'] = res.name if hasattr(res, 'name') else str(self.resource_combo.currentText())
                except Exception:
                    cfg['resource'] = None
                try:
                    cfg['resource_amount'] = int(self.resource_amount_spin.value())
                except Exception:
                    cfg['resource_amount'] = None
            else:
                cfg['artifact'] = None
                cfg['creature'] = None
                cfg['creature_count'] = None
                cfg['resource'] = None
                cfg['resource_amount'] = None

            # loss params
            try:
                cfg['loss_days'] = int(self.loss_days_combo.currentData() or 0)
            except Exception:
                cfg['loss_days'] = None

            # show save dialog
            default_path = os.path.join(os.getcwd(), 'mapgen_config.json')
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save configuration', default_path, 'JSON files (*.json)')
            if not file_path:
                return
            # ensure extension
            if not file_path.lower().endswith('.json'):
                file_path = file_path + '.json'
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cfg, f, indent=2)
            QMessageBox.information(self, 'Saved', f'Configuration saved to {file_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Save error', f'Failed to save configuration: {e}')

    def on_load_config(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Load configuration', os.getcwd(), 'JSON files (*.json)')
            if not file_path:
                return
            with open(file_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)

            # apply values if present
            try:
                if 'folder' in cfg:
                    self.folder_path_edit.setText(cfg.get('folder') or '')
                if 'filename' in cfg:
                    self.filename_edit.setText(cfg.get('filename') or '')
                if 'map_name' in cfg:
                    self.map_name_edit.setText(cfg.get('map_name') or '')
                if 'map_desc' in cfg:
                    try:
                        self.map_desc_edit.setPlainText(cfg.get('map_desc') or '')
                    except Exception:
                        pass
                if 'size' in cfg:
                    val = cfg.get('size')
                    if val is not None:
                        idx = self.size_combo.findText(val)
                        if idx >= 0:
                            self.size_combo.setCurrentIndex(idx)

                # terrains: reset existing then add from config
                try:
                    # remove existing
                    for t in list(self.terrain_widgets.keys()):
                        try:
                            self._remove_terrain(t)
                        except Exception:
                            pass
                    terr = cfg.get('terrains') or {}
                    for tname, val in terr.items():
                        try:
                            # map name to TerrainType if possible
                            tt = None
                            try:
                                tt = TerrainType[tname]
                            except Exception:
                                tt = None
                            if tt is not None:
                                self._add_terrain(tt)
                                # set value
                                info = self.terrain_widgets.get(tt)
                                if info:
                                    info['spin'].setValue(int(val))
                            else:
                                # fallback: add first available terrain if name unknown
                                pass
                        except Exception:
                            pass
                    # ensure available list updated
                    self._refresh_available_terrains()
                except Exception:
                    pass

                if 'player_cities' in cfg:
                    try:
                        v = int(cfg.get('player_cities') or 1)
                        # clamp to allowed range 1..8
                        v = max(1, min(8, v))
                        self.player_cities_spin.setValue(v)
                    except Exception:
                        pass
                if 'players' in cfg:
                    try:
                        v = int(cfg.get('players') or 1)
                        # clamp to allowed range 1..8
                        v = max(1, min(8, v))
                        self.players_spin.setValue(v)
                    except Exception:
                        pass
                if 'neutral_cities' in cfg:
                    try:
                        # clamp neutral to allowed total (MAX_TOTAL_TOWNS - 1 - player_cities)
                        try:
                            pc = int(self.player_cities_spin.value())
                        except Exception:
                            pc = 0
                        allowed = max(0, MAX_TOTAL_TOWNS - 1 - pc)
                        nv = int(cfg.get('neutral_cities') or 0)
                        nv = max(0, min(allowed, nv))
                        self.neutral_cities_spin.setValue(nv)
                        try:
                            self.neutral_cities_spin.setMaximum(allowed)
                        except Exception:
                            pass
                    except Exception:
                        pass
                if 'difficulty' in cfg:
                    try:
                        self.difficulty_spin.setValue(int(cfg.get('difficulty') or 0))
                    except Exception:
                        pass
                if 'teams' in cfg:
                    try:
                        self.teams_spin.setValue(int(cfg.get('teams') or 0))
                    except Exception:
                        pass

                # apply team assignments
                try:
                    tfp = cfg.get('team_for_player') or []
                    # ensure grid rebuilt
                    self._rebuild_teams_grid()
                    players_active = int(self.players_spin.value())
                    num_teams_active = int(self.teams_spin.value())
                    for p_idx in range(min(8, len(tfp))):
                        try:
                            # only apply assignments for active players
                            if p_idx >= players_active:
                                continue
                            gid = int(tfp[p_idx])
                            # only apply if teams are enabled and gid within range
                            if num_teams_active <= 0:
                                continue
                            if gid < 0 or gid >= num_teams_active:
                                continue
                            if p_idx < len(self.team_radio_buttons):
                                row = self.team_radio_buttons[p_idx]
                                if gid >= 0 and gid < len(row) and row[gid].isEnabled():
                                    row[gid].setChecked(True)
                        except Exception:
                            pass
                except Exception:
                    pass

                # victory / loss
                try:
                    if 'victory' in cfg and cfg.get('victory'):
                        vname = cfg.get('victory')
                        # try match by enum name
                        try:
                            found_idx = -1
                            for i in range(self.victory_combo.count()):
                                data = self.victory_combo.itemData(i)
                                name = data.name if hasattr(data, 'name') else None
                                if name == vname or self.victory_combo.itemText(i) == vname:
                                    found_idx = i
                                    break
                            if found_idx >= 0:
                                self.victory_combo.setCurrentIndex(found_idx)
                        except Exception:
                            pass
                except Exception:
                    pass

                try:
                    if 'loss' in cfg and cfg.get('loss'):
                        lname = cfg.get('loss')
                        found_idx = -1
                        for i in range(self.loss_combo.count()):
                            data = self.loss_combo.itemData(i)
                            name = data.name if hasattr(data, 'name') else None
                            if name == lname or self.loss_combo.itemText(i) == lname:
                                found_idx = i
                                break
                        if found_idx >= 0:
                            self.loss_combo.setCurrentIndex(found_idx)
                        # loss days
                        try:
                            if 'loss_days' in cfg and cfg.get('loss_days') is not None:
                                days = int(cfg.get('loss_days'))
                                idx = self.loss_days_combo.findData(days)
                                if idx >= 0:
                                    self.loss_days_combo.setCurrentIndex(idx)
                        except Exception:
                            pass
                except Exception:
                    pass

            except Exception:
                pass
            # refresh size/players warning after loading config
            try:
                self._update_size_players_warning()
            except Exception:
                pass
            QMessageBox.information(self, 'Loaded', f'Configuration loaded from {file_path}. If any field was invalid, it was set to a default value.')
        except Exception as e:
            QMessageBox.critical(self, 'Load error', f'Failed to load configuration: {e}')

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

        # color square that matches preview colors for this terrain
        def _rgb_for_terrain(t):
            try:
                v = t.value
            except Exception:
                try:
                    v = int(t)
                except Exception:
                    v = 0
            color_map = {
                0: (153, 102, 51),   # DIRT
                1: (201, 152, 88),  # SAND
                2: (12, 186, 12),    # GRASS
                3: (240, 240, 240),  # SNOW
                4: (55, 69, 31),    # SWAMP
                5: (128, 128, 128),  # ROUGH
                6: (0, 0, 0),        # SUBTERRANEAN
                7: (64, 64, 64),     # LAVA
                8: (28, 107, 160),   # WATER
                9: (0, 0, 0),        # ROCK
            }
            return color_map.get(v, (192, 192, 192))

        color_label = QLabel()
        color_label.setFixedSize(18, 12)
        r, g, b = _rgb_for_terrain(terrain)
        # subtle border so square is visible on light backgrounds
        color_label.setStyleSheet(f"background-color: rgb({r},{g},{b}); border: 1px solid #444;")
        hl.addWidget(color_label)

        label = QLabel(terrain.name)
        spin = QSpinBox()
        spin.setRange(1, 5)
        spin.setValue(1)
        # Make text selection in the spinbox's editor transparent so selection
        # doesn't show a solid highlight over the terrain value field.
        try:
            le = None
            try:
                le = spin.lineEdit()
            except Exception:
                le = None
            # Ensure selected text remains visible: transparent selection background
            # but explicit selection color (black) so the digits don't disappear.
            style = (
                "selection-background-color: rgba(0,0,0,0);"
                "selection-color: rgba(0,0,0,1);"
            )
            if le is not None:
                le.setStyleSheet(style)
            else:
                # Fallback: apply stylesheet to the spinbox targeting its QLineEdit
                spin.setStyleSheet(f"QSpinBox QLineEdit {{ {style} }}")
        except Exception:
            pass
        remove_btn = QPushButton("Remove")
        remove_btn.setCursor(QtCore.Qt.PointingHandCursor)

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
                w_str, rest = size_text.split('x')
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
                elif v_choice == VictoryConditions.TRANSPORT_ARTIFACT:
                    # Transport artifact needs an artifact selected before generation
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
                    # loss_days_combo stores the corresponding days as item data
                    data = self.loss_days_combo.currentData()
                    try:
                        lc_params.days = int(data)
                    except Exception:
                        # fallback: if data missing, default to 6 days
                        lc_params.days = 6

                # Informational guidance is shown inline in the Victory/Loss groups
                # (handled by the change handlers) so do not pop up messages here.
                pass

            map, towns_gen, heroes_gen, monsters_gen = generate_voronoi_map(
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
                # store towns and players count so saved BMP can draw neutral towns
                try:
                    self._last_map_towns = towns_gen or []
                except Exception:
                    self._last_map_towns = []
                try:
                    self._last_players_count = int(self.players_spin.value())
                except Exception:
                    self._last_players_count = 0
                # build and display preview image
                tile_px = max(1, 300 // max(width, height))
                qimg = self._build_preview_qimage(self._last_map, width, height, tile_px, neutral_towns=(towns_gen[players_count:] if towns_gen else []))
                pix = QPixmap.fromImage(qimg)
                self.preview_label.setPixmap(pix.scaled(self.preview_label.size(), QtCore.Qt.KeepAspectRatio))
                # clear placeholder styling
                self.preview_label.setStyleSheet("")
                self.preview_label.setText("")
                # If victory condition requires a town, prompt the user to pick one
                try:
                    town_required = {
                        VictoryConditions.BUILD_GRAIL,
                        VictoryConditions.TRANSPORT_ARTIFACT,
                        VictoryConditions.UPGRADE_TOWN,
                        VictoryConditions.CAPTURE_TOWN,
                        VictoryConditions.DEFEAT_HERO,
                        VictoryConditions.DEFEAT_MONSTER,
                    }
                    if v_choice in town_required:
                        # Determine whether we are selecting a town or a hero
                        if v_choice == VictoryConditions.DEFEAT_HERO:
                            entries = heroes_gen
                        elif v_choice == VictoryConditions.DEFEAT_MONSTER:
                            entries = monsters_gen
                        else:
                            entries = towns_gen

                        if not entries:
                            QMessageBox.warning(self, "No entries", "No towns or heroes were found to select from.")
                        else:
                            # Choose dialog type depending on victory choice
                            if v_choice == VictoryConditions.UPGRADE_TOWN:
                                dlg = UpgradeTownDialog(entries, parent=self)
                            elif v_choice == VictoryConditions.CAPTURE_TOWN:
                                dlg = CaptureTownDialog(entries, parent=self)
                            elif v_choice == VictoryConditions.DEFEAT_HERO:
                                dlg = HeroPickerDialog(entries, parent=self)
                            elif v_choice == VictoryConditions.DEFEAT_MONSTER:
                                dlg = DefeatMonsterDialog(entries, parent=self)
                            else:
                                dlg = TownPickerDialog(entries, parent=self)
                                

                            res = dlg.exec()

                            if res == QtWidgets.QDialog.Accepted:
                                sel_idx = dlg.selected_index()
                                if sel_idx is not None and 0 <= sel_idx < len(entries):
                                    item = entries[sel_idx]

                                    # Extract coords defensively depending on representation
                                    try:
                                        if isinstance(item, (list, tuple)):
                                            ix = int(item[0])
                                            iy = int(item[1])
                                            iz = int(item[2])
                                        else:
                                            # object-like entry: try attributes first
                                            try:
                                                ix = int(getattr(item, 'x'))
                                                iy = int(getattr(item, 'y'))
                                                # z may be missing; default to 0
                                                iz = int(getattr(item, 'z', 0))
                                            except Exception:
                                                # try mapping-like access
                                                try:
                                                    ix = int(item[0] if 0 in item else item.get('x'))
                                                    iy = int(item[1] if 1 in item else item.get('y'))
                                                    iz = int(item[2] if 2 in item else item.get('z', 0))
                                                except Exception:
                                                    QMessageBox.warning(self, "Selection error", "Selected entry does not contain usable coordinates.")
                                    except Exception:
                                        QMessageBox.warning(self, "Selection error", "Failed to extract coordinates from the selected entry.")

                                    addinfo = getattr(map, 'additional_info', None)
                                    if addinfo is not None and getattr(addinfo, 'victory_condition', None) is not None:
                                        details = addinfo.victory_condition.details

                                        # If this is hero-defeat detail, create/assign DefeatHero
                                        if v_choice == VictoryConditions.DEFEAT_HERO:
                                            if isinstance(details, DefeatHero):
                                                details.x = ix
                                                details.y = iy
                                                details.z = iz
                                        elif v_choice == VictoryConditions.DEFEAT_MONSTER:
                                            # persist monster-specific details and the allow_normal flag
                                            if isinstance(details, DefeatMonster):
                                                details.x = ix
                                                details.y = iy
                                                details.z = iz
                                            # also persist allow_normal_win from dialog if present
                                            if isinstance(dlg, DefeatMonsterDialog):
                                                addinfo.victory_condition.allow_normal_win = int(bool(dlg.allow_normal_win()))
                                        else:
                                            details.x = ix
                                            details.y = iy
                                            details.z = iz

                                            # If we used the Upgrade dialog, persist the extra params
                                            if isinstance(dlg, UpgradeTownDialog):
                                                addinfo.victory_condition.allow_normal_win = int(bool(dlg.allow_normal_win()))

                                                try:
                                                    hall_enum = HallLevel(dlg.hall_level())
                                                    castle_enum = CastleLevel(dlg.castle_level())
                                                except Exception:
                                                    hall_enum = None
                                                    castle_enum = None

                                                if isinstance(addinfo.victory_condition.details, UpgradeTown):
                                                    det = addinfo.victory_condition.details
                                                    det.x = ix
                                                    det.y = iy
                                                    det.z = iz
                                                    det.hall_level = hall_enum
                                                    det.castle_level = castle_enum
                                            # If we used the Capture dialog, persist the extra params
                                            elif isinstance(dlg, CaptureTownDialog):
                                                addinfo.victory_condition.allow_normal_win = int(bool(dlg.allow_normal_win()))
                                                addinfo.victory_condition.applies_to_computer = int(bool(dlg.applies_to_computer()))
                                                if isinstance(addinfo.victory_condition.details, CaptureTown):
                                                    det = addinfo.victory_condition.details
                                                    det.x = ix
                                                    det.y = iy
                                                    det.z = iz
                            else:
                                # user cancelled town selection
                                choice_msg = QMessageBox(self)
                                choice_msg.setWindowTitle("Town selection cancelled")
                                choice_msg.setText("You cancelled town selection. Do you want to save the JSON only or cancel saving?")
                                save_btn = choice_msg.addButton("Save JSON only", QMessageBox.AcceptRole)
                                cancel_btn = choice_msg.addButton("Cancel saving", QMessageBox.RejectRole)
                                choice_msg.exec()
                                if choice_msg.clickedButton() is cancel_btn:
                                    self.status_label.setText("Cancelled by user")
                                    self.generate_btn.setEnabled(True)
                                    return
                                # otherwise continue and save JSON only (conversion will either fail or be attempted below)
                except Exception:
                    pass
                # After victory selection handling, check loss condition that needs a town
                try:
                    if l_choice == LossConditions.LOSE_TOWN:
                        # prompt user to pick a town for the loss condition
                        if not towns_gen:
                            QMessageBox.warning(self, "No towns", "No towns were found to select from for loss condition.")
                        else:
                            ldlg = TownPickerDialog(towns_gen, parent=self)
                            lres = ldlg.exec()
                            if lres == QtWidgets.QDialog.Accepted:
                                lsel = ldlg.selected_index()
                                if lsel is not None and 0 <= lsel < len(towns_gen):
                                    town_item = towns_gen[lsel]
                                    if isinstance(town_item, (list, tuple)):
                                        ltx = int(town_item[0])
                                        lty = int(town_item[1])
                                        ltz = int(town_item[2])

                                    addinfo = getattr(map, 'additional_info', None)
                                    if addinfo is not None and getattr(addinfo, 'loss_condition', None) is not None:
                                        if isinstance(addinfo.loss_condition.details, LoseTown):
                                            det = addinfo.loss_condition.details
                                            det.x = ltx
                                            det.y = lty
                                            det.z = ltz
                            # handle lose-hero selection similarly
                    elif l_choice == LossConditions.LOSE_HERO:
                        # prompt user to pick a hero for the loss condition
                        if not heroes_gen:
                            QMessageBox.warning(self, "No heroes", "No heroes were found to select from for loss condition.")
                        else:
                            hdlg = HeroPickerDialog(heroes_gen, parent=self)
                            hres = hdlg.exec()
                            if hres == QtWidgets.QDialog.Accepted:
                                hsel = hdlg.selected_index()
                                if hsel is not None and 0 <= hsel < len(heroes_gen):
                                    hero_item = heroes_gen[hsel]
                                    if isinstance(hero_item, (list, tuple)):
                                        htx = int(hero_item[0])
                                        hty = int(hero_item[1])
                                        htz = int(hero_item[2])

                                    addinfo = getattr(map, 'additional_info', None)
                                    if addinfo is not None and getattr(addinfo, 'loss_condition', None) is not None:
                                        if isinstance(addinfo.loss_condition.details, LoseHero):
                                            det = addinfo.loss_condition.details
                                            det.x = htx
                                            det.y = hty
                                            det.z = htz
                            else:
                                # user cancelled loss-town selection: ask whether to continue saving
                                choice_msg = QMessageBox(self)
                                choice_msg.setWindowTitle("Loss-town selection cancelled")
                                choice_msg.setText("You cancelled loss-town selection. Do you want to save the JSON only or cancel saving?")
                                save_btn = choice_msg.addButton("Save JSON only", QMessageBox.AcceptRole)
                                cancel_btn = choice_msg.addButton("Cancel saving", QMessageBox.RejectRole)
                                choice_msg.exec()
                                if choice_msg.clickedButton() is cancel_btn:
                                    self.status_label.setText("Cancelled by user")
                                    self.generate_btn.setEnabled(True)
                                    return
                except Exception:
                    pass
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

        try:
            self.status_label.setText("Converting JSON to h3m...")
            QApplication.processEvents()
            converter = None
            try:
                converter = os.environ.get('H3MTXT_PATH')
            except Exception:
                converter = None
            if not converter:
                try:
                    converter = shutil.which(H3MTXT_NAME)
                except Exception:
                    converter = None
            if not converter:
                try:
                    if os.path.exists(H3MTXT_DEFAULT_PATH):
                        converter = H3MTXT_DEFAULT_PATH
                except Exception:
                    converter = None
            if not converter:
                try:
                    cwd_candidate = os.path.join(os.getcwd(), H3MTXT_NAME)
                    if os.path.exists(cwd_candidate):
                        converter = cwd_candidate
                except Exception:
                    converter = None

            if not converter:
                QMessageBox.information(self, "Saved JSON", f"JSON saved to {json_file_path}. Converter not found; .h3m not created.")
                self.status_label.setText("Saved JSON (no converter)")
            else:
                converter_dir = os.path.dirname(converter) or os.getcwd()
                result = subprocess.run([converter, json_file_path, h3m_file_path], cwd=converter_dir)
                if result.returncode == 0:
                    QMessageBox.information(self, "Success", f"New file created at: {h3m_file_path}")
                    self.status_label.setText("Done")
                    try:
                        print("successfully generated a map using GUI")
                    except Exception:
                        pass
                else:
                    QMessageBox.information(self, "Conversion", f"Conversion finished with code {result.returncode}. JSON saved to {json_file_path}")
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
            # determine neutral towns from last generated towns and players count
            neutral_towns = []
            try:
                towns = getattr(self, '_last_map_towns', []) or []
                pcount = getattr(self, '_last_players_count', 0) or 0
                if towns and pcount is not None:
                    neutral_towns = towns[pcount:]
            except Exception:
                neutral_towns = []

            self._write_preview_bmp(file_path, self._last_map, width, height, tile_px, neutral_towns=neutral_towns)
            QMessageBox.information(self, "Saved", f"Preview saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Preview error", f"Failed to save preview: {e}")

    def _write_preview_bmp(self, path: str, map_obj, width: int, height: int, tile_px: int = 6, neutral_towns=None):
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

        # Overlay player main towns (if present) as small colored squares
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

                # tiles to color: (x-1,y), (x,y), (x+1,y), (x,y+1)
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

    def _build_preview_qimage(self, map_obj, width: int, height: int, tile_px: int = 6, neutral_towns=None) -> QImage:
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


        # print("Overlaying player main towns...")
        # Paint player main towns on top of generated image
        player_towns = 0
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
                    #city_x = int(mt.x + 2)
                    city_x = int(mt.x)
                    city_y = int(mt.y)
                except Exception:
                    continue

                #print("Overlaying main town for player", p_idx+1, "at", city_x, city_y)

                tile_coords = [
                    (city_x - 1, city_y),
                    (city_x, city_y),
                    (city_x + 1, city_y),
                    (city_x, city_y - 1),
                ]

                color = player_colors[p_idx] if p_idx < len(player_colors) else QColor(0, 0, 0)
                # draw filled tiles for town without outlining borders
                painter.setPen(QtCore.Qt.NoPen)
                for tx, ty in tile_coords:
                    if tx < 0 or tx >= width or ty < 0 or ty >= height:
                        continue
                    x_px = int(tx * tile_px)
                    y_px = int(ty * tile_px)
                    rect = QtCore.QRect(x_px, y_px, int(tile_px), int(tile_px))
                    painter.fillRect(rect, color)
                player_towns += 1
            painter.end()
        except Exception:
            # if overlay fails, return base image
            pass

        if neutral_towns:
            # print("Overlaying neutral towns...")
            # Overlay generated towns like player towns but in gray
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

                    # print("Overlaying neutral town at", tx, ty)

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
        # print how many players' towns were drawn
        print(f"Drew {player_towns} player towns on preview.")
        # print how many neutral towns were drawn
        print(f"Drew {len(neutral_towns)} neutral towns on preview.")
        return qimg

    def _update_size_players_warning(self):
        """Show a suggestion when map size 36x36 is selected."""
        try:
            size_text = self.size_combo.currentText() if hasattr(self, 'size_combo') else ''
            # show when 36x36 specifically selected
            try:
                is_small = '36x36' in size_text
            except Exception:
                is_small = False

            if is_small:
                msg = "Small map selected (36x36). Recommended amount of players: 4 or fewer - otherwise the generator may not be able to place all player towns (Voronoi diagram centroids), causing an error."
                try:
                    self.size_warning_label.setText(msg)
                    self.size_warning_label.setVisible(True)
                except Exception:
                    pass
            else:
                try:
                    self.size_warning_label.setVisible(False)
                except Exception:
                    pass
        except Exception:
            try:
                self.size_warning_label.setVisible(False)
            except Exception:
                pass

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

        # Try running the external converter if available. Resolution order:
        # 1. Environment variable `H3MTXT_PATH`
        # 2. System PATH via shutil.which
        # 3. Project-root location (one level above this file)
        # 4. Current working directory
        converter = None
        try:
            converter = os.environ.get('H3MTXT_PATH')
        except Exception:
            converter = None
        if not converter:
            try:
                converter = shutil.which(H3MTXT_NAME)
            except Exception:
                converter = None
        if not converter:
            try:
                if os.path.exists(H3MTXT_DEFAULT_PATH):
                    converter = H3MTXT_DEFAULT_PATH
            except Exception:
                converter = None
        if not converter:
            try:
                cwd_candidate = os.path.join(os.getcwd(), H3MTXT_NAME)
                if os.path.exists(cwd_candidate):
                    converter = cwd_candidate
            except Exception:
                converter = None

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


class TownPickerDialog(QtWidgets.QDialog):
    """Dialog to let the user pick one town from the generated towns list.

    Supports towns represented either as Objects (with attributes x,y,z and optional properties.name)
    or as simple tuples/lists (x,y,z). The dialog presents a readable label per entry and returns
    the selected index via `selected_index()`.
    """
    def __init__(self, towns: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select town")
        self.setModal(True)
        self._towns = towns
        self._selected = None

        layout = QVBoxLayout()
        self.list = QtWidgets.QListWidget()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # determine how many player towns to color, based on parent UI if available
        try:
            parent = self.parent()
            players_count = int(parent.players_spin.value()) if parent is not None else 0
        except Exception:
            players_count = 0
        player_colors = ['red', 'blue', 'tan', 'green', 'orange', 'purple', 'teal', 'pink']
        for i, t in enumerate(self._towns):
            label = f"Town #{i+1}"
            # tuple/list case
            if isinstance(t, (list, tuple)):
                tx = t[0] if len(t) > 0 else None
                ty = t[1] if len(t) > 1 else None
                tz = t[2] if len(t) > 2 else None
                # show coordinates when available
                if tx is not None and ty is not None:
                    label = f"Town #{i+1} — ({tx}, {ty}, {tz})"
            item = QtWidgets.QListWidgetItem(label)
            try:
                if i < players_count:
                    col = player_colors[i] if i < len(player_colors) else 'black'
                    item.setForeground(QColor(col))
                else:
                    item.setForeground(QColor('black'))
            except Exception:
                pass
            self.list.addItem(item)

        layout.addWidget(QLabel("Choose the town that should be used for the victory condition:"))
        layout.addWidget(self.list)

        btn_h = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(self._on_ok)
        cancel.clicked.connect(self.reject)
        btn_h.addStretch()
        btn_h.addWidget(ok)
        btn_h.addWidget(cancel)

        layout.addLayout(btn_h)
        self.setLayout(layout)

        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    def _on_ok(self):
        row = self.list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No selection", "Please select a town or Cancel.")
            return
        self._selected = row
        self.accept()

    def selected_index(self):
        return self._selected


class UpgradeTownDialog(QtWidgets.QDialog):
    """Dialog for configuring the Upgrade Town victory condition.

    Shows a town list (same behaviour as TownPickerDialog) plus:
    - checkbox to allow normal victory (`allow_normal_win` -> 0/1)
    - Hall level choice: Town(0), City(1), Capitol(2)
    - Castle level choice: Fort(0), Citadel(1), Castle(2)
    """
    def __init__(self, towns: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Upgrade Town - parameters")
        self.setModal(True)
        self._towns = towns or []
        self._selected = None

        layout = QVBoxLayout()

        # allow normal victory checkbox
        self.allow_normal_cb = QtWidgets.QCheckBox("Also allow normal victory")
        layout.addWidget(self.allow_normal_cb)

        # town list
        layout.addWidget(QLabel("Choose town to upgrade:"))
        self.list = QtWidgets.QListWidget()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # color player towns similarly
        try:
            parent = self.parent()
            players_count = int(parent.players_spin.value()) if parent is not None else 0
        except Exception:
            players_count = 0
        player_colors = ['red', 'blue', 'tan', 'green', 'orange', 'purple', 'teal', 'pink']
        for i, t in enumerate(self._towns):
            label = f"Town #{i+1}"
            try:
                if isinstance(t, (list, tuple)):
                    tx = t[0] if len(t) > 0 else None
                    ty = t[1] if len(t) > 1 else None
                    if tx is not None and ty is not None:
                        label = f"Town #{i+1}, at ({tx}, {ty})"
                else:
                    name = getattr(getattr(t, 'properties', None), 'name', None)
                    tx = getattr(t, 'x', None)
                    ty = getattr(t, 'y', None)
                    if name:
                        label = f"#{i+1} {name}"
                        if tx is not None and ty is not None:
                            label += f" — ({tx}, {ty})"
                    else:
                        if tx is not None and ty is not None:
                            label = f"Town #{i+1} — ({tx}, {ty})"
            except Exception:
                label = f"Town #{i+1}"
            item = QtWidgets.QListWidgetItem(label)
            try:
                if i < players_count:
                    col = player_colors[i] if i < len(player_colors) else 'black'
                    item.setForeground(QColor(col))
                else:
                    item.setForeground(QColor('black'))
            except Exception:
                pass
            self.list.addItem(item)
        layout.addWidget(self.list)

        # Hall / Castle combos
        form = QFormLayout()
        self.hall_combo = QComboBox()
        self.hall_combo.addItems(["Town", "City", "Capitol"])  # 0,1,2
        self.castle_combo = QComboBox()
        self.castle_combo.addItems(["Fort", "Citadel", "Castle"])  # 0,1,2
        form.addRow(QLabel("Hall level:"), self.hall_combo)
        form.addRow(QLabel("Castle level:"), self.castle_combo)
        layout.addLayout(form)

        # buttons
        btn_h = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(self._on_ok)
        cancel.clicked.connect(self.reject)
        btn_h.addStretch()
        btn_h.addWidget(ok)
        btn_h.addWidget(cancel)
        layout.addLayout(btn_h)

        self.setLayout(layout)
        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    def _on_ok(self):
        row = self.list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No selection", "Please select a town or Cancel.")
            return
        self._selected = row
        self.accept()

    def selected_index(self):
        return self._selected

    def allow_normal_win(self):
        return 1 if self.allow_normal_cb.isChecked() else 0

    def hall_level(self):
        return int(self.hall_combo.currentIndex())

    def castle_level(self):
        return int(self.castle_combo.currentIndex())


class CaptureTownDialog(QtWidgets.QDialog):
    """Dialog for configuring the Capture Town victory condition.

    Shows two checkboxes (allow normal victory, applies to computer) and a town list.
    """
    def __init__(self, towns: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Capture Town - parameters")
        self.setModal(True)
        self._towns = towns or []
        self._selected = None

        layout = QVBoxLayout()

        # allow normal victory checkbox
        self.allow_normal_cb = QtWidgets.QCheckBox("Also allow normal victory")
        layout.addWidget(self.allow_normal_cb)

        # applies to computer checkbox
        self.applies_cb = QtWidgets.QCheckBox("Special victory condition also applies to computer opponents")
        layout.addWidget(self.applies_cb)

        # town list
        layout.addWidget(QLabel("Choose town to capture:"))
        self.list = QtWidgets.QListWidget()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        try:
            parent = self.parent()
            players_count = int(parent.players_spin.value()) if parent is not None else 0
        except Exception:
            players_count = 0
        player_colors = ['red', 'blue', 'tan', 'green', 'orange', 'purple', 'teal', 'pink']
        for i, t in enumerate(self._towns):
            label = f"Town #{i+1}"
            try:
                if isinstance(t, (list, tuple)):
                    tx = t[0] if len(t) > 0 else None
                    ty = t[1] if len(t) > 1 else None
                    if tx is not None and ty is not None:
                        label = f"Town #{i+1}, at ({tx}, {ty})"
                else:
                    name = getattr(getattr(t, 'properties', None), 'name', None)
                    tx = getattr(t, 'x', None)
                    ty = getattr(t, 'y', None)
                    if name:
                        label = f"#{i+1} {name}"
                        if tx is not None and ty is not None:
                            label += f" — ({tx}, {ty})"
                    else:
                        if tx is not None and ty is not None:
                            label = f"Town #{i+1} — ({tx}, {ty})"
            except Exception:
                label = f"Town #{i+1}"
            item = QtWidgets.QListWidgetItem(label)
            try:
                if i < players_count:
                    col = player_colors[i] if i < len(player_colors) else 'black'
                    item.setForeground(QColor(col))
                else:
                    item.setForeground(QColor('black'))
            except Exception:
                pass
            self.list.addItem(item)
        layout.addWidget(self.list)

        # buttons
        btn_h = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(self._on_ok)
        cancel.clicked.connect(self.reject)
        btn_h.addStretch()
        btn_h.addWidget(ok)
        btn_h.addWidget(cancel)
        layout.addLayout(btn_h)

        self.setLayout(layout)
        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    def _on_ok(self):
        row = self.list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No selection", "Please select a town or Cancel.")
            return
        self._selected = row
        self.accept()

    def selected_index(self):
        return self._selected

    def allow_normal_win(self):
        return 1 if self.allow_normal_cb.isChecked() else 0

    def applies_to_computer(self):
        return 1 if self.applies_cb.isChecked() else 0


class DefeatMonsterDialog(QtWidgets.QDialog):
    """Dialog for configuring the Defeat Monster victory condition.

    Shows a checkbox to allow normal victory and a list of generated monsters
    (monsters_gen is a list of tuples (x,y,z)).
    """
    def __init__(self, monsters: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Defeat Monster - parameters")
        self.setModal(True)
        self._monsters = monsters or []
        self._selected = None

        layout = QVBoxLayout()

        # allow normal victory checkbox
        self.allow_normal_cb = QtWidgets.QCheckBox("Also allow normal victory")
        layout.addWidget(self.allow_normal_cb)

        # monster list
        layout.addWidget(QLabel("Choose monster to defeat:"))
        self.list = QtWidgets.QListWidget()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        for i, m in enumerate(self._monsters):
            label = f"Monster #{i+1}"
            try:
                if isinstance(m, (list, tuple)):
                    mx = m[0] if len(m) > 0 else None
                    my = m[1] if len(m) > 1 else None
                    mz = m[2] if len(m) > 2 else None
                    if mx is not None and my is not None:
                        label = f"Monster #{i+1}, at ({mx}, {my}, {mz})"
                else:
                    mx = getattr(m, 'x', None)
                    my = getattr(m, 'y', None)
                    if mx is not None and my is not None:
                        label = f"Monster #{i+1} — ({mx}, {my})"
            except Exception:
                label = f"Monster #{i+1}"
            self.list.addItem(label)
        layout.addWidget(self.list)

        # buttons
        btn_h = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(self._on_ok)
        cancel.clicked.connect(self.reject)
        btn_h.addStretch()
        btn_h.addWidget(ok)
        btn_h.addWidget(cancel)
        layout.addLayout(btn_h)

        self.setLayout(layout)
        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    def _on_ok(self):
        row = self.list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No selection", "Please select a monster or Cancel.")
            return
        self._selected = row
        self.accept()

    def selected_index(self):
        return self._selected

    def allow_normal_win(self):
        return 1 if self.allow_normal_cb.isChecked() else 0


class HeroPickerDialog(QtWidgets.QDialog):
    """Dialog to let the user pick one hero from the generated heroes list.

    Supports hero represented either as Objects (with attributes x,y,z and optional properties.name or name)
    or as simple tuples/lists (x,y,z). Returns the selected index via `selected_index()`.
    """
    def __init__(self, heroes: list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select hero")
        self.setModal(True)
        self._heroes = heroes or []
        self._selected = None

        layout = QVBoxLayout()
        self.list = QtWidgets.QListWidget()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        for i, h in enumerate(self._heroes):
            label = f"Hero #{i+1}"
            try:
                if isinstance(h, (list, tuple)):
                    hx = h[0] if len(h) > 0 else None
                    hy = h[1] if len(h) > 1 else None
                    hz = h[2] if len(h) > 2 else None
                    if hx is not None and hy is not None:
                        label = f"Hero #{i+1}, at ({hx}, {hy}, {hz})"
                else:
                    name = getattr(h, 'name', None) or getattr(getattr(h, 'properties', None), 'name', None)
                    hx = getattr(h, 'x', None)
                    hy = getattr(h, 'y', None)
                    if name:
                        label = f"#{i+1} {name}"
                        if hx is not None and hy is not None:
                            label += f" — ({hx}, {hy})"
                    else:
                        if hx is not None and hy is not None:
                            label = f"Hero #{i+1} ({hx}, {hy})"
            except Exception:
                label = f"Hero #{i+1}"
            # color player-owned heroes by index (first N entries -> players)
            try:
                parent = self.parent()
                players_count = int(parent.players_spin.value()) if parent is not None else 0
            except Exception:
                players_count = 0
            player_colors = ['red', 'blue', 'tan', 'green', 'orange', 'purple', 'teal', 'pink']
            item = QtWidgets.QListWidgetItem(label)
            try:
                if i < players_count:
                    col = player_colors[i] if i < len(player_colors) else 'black'
                    item.setForeground(QColor(col))
                else:
                    item.setForeground(QColor('black'))
            except Exception:
                pass
            self.list.addItem(item)

        layout.addWidget(QLabel("Choose the hero that should be used for the victory condition:"))
        layout.addWidget(self.list)

        btn_h = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancel")
        ok.clicked.connect(self._on_ok)
        cancel.clicked.connect(self.reject)
        btn_h.addStretch()
        btn_h.addWidget(ok)
        btn_h.addWidget(cancel)

        layout.addLayout(btn_h)
        self.setLayout(layout)

        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    def _on_ok(self):
        row = self.list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No selection", "Please select a hero or Cancel.")
            return
        self._selected = row
        self.accept()

    def selected_index(self):
        return self._selected


def main():
    app = QApplication(sys.argv)
    win = MapGeneratorGUI()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
