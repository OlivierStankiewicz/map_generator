from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QListWidget, QLabel, QAbstractItemView, QHBoxLayout, QPushButton, QMessageBox

class DefeatMonsterDialog(QDialog):
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
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
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