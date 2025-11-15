"""Application stylesheet and theme."""

from .colors import COLORS


def get_stylesheet() -> str:
    """Get the complete application stylesheet.

    Returns:
        CSS stylesheet string for the entire application
    """
    return f"""
    /* Global styles */
    * {{
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont,
                     'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell,
                     'Helvetica Neue', sans-serif;
        outline: none;
    }}

    QMainWindow {{
        background: {COLORS['bg_primary']};
    }}

    /* Notes list sidebar */
    QListWidget {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border_subtle']};
        border-radius: 12px;
        padding: 8px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}

    QListWidget::item {{
        background: transparent;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 4px 0;
        border: none;
    }}

    QListWidget::item:hover {{
        background: {COLORS['bg_hover']};
    }}

    QListWidget::item:selected {{
        background: {COLORS['bg_selected']};
        color: {COLORS['text_primary']};
    }}

    /* Text editor */
    QTextEdit {{
        background: {COLORS['bg_primary']};
        border: none;
        color: {COLORS['text_primary']};
        font-size: 16px;
        line-height: 1.6;
        padding: 24px;
        selection-background-color: {COLORS['accent_primary']};
        selection-color: {COLORS['text_primary']};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: transparent;
        width: 12px;
        margin: 0px;
        border-radius: 6px;
    }}

    QScrollBar::handle:vertical {{
        background: {COLORS['bg_hover']};
        border-radius: 6px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {COLORS['bg_selected']};
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: transparent;
        height: 12px;
        margin: 0px;
        border-radius: 6px;
    }}

    QScrollBar::handle:horizontal {{
        background: {COLORS['bg_hover']};
        border-radius: 6px;
        min-width: 30px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {COLORS['bg_selected']};
    }}

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* Buttons */
    QPushButton {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border_subtle']};
        border-radius: 8px;
        padding: 10px 20px;
        color: {COLORS['text_primary']};
        font-size: 14px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background: {COLORS['bg_hover']};
        border: 1px solid {COLORS['border_medium']};
    }}

    QPushButton:pressed {{
        background: {COLORS['bg_selected']};
    }}

    QPushButton[primary="true"] {{
        background: {COLORS['accent_primary']};
        border: none;
    }}

    QPushButton[primary="true"]:hover {{
        background: {COLORS['accent_hover']};
    }}

    /* Search bar */
    QLineEdit {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border_subtle']};
        border-radius: 8px;
        padding: 10px 16px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}

    QLineEdit:focus {{
        border: 1px solid {COLORS['accent_primary']};
    }}

    QLineEdit::placeholder {{
        color: {COLORS['text_tertiary']};
    }}

    /* Tooltips */
    QToolTip {{
        background: {COLORS['bg_primary']};
        border: 1px solid {COLORS['border_medium']};
        border-radius: 6px;
        padding: 6px 10px;
        color: {COLORS['text_primary']};
        font-size: 12px;
    }}

    /* Labels */
    QLabel {{
        color: {COLORS['text_primary']};
    }}
    """
