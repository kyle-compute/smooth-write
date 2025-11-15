"""Color definitions for the dark theme."""

from typing import Dict

# Color palette for dark theme
COLORS: Dict[str, str] = {
    # Background colors (solid/opaque)
    "bg_primary": "rgb(18, 18, 24)",
    "bg_secondary": "rgb(28, 28, 36)",
    "bg_hover": "rgb(48, 48, 60)",
    "bg_selected": "rgb(88, 88, 108)",

    # Accent colors
    "accent_primary": "#7c3aed",  # Purple
    "accent_secondary": "#a78bfa",
    "accent_hover": "#8b5cf6",

    # Text colors
    "text_primary": "#e5e7eb",
    "text_secondary": "#9ca3af",
    "text_tertiary": "#6b7280",

    # Border colors
    "border_subtle": "rgba(255, 255, 255, 0.1)",
    "border_medium": "rgba(255, 255, 255, 0.2)",

    # Shadows
    "shadow_sm": "0 2px 8px rgba(0, 0, 0, 0.15)",
    "shadow_md": "0 4px 16px rgba(0, 0, 0, 0.25)",
    "shadow_lg": "0 8px 32px rgba(0, 0, 0, 0.35)",
}
