"""
Mini Left-Side Browser Panel  (PyQt5 + QtWebEngine)
=====================================================
Full Chromium engine — JavaScript works on ALL websites (Facebook, Instagram, etc.)

Install requirements:
    pip install PyQt5 PyQtWebEngine

Run:
    python mini_browser.py
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtGui import QFont, QCursor


# ─── CONFIG ──────────────────────────────────────────────────────────────────
START_URL      = "https://www.google.com"
WINDOW_WIDTH   = 370
WINDOW_HEIGHT  = 800
BG_COLOR       = "#1a1a2e"
BAR_COLOR      = "#0f0f1e"
ACCENT         = "#e94560"
BTN_BG         = "#1e2a45"
TEXT_COLOR     = "#f0f0f0"
URL_BG         = "#0d1120"
# ─────────────────────────────────────────────────────────────────────────────


STYLE = f"""
    QWidget {{
        background: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Segoe UI';
    }}
    #titleBar {{
        background: {BAR_COLOR};
        border-bottom: 1px solid #2a2a4a;
    }}
    QPushButton#navBtn {{
        background: {BTN_BG};
        color: {TEXT_COLOR};
        border: none;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 12px;
    }}
    QPushButton#navBtn:hover {{ background: #2a3a5a; }}
    QPushButton#navBtn:pressed {{ background: #3a4a6a; }}

    QPushButton#closeBtn {{
        background: {ACCENT};
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
    }}
    QPushButton#closeBtn:hover {{ background: #ff6b81; }}
    QPushButton#closeBtn:pressed {{ background: #c0392b; }}

    QPushButton#toggleBtn {{
        background: #2a3a5a;
        color: {TEXT_COLOR};
        border: none;
        border-radius: 4px;
        font-size: 10px;
        padding: 4px 7px;
    }}
    QPushButton#toggleBtn:hover {{ background: #3a4a6a; }}

    QLineEdit#urlBar {{
        background: {URL_BG};
        color: {TEXT_COLOR};
        border: 1px solid #2a2a4a;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 11px;
        selection-background-color: {ACCENT};
    }}
    QLineEdit#urlBar:focus {{ border: 1px solid {ACCENT}; }}

    QPushButton#goBtn {{
        background: {ACCENT};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: bold;
    }}
    QPushButton#goBtn:hover {{ background: #ff6b81; }}
"""


class MiniBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x_big     = False
        self._drag_pos = None

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet(STYLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Snap to left side, vertically centered
        screen = QApplication.primaryScreen().availableGeometry()
        y = (screen.height() - WINDOW_HEIGHT) // 2
        self.move(0, y)

        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._make_titlebar())
        layout.addWidget(self._make_urlbar())
        layout.addWidget(self._make_browser())

    def _make_titlebar(self):
        bar = QWidget()
        bar.setObjectName("titleBar")
        bar.setFixedHeight(38)
        h = QHBoxLayout(bar)
        h.setContentsMargins(10, 0, 6, 0)
        h.setSpacing(6)

        icon = QLabel("🌐")
        icon.setFont(QFont("Segoe UI Emoji", 13))
        h.addWidget(icon)

        title = QLabel("Mini Browser")
        title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        title.setStyleSheet(f"color: {TEXT_COLOR};")
        h.addWidget(title)
        h.addStretch()

        self.toggle_btn = QPushButton("⇔")
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setToolTip("Toggle close-button size")
        self.toggle_btn.setFixedSize(28, 26)
        self.toggle_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_btn.clicked.connect(self._toggle_x_size)
        h.addWidget(self.toggle_btn)

        self.close_btn = QPushButton()
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.clicked.connect(self._close)
        h.addWidget(self.close_btn)
        self._refresh_close_btn()

        bar.mousePressEvent   = self._drag_start
        bar.mouseMoveEvent    = self._drag_move
        bar.mouseReleaseEvent = self._drag_end
        return bar

    def _make_urlbar(self):
        bar = QWidget()
        bar.setStyleSheet(f"background: {BAR_COLOR}; border-bottom: 1px solid #1a1a3a;")
        bar.setFixedHeight(34)
        h = QHBoxLayout(bar)
        h.setContentsMargins(6, 3, 6, 3)
        h.setSpacing(4)

        for text, slot in [("◀", self._go_back), ("▶", self._go_forward), ("⟳", self._reload)]:
            b = QPushButton(text)
            b.setObjectName("navBtn")
            b.setFixedSize(26, 26)
            b.setCursor(QCursor(Qt.PointingHandCursor))
            b.clicked.connect(slot)
            h.addWidget(b)

        self.url_bar = QLineEdit(START_URL)
        self.url_bar.setObjectName("urlBar")
        self.url_bar.setFixedHeight(26)
        self.url_bar.returnPressed.connect(self._navigate_from_bar)
        h.addWidget(self.url_bar)

        go = QPushButton("Go")
        go.setObjectName("goBtn")
        go.setFixedSize(34, 26)
        go.setCursor(QCursor(Qt.PointingHandCursor))
        go.clicked.connect(self._navigate_from_bar)
        h.addWidget(go)
        return bar

    def _make_browser(self):
        self.browser = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        self.browser.urlChanged.connect(
            lambda url: self.url_bar.setText(url.toString())
        )
        self.browser.load(QUrl(START_URL))
        return self.browser

    # ── Close button toggle ───────────────────────────────────────────────────
    def _refresh_close_btn(self):
        if self.x_big:
            self.close_btn.setText("  ✕  ")
            self.close_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
            self.close_btn.setFixedSize(44, 30)
        else:
            self.close_btn.setText("×")
            self.close_btn.setFont(QFont("Segoe UI", 11))
            self.close_btn.setFixedSize(26, 26)

    def _toggle_x_size(self):
        self.x_big = not self.x_big
        self._refresh_close_btn()

    def _close(self):
        QApplication.quit()

    # ── Navigation ────────────────────────────────────────────────────────────
    def _navigate_from_bar(self):
        url = self.url_bar.text().strip()
        if not url.startswith(("http://", "https://")):
            if " " in url or "." not in url:
                url = "https://www.google.com/search?q=" + url.replace(" ", "+")
            else:
                url = "https://" + url
        self.browser.load(QUrl(url))

    def _go_back(self):    self.browser.back()
    def _go_forward(self): self.browser.forward()
    def _reload(self):     self.browser.reload()

    # ── Draggable title bar ───────────────────────────────────────────────────
    def _drag_start(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def _drag_move(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)

    def _drag_end(self, event):
        self._drag_pos = None


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Mini Browser")
    window = MiniBrowser()
    window.show()
    sys.exit(app.exec_())