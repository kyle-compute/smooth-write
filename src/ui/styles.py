"""Application stylesheet and theme."""

from .colors import COLORS


def get_stylesheet() -> str:
    """Get the complete application stylesheet.

    Returns:
        CSS stylesheet string for the entire application
    """
    return f"""
    /* Global styles - Warm, Anthropic-inspired design */
    * {{
        font-family: 'SF Pro Text', 'Inter', -apple-system, BlinkMacSystemFont,
                     'Segoe UI', Roboto, sans-serif;
        outline: none;
    }}

    QMainWindow {{
        background: {COLORS['bg_primary']};
        color: {COLORS['text_primary']};
    }}

    /* Notes list sidebar - Improved spacing and softness */
    QListWidget {{
        background: {COLORS['bg_secondary']};
        border: 1px solid {COLORS['border_subtle']};
        border-radius: 16px;
        padding: 10px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}

    QListWidget::item {{
        background: transparent;
        border-radius: 12px;
        padding: 16px 18px;
        margin: 3px 0;
        border: 1px solid transparent;
    }}

    QListWidget::item:hover {{
        background: {COLORS['bg_hover']};
        border: 1px solid {COLORS['border_subtle']};
    }}

    QListWidget::item:selected {{
        background: {COLORS['bg_selected']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border_medium']};
    }}

    /* Text editor - Comfortable for extended writing */
    QTextEdit {{
        background: {COLORS['bg_primary']};
        border: none;
        color: {COLORS['text_primary']};
        font-size: 18px;
        line-height: 1.6;
        padding: 32px;
        selection-background-color: {COLORS['selection_bg']};
        selection-color: {COLORS['text_primary']};
    }}

    QTextEdit::placeholder {{
        color: {COLORS['text_placeholder']};
    }}

    /* Scrollbars - Soft and subtle */
    QScrollBar:vertical {{
        background: transparent;
        width: 14px;
        margin: 0px;
        border-radius: 7px;
    }}

    QScrollBar::handle:vertical {{
        background: {COLORS['border_strong']};
        border-radius: 7px;
        min-height: 40px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {COLORS['text_tertiary']};
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: transparent;
        height: 14px;
        margin: 0px;
        border-radius: 7px;
    }}

    QScrollBar::handle:horizontal {{
        background: {COLORS['border_strong']};
        border-radius: 7px;
        min-width: 40px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {COLORS['text_tertiary']};
    }}

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* Buttons - Improved touch targets and coral accents */
    QPushButton {{
        background: {COLORS['bg_elevated']};
        border: 1px solid {COLORS['border_medium']};
        border-radius: 10px;
        padding: 12px 24px;
        color: {COLORS['text_primary']};
        font-size: 14px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background: {COLORS['bg_hover']};
        border: 1px solid {COLORS['border_strong']};
    }}

    QPushButton:pressed {{
        background: {COLORS['bg_selected']};
    }}

    QPushButton[primary="true"] {{
        background: {COLORS['accent_primary']};
        border: none;
        color: {COLORS['text_on_accent']};
    }}

    QPushButton[primary="true"]:hover {{
        background: {COLORS['accent_hover']};
        color: {COLORS['text_on_accent']};
    }}

    /* Search bar - Better spacing and coral focus ring */
    QLineEdit {{
        background: {COLORS['bg_elevated']};
        border: 2px solid {COLORS['border_medium']};
        border-radius: 10px;
        padding: 12px 18px;
        color: {COLORS['text_primary']};
        font-size: 14px;
    }}

    QLineEdit:focus {{
        border: 2px solid {COLORS['focus_ring']};
        background: {COLORS['bg_elevated']};
    }}

    QLineEdit::placeholder {{
        color: {COLORS['text_placeholder']};
    }}

    /* Tooltips - Soft and warm */
    QToolTip {{
        background: {COLORS['bg_elevated']};
        border: 1px solid {COLORS['border_medium']};
        border-radius: 8px;
        padding: 8px 12px;
        color: {COLORS['text_primary']};
        font-size: 12px;
    }}

    /* Labels - Use warm text colors */
    QLabel {{
        color: {COLORS['text_primary']};
    }}

    /* Splitter - More grabbable handle */
    QSplitter::handle {{
        background: {COLORS['border_medium']};
    }}

    QSplitter::handle:hover {{
        background: {COLORS['border_strong']};
    }}
    """
