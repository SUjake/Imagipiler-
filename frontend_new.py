from compiler_core import run_compiler
import sys
from rich.console import Console

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPlainTextEdit, QPushButton,
    QVBoxLayout, QWidget, QTextEdit, QLabel, QScrollArea
)
from PyQt5.QtGui import (
    QFont, QColor, QTextCharFormat, QSyntaxHighlighter,
    QPixmap, QTextOption, QDesktopServices
)
from PyQt5.QtCore import Qt, QRegExp, QThread, pyqtSignal, QUrl


# ---------------- WORKER THREAD ----------------
class CompilerWorker(QThread):
    result_signal = pyqtSignal(str, str)

    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self):
        console = Console(record=True, width=140, force_terminal=True, color_system="truecolor")

        try:
            ast_path = run_compiler(self.code, console=console)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            ast_path = None

        html = console.export_html(inline_styles=True, theme=None)

        html = f"""
        <html>
        <head>
        <style>
        body {{
            background-color: #1e1e1e;
            color: white;
        }}
        pre {{
            background-color: #1e1e1e !important;
            color: white !important;
            font-family: Consolas;
            font-size: 14px;
        }}
        </style>
        </head>
        <body>
        {html}
        </body>
        </html>
        """

        self.result_signal.emit(html, ast_path)


# ---------------- SYNTAX HIGHLIGHTER ----------------
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)

        keywords = ["show", "take", "int", "string", "float"]

        self.rules = [(QRegExp(r'\b' + word + r'\b'), keyword_format) for word in keywords]

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.rules.append((QRegExp(r'".*"'), string_format))
        self.rules.append((QRegExp(r"'.*'"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.rules.append((QRegExp(r'#.*'), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)


# ---------------- EDITOR ----------------
class CodeEditor(QPlainTextEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            cursor.select(cursor.LineUnderCursor)
            current_line = cursor.selectedText()

            indent = ""
            for char in current_line:
                if char in [" ", "\t"]:
                    indent += char
                else:
                    break

            super().keyPressEvent(event)
            self.insertPlainText(indent)
        else:
            super().keyPressEvent(event)


# ---------------- MAIN WINDOW ----------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Imagipiler IDE")
        self.setGeometry(100, 100, 1100, 750)

        self.current_ast_path = None

        # Editor
        self.editor = CodeEditor()
        self.editor.setFont(QFont("Consolas", 12))
        self.editor.setStyleSheet("background:#1e1e1e; color:white;")
        self.highlighter = PythonHighlighter(self.editor.document())

        # Run Button
        self.button = QPushButton("Run Imagipiler")
        self.button.clicked.connect(self.run_code)

        # Console Preview
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setWordWrapMode(QTextOption.NoWrap)
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.console.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.console.setStyleSheet("""
            background-color: #1e1e1e;
            color: white;
            font-family: Consolas;
        """)

        # AST VIEW
        self.ast_label = QLabel()
        self.ast_label.setAlignment(Qt.AlignCenter)

        self.ast_scroll = QScrollArea()
        self.ast_scroll.setWidgetResizable(True)
        self.ast_scroll.setWidget(self.ast_label)
        self.ast_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ast_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ast_scroll.setStyleSheet("background-color: #222;")

        # Buttons
        self.open_ast_button = QPushButton("Open Full AST")
        self.open_ast_button.setEnabled(False)
        self.open_ast_button.clicked.connect(self.open_ast_image)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.editor, 3)
        layout.addWidget(self.button, 0)
        layout.addWidget(self.console, 3)
        layout.addWidget(self.ast_scroll, 2)
        layout.addWidget(self.open_ast_button, 0)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_code(self):
        code = self.editor.toPlainText()
        self.console.clear()
        self.ast_label.clear()
        self.open_ast_button.setEnabled(False)

        self.worker = CompilerWorker(code)
        self.worker.result_signal.connect(self.display_output)
        self.worker.start()

    def display_output(self, html, image_path):
        self.console.setHtml(html)

        self.current_ast_path = image_path

        if image_path:
            pixmap = QPixmap(image_path)
            scaled = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.ast_label.setPixmap(scaled)
            self.open_ast_button.setEnabled(True)

    def open_ast_image(self):
        if self.current_ast_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.current_ast_path))


# ---------------- RUN APP ----------------
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())