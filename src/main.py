"""Application entry point."""

import sys
import logging
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

from .app import MainWindow
from .ui.animations import animation_manager


def setup_logging() -> None:
    """Configure application logging."""
    # Create logs directory
    log_dir = Path.cwd() / "logs"
    log_dir.mkdir(exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "smooth-write.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Logging initialized")


def setup_application() -> QApplication:
    """Set up and configure the Qt application.

    Returns:
        Configured QApplication instance
    """
    # Enable smooth rendering with OpenGL
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseDesktopOpenGL)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    # Enable high DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Smooth Write")
    app.setOrganizationName("SmoothWrite")
    app.setApplicationVersion("0.1.0")

    # Set application-wide palette for dark theme
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 24))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(229, 231, 235))
    palette.setColor(QPalette.ColorRole.Base, QColor(28, 28, 36))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(38, 38, 46))
    palette.setColor(QPalette.ColorRole.Text, QColor(229, 231, 235))
    palette.setColor(QPalette.ColorRole.Button, QColor(28, 28, 36))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(229, 231, 235))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(124, 58, 237))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(229, 231, 235))

    app.setPalette(palette)

    # Set cursor flash time for smoother appearance (match Microsoft Word)
    app.setCursorFlashTime(530)  # ~530ms is standard on Windows

    logger = logging.getLogger(__name__)
    logger.info("Application configured")

    return app


def main() -> int:
    """Main entry point.

    Returns:
        Exit code
    """
    # Set up logging
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starting Smooth Write v0.1.0")

    try:
        # Create application
        app = setup_application()

        # Create and show main window with smooth fade-in
        window = MainWindow()

        # Set initial window opacity for fade-in animation
        window.setWindowOpacity(0.0)

        window.show()

        # Animate fade in (uses windowOpacity automatically for windows)
        animation_manager.fade_in(window, duration=300)

        logger.info("Application started successfully")

        # Run event loop
        return app.exec()

    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
