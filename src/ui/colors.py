"""Color definitions for the warm, Anthropic-inspired theme."""

from typing import Dict

# Warm, soft color palette inspired by Anthropic's design aesthetic
COLORS: Dict[str, str] = {
    # Background colors - Warm neutrals (light theme)
    "bg_primary": "#FAF9F6",        # Soft cream - main writing surface
    "bg_secondary": "#F5F3EE",      # Warm off-white - sidebar
    "bg_tertiary": "#EDEAE3",       # Subtle warm gray - cards
    "bg_hover": "#E8E5DD",          # Warm gray hover state
    "bg_selected": "#E0DBD1",       # Warm taupe selection
    "bg_elevated": "#FFFFFF",       # Pure white for elevation

    # Accent colors - Soft corals (Anthropic-inspired)
    "accent_primary": "#E87854",    # Soft coral - primary actions
    "accent_hover": "#DC6A48",      # Deeper coral - hover states
    "accent_secondary": "#CC785C",  # Muted terracotta - secondary
    "accent_muted": "#F4A68C",      # Pale coral - subtle highlights

    # Text colors - Warm darks for comfortable reading
    "text_primary": "#2C2416",      # Deep warm brown - main text
    "text_secondary": "#5C5244",    # Medium warm gray - secondary text
    "text_tertiary": "#8B8173",     # Light warm gray - timestamps
    "text_placeholder": "#B5AFA3",  # Very light warm gray - placeholders
    "text_on_accent": "#FFFFFF",    # White text on coral buttons

    # Border colors - Warm subtle boundaries
    "border_subtle": "#E8E5DD",     # Barely visible warm border
    "border_medium": "#D9D5CC",     # Subtle warm border
    "border_strong": "#C9C4B9",     # Visible warm border

    # Special states
    "selection_bg": "#F4E8D8",      # Warm peach text selection
    "focus_ring": "#E87854",        # Coral focus indicator

    # Shadows - Soft warm shadows (not harsh black)
    "shadow_sm": "0 2px 8px rgba(44, 36, 22, 0.08)",
    "shadow_md": "0 4px 16px rgba(44, 36, 22, 0.12)",
    "shadow_lg": "0 8px 32px rgba(44, 36, 22, 0.16)",
}
