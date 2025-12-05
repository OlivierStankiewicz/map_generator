from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem, QLabel, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QColor

class TownPickerDialog(QDialog):
    """Dialog to let the user pick one town from the generated towns list.

    Supports towns represented either as Objects (with attributes x,y,z and optional properties.name)
    or as simple tuples/lists (x,y,z). The dialog presents a readable label per entry and returns
    the selected index via `selected_index()`.
    """
    def __init__(self, towns: list, parent=None, type=None):
        super().__init__(parent)
        self.setWindowTitle("Select town")
        self.setModal(True)
        self._towns = towns
        self._selected = None
        self.type = type

        layout = QVBoxLayout()
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)

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


        victory_condition_town_text = "Choose the town that should be used for the victory condition:"
        loss_condition_town_text = "Choose the town that should be used for the loss condition:"
        if(self.type == 'victory'):
            layout.addWidget(QLabel(victory_condition_town_text))
        elif(self.type == 'loss'):
            layout.addWidget(QLabel(loss_condition_town_text))
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