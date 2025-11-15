"""Animation helper module for smooth UI transitions."""

import logging
from typing import Optional, Callable, List
from PyQt6.QtCore import (
    QPropertyAnimation, QVariantAnimation, QSequentialAnimationGroup,
    QParallelAnimationGroup, QEasingCurve, QTimer, pyqtProperty, QRect
)
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QGraphicsOpacityEffect

logger = logging.getLogger(__name__)


class AnimationManager:
    """Manages animations to prevent garbage collection and provide smooth transitions."""

    # Standard durations (milliseconds)
    DURATION_INSTANT = 100
    DURATION_FAST = 150
    DURATION_NORMAL = 250
    DURATION_SLOW = 400

    # Standard easing curves
    EASE_IN = QEasingCurve.Type.InQuad
    EASE_OUT = QEasingCurve.Type.OutQuad
    EASE_IN_OUT = QEasingCurve.Type.InOutQuad
    EASE_OUT_BACK = QEasingCurve.Type.OutBack
    EASE_OUT_CUBIC = QEasingCurve.Type.OutCubic
    EASE_IN_CUBIC = QEasingCurve.Type.InCubic

    def __init__(self):
        """Initialize animation manager."""
        self._active_animations: List = []

    def _store_animation(self, animation) -> None:
        """Store animation reference to prevent garbage collection."""
        self._active_animations.append(animation)
        animation.finished.connect(lambda: self._cleanup_animation(animation))

    def _cleanup_animation(self, animation) -> None:
        """Remove finished animation from active list."""
        if animation in self._active_animations:
            self._active_animations.remove(animation)

    def fade_in(self, widget: QWidget, duration: int = DURATION_NORMAL,
                on_finished: Optional[Callable] = None) -> QPropertyAnimation:
        """Fade in widget from transparent to opaque.

        Uses windowOpacity for top-level windows (avoids QPainter conflicts)
        and QGraphicsOpacityEffect for child widgets.
        """
        # Check if this is a top-level window
        is_window = widget.isWindow()

        if is_window:
            # Use windowOpacity for top-level windows to avoid QPainter conflicts
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(duration)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(self.EASE_OUT_CUBIC)
        else:
            # Use QGraphicsOpacityEffect for child widgets
            if not widget.graphicsEffect():
                effect = QGraphicsOpacityEffect()
                widget.setGraphicsEffect(effect)

            effect = widget.graphicsEffect()
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(self.EASE_OUT_CUBIC)

        if on_finished:
            animation.finished.connect(on_finished)

        self._store_animation(animation)
        animation.start()
        return animation

    def fade_out(self, widget: QWidget, duration: int = DURATION_FAST,
                 on_finished: Optional[Callable] = None) -> QPropertyAnimation:
        """Fade out widget from opaque to transparent.

        Uses windowOpacity for top-level windows (avoids QPainter conflicts)
        and QGraphicsOpacityEffect for child widgets.
        """
        # Check if this is a top-level window
        is_window = widget.isWindow()

        if is_window:
            # Use windowOpacity for top-level windows to avoid QPainter conflicts
            animation = QPropertyAnimation(widget, b"windowOpacity")
            animation.setDuration(duration)
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.setEasingCurve(self.EASE_IN_CUBIC)
        else:
            # Use QGraphicsOpacityEffect for child widgets
            if not widget.graphicsEffect():
                effect = QGraphicsOpacityEffect()
                widget.setGraphicsEffect(effect)

            effect = widget.graphicsEffect()
            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.setEasingCurve(self.EASE_IN_CUBIC)

        if on_finished:
            animation.finished.connect(on_finished)

        self._store_animation(animation)
        animation.start()
        return animation

    def cross_fade(self, widget: QWidget, switch_callback: Callable,
                   duration: int = DURATION_NORMAL) -> QSequentialAnimationGroup:
        """Cross-fade: fade out, switch content, fade in."""
        sequence = QSequentialAnimationGroup()

        # Fade out
        fade_out_anim = self.fade_out(widget, duration // 2)
        fade_out_anim.finished.connect(switch_callback)

        # Fade in
        fade_in_anim = self.fade_in(widget, duration // 2)

        sequence.addAnimation(fade_out_anim)
        sequence.addAnimation(fade_in_anim)

        self._store_animation(sequence)
        sequence.start()
        return sequence

    def slide_in_from_top(self, widget: QWidget, duration: int = DURATION_SLOW) -> QParallelAnimationGroup:
        """Slide widget in from above with fade."""
        group = QParallelAnimationGroup()

        # Get final geometry
        final_geo = widget.geometry()

        # Start geometry (above viewport)
        start_geo = QRect(
            final_geo.x(),
            final_geo.y() - 50,  # Start 50px above
            final_geo.width(),
            final_geo.height()
        )

        # Position animation
        widget.setGeometry(start_geo)
        pos_anim = QPropertyAnimation(widget, b"geometry")
        pos_anim.setDuration(duration)
        pos_anim.setStartValue(start_geo)
        pos_anim.setEndValue(final_geo)
        pos_anim.setEasingCurve(self.EASE_OUT_BACK)

        # Opacity animation
        opacity_anim = self.fade_in(widget, duration)

        group.addAnimation(pos_anim)
        group.addAnimation(opacity_anim)

        self._store_animation(group)
        group.start()
        return group


# Global animation manager instance
animation_manager = AnimationManager()
