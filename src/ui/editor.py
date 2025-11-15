"""Rich text editor widget."""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

try:
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget
    OPENGL_AVAILABLE = True
except ImportError:
    OPENGL_AVAILABLE = False

logger = logging.getLogger(__name__)


class RichTextEditor(QWidget):
    """Rich text editor for writing notes.

    Provides a clean, distraction-free writing experience.

    Signals:
        content_changed: Emitted when content changes
    """

    content_changed = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize rich text editor.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
        logger.info("Rich text editor initialized")

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create text editor
        self._editor = QTextEdit()
        self._editor.setAcceptRichText(True)
        self._editor.setPlaceholderText("Start writing...")

        # OpenGL viewport disabled due to segfault issues on some systems
        # if OPENGL_AVAILABLE:
        #     try:
        #         self._editor.setViewport(QOpenGLWidget())
        #         logger.info("OpenGL viewport enabled for smooth rendering")
        #     except Exception as e:
        #         logger.warning(f"Failed to enable OpenGL viewport: {e}")

        # Enable smooth rendering for cursor and text
        self._editor.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self._editor.viewport().setAttribute(
            Qt.WidgetAttribute.WA_OpaquePaintEvent, False
        )

        # Set comfortable font with optimized rendering for smooth cursor
        font = QFont()
        font.setFamily("SF Pro Text")
        font.setPointSize(16)
        font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
        font.setStyleStrategy(QFont.StyleStrategy.PreferDefault)
        self._editor.setFont(font)

        # Set cursor width for better visibility
        self._editor.setCursorWidth(2)

        # Optimize text document for smooth rendering
        doc = self._editor.document()
        doc.setUseDesignMetrics(True)
        doc.setDocumentMargin(4)

        # Disable auto-fill background for smoother repaints
        self._editor.setAutoFillBackground(False)
        self._editor.viewport().setAutoFillBackground(False)

        layout.addWidget(self._editor)

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self._editor.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self) -> None:
        """Handle text change."""
        self.content_changed.emit()

    # Public API

    def get_html(self) -> str:
        """Get editor content as HTML.

        Returns:
            HTML content
        """
        return self._editor.toHtml()

    def set_html(self, html: str) -> None:
        """Set editor content from HTML.

        Args:
            html: HTML content to set
        """
        self._editor.setHtml(html)

    def get_plain_text(self) -> str:
        """Get editor content as plain text.

        Returns:
            Plain text content
        """
        return self._editor.toPlainText()

    def set_plain_text(self, text: str) -> None:
        """Set editor content from plain text.

        Args:
            text: Plain text to set
        """
        self._editor.setPlainText(text)

    def clear(self) -> None:
        """Clear editor content."""
        self._editor.clear()

    def set_focus(self) -> None:
        """Set focus to editor."""
        self._editor.setFocus()

    def is_modified(self) -> bool:
        """Check if document has been modified.

        Returns:
            True if modified, False otherwise
        """
        return self._editor.document().isModified()

    def set_modified(self, modified: bool) -> None:
        """Set document modified state.

        Args:
            modified: Modified state
        """
        self._editor.document().setModified(modified)
