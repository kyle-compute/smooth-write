"""Rich text editor widget."""

import logging
from typing import Optional

from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from .animations import animation_manager

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

        # OpenGL viewport disabled due to segfault issues on this system
        # Hardware acceleration would be ideal, but software rendering with
        # optimizations below provides acceptable smoothness
        # if OPENGL_AVAILABLE:
        #     try:
        #         gl_widget = QOpenGLWidget()
        #         self._editor.setViewport(gl_widget)
        #         logger.info("OpenGL viewport enabled for smooth rendering")
        #     except Exception as e:
        #         logger.warning(f"Failed to enable OpenGL viewport: {e}")

        # Enable smooth rendering for cursor and text
        # Allow Qt to manage background erasure for proper cursor rendering
        # (WA_OpaquePaintEvent causes cursor ghosting/artifacts)
        self._editor.viewport().setAttribute(
            Qt.WidgetAttribute.WA_OpaquePaintEvent, False
        )
        # Use default system background handling
        self._editor.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)

        # Set comfortable font with optimized rendering for smooth cursor
        font = QFont()
        font.setFamily("SF Pro Text")
        font.setPointSize(18)  # Larger for comfortable reading
        # Use full hinting and antialiasing for smoother appearance
        font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self._editor.setFont(font)

        # Set cursor width for better visibility
        self._editor.setCursorWidth(3)  # Wider cursor for better visibility

        # Optimize text document for smooth rendering
        doc = self._editor.document()
        # Disable design metrics to prevent cursor positioning jitter
        doc.setUseDesignMetrics(False)
        doc.setDocumentMargin(10)  # More breathing room around text

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

    def set_html(self, html: str, animate: bool = True) -> None:
        """Set editor content from HTML with smooth cross-fade animation.

        Args:
            html: HTML content to set
            animate: Whether to animate the transition (default: True)
        """
        if not animate or not html:
            self._editor.setHtml(html)
            return

        # Cross-fade animation
        def switch_content():
            self._editor.setHtml(html)

        animation_manager.cross_fade(self._editor, switch_content, duration=200)

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
