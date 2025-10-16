from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
import sys
import os
import json
import subprocess
import shutil

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
        # Try an alternate import path if the package is referenced differently
        from src.generation.map_gen.map_gen import generate_voronoi_map
    except Exception:
        # Leave generate_voronoi_map as None; the GUI will show an error if called
        generate_voronoi_map = None

class MapGeneratorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Generator GUI")
        self.resize(480, 150)

        # Widgets
        self.folder_label = QLabel("Save folder:")
        self.folder_path_edit = QLineEdit()
        self.folder_browse_btn = QPushButton("Browse")

        self.filename_label = QLabel("File name (without extension):")
        self.filename_edit = QLineEdit()

        self.generate_btn = QPushButton("Generate map")
        self.status_label = QLabel("")

        # Layout
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path_edit)
        folder_layout.addWidget(self.folder_browse_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.folder_label)
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(self.filename_label)
        main_layout.addWidget(self.filename_edit)
        main_layout.addWidget(self.generate_btn)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Signals
        self.folder_browse_btn.clicked.connect(self.browse_folder)
        self.generate_btn.clicked.connect(self.on_generate)

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

        self.status_label.setText("Generating map representation...")
        QApplication.processEvents()

        if generate_voronoi_map is None:
            QMessageBox.critical(self, "Import error", "Could not import map generator function. Run from project root or adjust imports.")
            self.status_label.setText("Failed: generator not available")
            return

        try:
            map_obj = generate_voronoi_map()
        except Exception as e:
            QMessageBox.critical(self, "Generation error", f"Map generation failed: {e}")
            self.status_label.setText("Failed: generation error")
            return

        try:
            json_map = json.dumps(map_obj.to_dict(), indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Serialize error", f"Failed to serialize map: {e}")
            self.status_label.setText("Failed: serialize error")
            return

        json_file_path = os.path.join(folder, f"{filename}.json")
        h3m_file_path = os.path.join(folder, f"{filename}.h3m")

        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                f.write(json_map)
        except Exception as e:
            QMessageBox.critical(self, "File error", f"Failed to write JSON file: {e}")
            self.status_label.setText("Failed: file write error")
            return

        # Try running the external converter if available.
        # Search order:
        # 1) absolute path on PATH (shutil.which)
        # 2) current working directory
        # 3) project root (one level above this file)
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
                # Run the converter from its directory so it behaves the same regardless of the GUI cwd
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


def main():
    app = QApplication(sys.argv)
    win = MapGeneratorGUI()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
