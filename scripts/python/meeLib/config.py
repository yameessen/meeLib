"""

*/meeLib.config
    Core functions of the meeLib library

"""

import json
import webbrowser
from pathlib import Path
from urllib.request import urlopen

import hou
from PySide2 import QtCore, QtWidgets
from PySide2.QtGui import QIcon, QPixmap

from .logging import logger

# region GLOBALS
MEELIB_FOLDER = Path(__file__).parent.parent.parent.parent.as_posix()
MEELIB_CFG = (Path(MEELIB_FOLDER) / "config.json").as_posix()


# region MAIN
def open_folder(path):
    if Path(path).exists():
        return hou.ui.showInFileBrowser(path)
    else:
        logger.error("Output dir does not exist")
        return False


# region CONFIG
def get_cfg_data():
    cfg_path = Path(MEELIB_CFG)
    if cfg_path.is_file():
        with cfg_path.open("r") as file:
            return json.load(file)
    else:
        logger.error("Config file not found.")
        return None


def write_cfg_data(cfg):
    cfg_path = Path(MEELIB_CFG)
    if cfg_path.is_file() and isinstance(cfg, dict):
        with cfg_path.open("w") as file:
            json.dump(cfg, file, indent=4)
            return True
    else:
        logger.error("Unable to write Config file.")
        return False


# region INTERNALS
def has_nodeinternal_folder(node):
    return node.parm("meeLib_nodeinternals") is not None


def show_nodeinternal_folder(node):
    nodeinternals_parm = node.parm("meeLib_nodeinternals")
    current_value = nodeinternals_parm.evalAsInt()
    nodeinternals_parm.set(0 if current_value == 1 else 1)


# region ABOUTS
def display_abouts():

    cfg = get_cfg_data()
    if not cfg:
        return

    abouts_dict = cfg.get("abouts", {})

    dialog = QtWidgets.QDialog(hou.ui.mainQtWindow())
    dialog.setWindowTitle("À propos de meeLib")
    dialog.setMinimumWidth(600)

    layout = QtWidgets.QVBoxLayout(dialog)
    layout.setSpacing(15)

    style = """
        QLabel {
            font-size: 12px;
            color: #e0e0e0;
        }
        QFrame {
            background: #232323;
            border-radius: 8px;
        }
    """
    dialog.setStyleSheet(style)

    icon_map = {
        "github": "https://cdn-icons-png.flaticon.com/512/733/733553.png",
        "linkedin": "https://cdn-icons-png.flaticon.com/512/174/174857.png",
        "onlyfans": "https://img.icons8.com/?size=100&id=i2VgeyEtUTLt&format=png&color=000000",
    }

    for key, value in abouts_dict.items():
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setStyleSheet("background: #232323;")

        hbox = QtWidgets.QHBoxLayout(frame)
        hbox.setContentsMargins(20, 10, 5, 10)

        key_label = QtWidgets.QLabel(key.capitalize())
        key_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        key_label.setStyleSheet("font-weight: bold; font-size: 18px; color: #ffb347;")
        hbox.addWidget(key_label, 1)

        if key == "socials":
            icons_layout = QtWidgets.QHBoxLayout()
            icons_layout.addStretch()  # Push icons to the right

            for subkey, url in value.items():
                btn = QtWidgets.QPushButton()
                btn.setCursor(QtCore.Qt.PointingHandCursor)

                icon_path = icon_map.get(subkey.lower())

                try:
                    data = urlopen(icon_path).read()
                    pixmap = QPixmap()
                    pixmap.loadFromData(data)
                    btn.setIcon(QIcon(pixmap))
                    btn.setIconSize(QtCore.QSize(28, 28))
                    btn.setToolTip(subkey.capitalize())
                except Exception:
                    btn.setText(subkey.capitalize())

                btn.setStyleSheet("background: transparent; border: none;")
                btn.clicked.connect(lambda checked=False, link=url: webbrowser.open(link))
                icons_layout.addWidget(btn)

            hbox.addLayout(icons_layout, 3)
        else:
            value_label = QtWidgets.QLabel(str(value))
            value_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            value_label.setWordWrap(True)
            value_label.setStyleSheet("font-size: 13px; color: #e0e0e0;")
            hbox.addWidget(value_label, 3)

        layout.addWidget(frame)

    dialog.exec_()
