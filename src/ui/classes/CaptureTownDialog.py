from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QListWidget, QLabel, QAbstractItemView, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QColor

class CaptureTownDialog(QDialog):
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
        self.allow_normal_cb = QCheckBox("Also allow normal victory")
        layout.addWidget(self.allow_normal_cb)

        # applies to computer checkbox
        self.applies_cb = QCheckBox("Special victory condition also applies to computer opponents")
        layout.addWidget(self.applies_cb)

        # town list
        layout.addWidget(QLabel("Choose town to capture:"))
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
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
