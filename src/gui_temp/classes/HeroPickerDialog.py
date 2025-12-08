from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel, QAbstractItemView, QHBoxLayout, QPushButton, QMessageBox, QListWidgetItem
from PySide6.QtGui import QColor

class HeroPickerDialog(QDialog):
    """Dialog to let the user pick one hero from the generated heroes list.

    Supports hero represented either as Objects (with attributes x,y,z and optional properties.name or name)
    or as simple tuples/lists (x,y,z). Returns the selected index via `selected_index()`.
    """
    def __init__(self, heroes: list, parent=None, type=None):
        super().__init__(parent)
        self.setWindowTitle("Select hero")
        self.setModal(True)
        self._heroes = heroes or []
        self._selected = None
        self._type = type

        layout = QVBoxLayout()
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)

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
            item = QListWidgetItem(label)
            try:
                if i < players_count:
                    col = player_colors[i] if i < len(player_colors) else 'black'
                    item.setForeground(QColor(col))
                else:
                    item.setForeground(QColor('black'))
            except Exception:
                pass
            self.list.addItem(item)

        if self._type == 'victory':
            layout.addWidget(QLabel("Choose the hero that should be used for the victory condition:"))
        elif self._type == 'loss':
            layout.addWidget(QLabel("Choose the hero that should be used for the loss condition:"))
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