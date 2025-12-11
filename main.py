from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTabBar, QStackedWidget, QToolButton, QSizePolicy,
    QLabel, QGridLayout, QDialog
)
import sys
import webbrowser
import os

class RibbonGroup(QWidget):
    def __init__(self, title, buttons):
        super().__init__()
        self.buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 2)
        layout.setSpacing(2)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(3)
        grid.setVerticalSpacing(3)

        for row, row_buttons in enumerate(buttons):
            for col, text in enumerate(row_buttons):
                if text:
                    btn = QToolButton()
                    btn.setText(text)
                    btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                    btn.setMinimumWidth(70)
                    btn.setMinimumHeight(28)

                    grid.addWidget(btn, row, col)
                    self.buttons[text] = btn

        layout.addLayout(grid)

        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 10px; color: #ffffff; margin-top: 2px;")
        layout.addWidget(label)

        self.setStyleSheet("""
        RibbonGroup {
            background: #2b2b2b;
            border: 1px solid #444;
        }
        QToolButton {
            background: #3c3c3c;
            color: #eee;
            font-size: 11px;
            border: 1px solid #555;
            padding: 3px 10px;
        }
        QToolButton:hover {
            background: #505050;
        }
        QToolButton:pressed {
            background: #666666;
        }
        """)


class RibbonMenu(QWidget):
    def __init__(self, example_ops, about_ops):
        super().__init__()

        self.example_ops = example_ops
        self.about_ops = about_ops

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_bar = QTabBar()
        for tab_name in ["Example", "About"]:
            self.tab_bar.addTab(tab_name)
        self.tab_bar.setExpanding(False)
        layout.addWidget(self.tab_bar)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.example_tab = self.make_example_tab()
        self.about_tab = self.make_about_tab()

        self.stack.addWidget(self.example_tab)
        self.stack.addWidget(self.about_tab)

        self.tab_bar.currentChanged.connect(self.stack.setCurrentIndex)

        self.setStyleSheet("""
        QTabBar::tab {
            padding: 4px 18px;
            background: #3c3c3c;
            color: #eee;
            
            font-weight: 600;
            font-size: 13px;
            border: none;
            margin-right: 1px;
        }
        QTabBar::tab:selected {
            background: #008f00;
        }
        QTabBar::tab:hover {
            background: #3bb846;
        }
        QWidget#RibbonContent {
            background: #2b2b2b;
        }
        """)

    def make_example_tab(self):
        tab = QWidget()
        tab.setObjectName("RibbonContent")

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 4)
        layout.setSpacing(8)

        example_group = RibbonGroup("Example", [
            ["Greet!"],
            ["About"],
        ])
        

        example_group.buttons["Greet!"].clicked.connect(self.example_ops["greet"])
        example_group.buttons["About"].clicked.connect(self.example_ops["about"])

        layout.addWidget(example_group)
        layout.addStretch()
        return tab
    
    def make_about_tab(self):
        tab = QWidget()
        tab.setObjectName("RibbonContent")

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 4)
        layout.setSpacing(8)

        about_group = RibbonGroup("About", [
            ["Website"],
            ["License"],
        ])
                
        about_group.buttons["Website"].clicked.connect(self.about_ops["website"])
        about_group.buttons["License"].clicked.connect(self.about_ops["license"])

        layout.addWidget(about_group)
        layout.addStretch()
        return tab














class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Ribbon Menu Demonstration Example")
        self.resize(1400, 900)


        example_ops = {
            "about": self.about,
            "greet": self.greet
        }
        about_ops = {
            "website": self.website,
            "license": self.license
        }


        self.ribbon = RibbonMenu(example_ops, about_ops)
        self.setMenuWidget(self.ribbon)




    def website(self):
        webbrowser.open("https://tk-dev-software.com")

    def greet(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Hi!")
        dlg.resize(200, 150)

        layout = QVBoxLayout(dlg)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        try:
            user = os.getlogin()
        except:
            user = ""

        label = QLabel(f"Hi {user}, my name's Annabeth!\nI hope you're having an awesome day :)", dlg)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)



        dlg.exec()

    def license(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("License")
        dlg.resize(400, 300)

        layout = QVBoxLayout(dlg)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)


        title_label = QLabel("License", dlg)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        license_label = QLabel("""
<b>MIT License</b><br><br>

Copyright (c) 2025 <i>Tobias Kisling (Annabeth / tk_dev / hasderhi)</i><br><br>

Permission is hereby granted, free of charge, to any person obtaining a copy<br>
of this software and associated documentation files (the "Software"), to deal<br>
in the Software without restriction, including without limitation the rights<br>
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell<br>
copies of the Software, and to permit persons to whom the Software is furnished<br>
to do so, subject to the following conditions:<br><br>

The above copyright notice and this permission notice shall be included in all<br>
copies or substantial portions of the Software.<br><br>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR<br>
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,<br>
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE<br>
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,<br>
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN<br>
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.<br><br>

<hr><br>

Note on third-party libraries:<br><br>

This application ("PySide6 Ribbon Menu Demonstration Example") uses <b>PySide6</b> (Qt for Python) for its GUI framework. PySide6<br>
is licensed under the <b>LGPLv3</b>, which allows dynamic linking in your application.
""", dlg)
        license_label.setAlignment(Qt.AlignCenter)
        license_label.setTextFormat(Qt.RichText)
        layout.addWidget(license_label)

        dlg.exec()

    def about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About PySide6 Ribbon Menu Demonstration Example")
        dlg.resize(400, 300)

        layout = QVBoxLayout(dlg)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)


        title_label = QLabel("PySide6 Ribbon Menu", dlg)
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel("v1.0.0", dlg)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        dev_label = QLabel("Developed by Annabeth Kisling", dlg)
        dev_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_label)

        website_label = QLabel('<a href="https://tk-dev-software.com">tk-dev-software.com</a>', dlg)
        website_label.setAlignment(Qt.AlignCenter)
        website_label.setTextFormat(Qt.RichText)
        website_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        website_label.setOpenExternalLinks(True)
        website_label.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(website_label)

        github_label = QLabel('<a href="https://github.com/hasderhi">@hasderhi on GitHub</a>', dlg)
        github_label.setAlignment(Qt.AlignCenter)
        github_label.setTextFormat(Qt.RichText)
        github_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        github_label.setOpenExternalLinks(True)
        github_label.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(github_label)

        dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
