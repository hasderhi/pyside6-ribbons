
import os
import sys


from PySide6.QtCore import (
    Qt, QSize
)
from PySide6.QtGui import (
    QColor, QIcon, QPixmap, QPainter
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTabBar, QStackedWidget, QToolButton, 
    QSizePolicy, QLabel, QGridLayout, QLabel
)

ICON_MAPPING = {
    "Save": "save.png",
    "Save as": "file-symlink.png",
    "Open": "folder-open.png",
    "New": "file-plus.png",

    "Title": "type.png",
    "Heading": "heading.png",
}


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)






def get_white_icon(icon_path):
    pixmap = QPixmap(icon_path)
    if pixmap.isNull():
        return QIcon()

    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor("#FFFFFF"))
    painter.end()
    
    return QIcon(pixmap)






class RibbonGroup(QWidget):
    def __init__(self, title, buttons, parent=None):
        super().__init__(parent)
        self.buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 4)
        layout.setSpacing(4)

        grid = QGridLayout()
        grid.setContentsMargins(2, 2, 2, 2)
        grid.setHorizontalSpacing(4)
        grid.setVerticalSpacing(4)

        for row, row_buttons in enumerate(buttons):
            for col, text in enumerate(row_buttons):
                if text:
                    btn = QToolButton()
                    btn.setText(text)
                    
                    icon_name = ICON_MAPPING.get(text)
                    if icon_name:
                        icon_path = resource_path(f"res/icons/{icon_name}")
                        white_icon = get_white_icon(icon_path)
                        btn.setIcon(white_icon)
                        btn.setIconSize(QSize(14, 14))
                        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
                    else:
                        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)

                    btn.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
                    btn.setMinimumWidth(90)
                    btn.setMinimumHeight(26)

                    grid.addWidget(btn, row, col)
                    self.buttons[text] = btn

        layout.addLayout(grid)

        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("GroupTitle")
        layout.addWidget(label)

        self.init_stylesheet()

    def init_stylesheet(self):
        self.setStyleSheet("""
            RibbonGroup {
                background-color: #252526;
                border: 1px solid #3E3E3E;
                border-radius: 6px;
            }
            QToolButton {
                background-color: #2D2D30; 
                color: #E0E0E0;
                font-size: 11px;
                border: 1px solid #404040;
                border-radius: 4px;
                padding: 4px 8px;

                qproperty-toolButtonStyle: ToolButtonTextBesideIcon; 
                spacing: 6px; 
            }
            QToolButton:hover {
                background-color: #3E3E42;
                border-color: #555555;
                color: #FFFFFF;
            }
            QToolButton:pressed {
                background-color: #00da49;
                border-color: #008f30;
                color: #FFFFFF;
            }
            QLabel#GroupTitle {
                font-size: 10px;
                font-weight: bold;
                color: #858585;
                background: transparent;
                text-transform: uppercase;
                margin-top: 4px;
            }
        """)


class RibbonMenu(QWidget):
    def __init__(self, file_ops, insert_ops, parent=None):
        super().__init__(parent)

        self.file_ops = file_ops
        self.insert_ops = insert_ops

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_bar = QTabBar()
        for tab_name in ["Home", "Insert"]:
            self.tab_bar.addTab(tab_name)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setDrawBase(False)
        layout.addWidget(self.tab_bar)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.home_tab = self.make_home_tab()
        self.insert_tab = self.make_insert_tab()

        self.stack.addWidget(self.home_tab)
        self.stack.addWidget(self.insert_tab)

        self.tab_bar.currentChanged.connect(self.stack.setCurrentIndex)
        self.init_global_stylesheet()

    def init_global_stylesheet(self):
        self.setStyleSheet("""
            QTabBar {
                background-color: #1E1E1E;
                qproperty-drawBase: 0;
            }
            QTabBar::tab {
                padding: 6px 20px;
                background-color: #1E1E1E;
                color: #969696;
                font-size: 12px;
                font-weight: 500;
                border: none;
                border-bottom: 2px solid transparent;
            }
            QTabBar::tab:hover {
                color: #E0E0E0;
                background-color: #2D2D2D;
            }
            QTabBar::tab:selected {
                color: #FFFFFF;
                background-color: #2B2B2B;
                border-bottom: 2px solid #008f30;
            }
            QWidget#RibbonContent {
                background-color: #272626;
                border-top: 1px solid #2D2D2D;
            }
        """)

    def make_home_tab(self):
        tab = QWidget()
        tab.setObjectName("RibbonContent")

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 8)
        layout.setSpacing(10)

        file_group = RibbonGroup("File", [
            ["Save", "Save as"],
            ["Open", "New"]
        ])

        # file_group.buttons["Save"].clicked.connect(self.file_ops["save"])
        # file_group.buttons["Save as"].clicked.connect(self.file_ops["save_as"])
        # file_group.buttons["Open"].clicked.connect(self.file_ops["open"])
        # file_group.buttons["New"].clicked.connect(self.file_ops["new"])

        layout.addWidget(file_group)
        layout.addStretch()
        return tab

    def make_insert_tab(self):
        tab = QWidget()
        tab.setObjectName("RibbonContent")

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 8)
        layout.setSpacing(10)

        insert_group = RibbonGroup("Insert", [
            ["Title"],
            ["Heading"],
        ])

        # insert_group.buttons["Title"].clicked.connect(self.insert_ops["title"])
        # insert_group.buttons["Heading"].clicked.connect(self.insert_ops["heading"])

        layout.addWidget(insert_group)
        layout.addStretch()
        return tab






# Main
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("annaScript Studio")
        self.resize(1400, 900)
        self.setMinimumSize(900, 300)


        file_ops = {
            "save": print("hi"),
            "save_as": print("hi"),
        }
        insert_ops = {
            "title": lambda: print("hi"),
            "heading": lambda: print("hi"),
        }

        self.ribbon = RibbonMenu(file_ops, insert_ops)
        self.setMenuWidget(self.ribbon)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(container)






# run entry
if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet("""
    QMainWindow, QWidget {
        background-color: #202020;
        color: #ffffff;
    }
    """)
    

    win = MainWindow()
    win.show()
    app.exec()