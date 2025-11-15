"""Auto-save manager with debouncing."""

import logging
from typing import Callable, Optional

from PyQt6.QtCore import QTimer

logger = logging.getLogger(__name__)


class AutoSaveManager:
    """Manages automatic saving with debouncing.

    Delays save operations until user stops typing, preventing
    excessive disk writes while ensuring data is never lost.

    Attributes:
        save_callback: Function to call when saving
        delay_ms: Delay in milliseconds before saving
    """

    def __init__(
        self,
        save_callback: Callable[[], None],
        delay_ms: int = 1000
    ):
        """Initialize auto-save manager.

        Args:
            save_callback: Function to call when saving (takes no args)
            delay_ms: Delay in milliseconds before saving (default: 1000ms)
        """
        self.save_callback = save_callback
        self.delay_ms = delay_ms

        # Create debounce timer
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_save)

        self._is_enabled = True
        logger.info(f"Auto-save initialized with {delay_ms}ms delay")

    def trigger(self) -> None:
        """Trigger auto-save (restarts debounce timer).

        Call this method whenever content changes. The actual save
        will happen after the delay period with no new triggers.
        """
        if not self._is_enabled:
            return

        # Restart the timer (debounce)
        self._timer.stop()
        self._timer.start(self.delay_ms)
        logger.debug("Auto-save triggered")

    def _on_save(self) -> None:
        """Internal: Execute save callback."""
        try:
            logger.debug("Executing auto-save")
            self.save_callback()
        except Exception as e:
            logger.error(f"Auto-save failed: {e}")

    def save_now(self) -> None:
        """Force immediate save, bypassing debounce timer."""
        self._timer.stop()
        self._on_save()

    def enable(self) -> None:
        """Enable auto-save."""
        self._is_enabled = True
        logger.info("Auto-save enabled")

    def disable(self) -> None:
        """Disable auto-save and cancel pending saves."""
        self._is_enabled = False
        self._timer.stop()
        logger.info("Auto-save disabled")

    def set_delay(self, delay_ms: int) -> None:
        """Change auto-save delay.

        Args:
            delay_ms: New delay in milliseconds
        """
        self.delay_ms = delay_ms
        logger.info(f"Auto-save delay changed to {delay_ms}ms")

    def cleanup(self) -> None:
        """Clean up resources."""
        self._timer.stop()
        self._timer.deleteLater()
