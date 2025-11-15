# Smooth Write

A beautiful, modern Python desktop writing application. Smooth Write provides a distraction-free writing experience with rich text support, auto-save, and an elegant dark theme.

## Features

- **Modern Dark UI** - Clean, solid dark theme with purple accents
- **Rich Text Editing** - HTML-based rich text support
- **Auto-Save** - Automatic saving with smart debouncing (1 second after you stop typing)
- **Multiple Notes** - Organize your thoughts with a searchable notes list
- **Keyboard Shortcuts** - Efficient workflow with keyboard navigation
- **Clean Design** - Distraction-free writing environment

## Installation

### Prerequisites

- Python 3.10 or higher
- Virtual environment (already set up with `.venv`)

### Setup

1. Activate the virtual environment:
```bash
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the App

```bash
python -m src.main
```

Or from the project root:
```bash
python src/main.py
```

### Keyboard Shortcuts

- **Ctrl+N** - Create new note
- **Ctrl+S** - Save current note immediately
- **Ctrl+F** - Focus search bar
- **Ctrl+Q** - Quit application

### Basic Workflow

1. **Create a Note** - Click the `+` button or press `Ctrl+N`
2. **Start Writing** - Click in the editor and start typing
3. **Search Notes** - Use the search bar to find specific notes
4. **Auto-Save** - Your work is automatically saved as you type

## Project Structure

```
smooth-write/
├── src/
│   ├── main.py              # Application entry point
│   ├── app.py               # Main window implementation
│   ├── core/                # Core business logic
│   │   ├── note.py         # Note data model
│   │   ├── storage.py      # JSON storage manager
│   │   └── auto_save.py    # Auto-save with debouncing
│   ├── ui/                  # User interface components
│   │   ├── editor.py       # Rich text editor widget
│   │   ├── notes_list.py   # Notes sidebar widget
│   │   ├── styles.py       # Glassmorphism styling
│   │   └── animations.py   # Smooth animations
│   └── utils/               # Utility modules
│       └── blur_effect.py  # Blur effect utilities
├── notes/                   # Stored notes (auto-created)
├── logs/                    # Application logs (auto-created)
├── assets/                  # Application assets
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Architecture

### Design Patterns

- **MVC Pattern** - Separation of data (Note), logic (StorageManager), and UI (Widgets)
- **Observer Pattern** - Qt signals/slots for event handling
- **Strategy Pattern** - Modular storage backend (currently JSON, extensible to database)

### Best Practices

- **Type Hints** - Full type annotations for better code quality
- **Docstrings** - Comprehensive documentation for all classes and methods
- **Logging** - Structured logging throughout the application
- **Separation of Concerns** - Clear module boundaries and responsibilities
- **Error Handling** - Graceful error handling with user feedback

## Data Storage

Notes are stored as individual JSON files in the `notes/` directory. Each note contains:

- `id` - Unique identifier
- `title` - Auto-generated from first line
- `content` - Rich text content (HTML format)
- `created_at` - Creation timestamp
- `modified_at` - Last modification timestamp
- `is_favorite` - Favorite status (future feature)

## Customization

### Changing Auto-Save Delay

Edit `src/app.py`, find the `AutoSaveManager` initialization:

```python
self._auto_save_manager = AutoSaveManager(
    save_callback=self._save_current_note,
    delay_ms=1000  # Change this value (in milliseconds)
)
```

### Modifying Theme Colors

Edit `src/ui/styles.py` and modify the `COLORS` dictionary:

```python
COLORS: Dict[str, str] = {
    "accent_primary": "#7c3aed",  # Change to your preferred color
    # ... other colors
}
```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for all public methods
- Keep functions focused and single-purpose

### Adding New Features

1. **New UI Component** - Add to `src/ui/`
2. **Business Logic** - Add to `src/core/`
3. **Utility Functions** - Add to `src/utils/`
4. **Update** `__init__.py` files to expose new modules

## Troubleshooting

### Window doesn't show blur effect

The blur effect implementation varies by platform. On Linux, it uses `QGraphicsBlurEffect`. For better native blur on Windows 11 or macOS, additional platform-specific code can be added.

### Notes not saving

Check the `logs/smooth-write.log` file for error messages. Ensure the application has write permissions in the current directory.

### Application crashes on startup

1. Verify Python version: `python --version` (should be 3.10+)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Check logs in `logs/smooth-write.log`

## Future Enhancements

- [ ] Export notes to Markdown/PDF
- [ ] Note folders and tags
- [ ] Cloud sync support
- [ ] Themes customization UI
- [ ] Spell check
- [ ] Word count statistics
- [ ] Image embedding
- [ ] Better native blur effects for Windows/macOS

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please ensure:

- Code follows existing style and patterns
- All functions have type hints and docstrings
- Changes are tested on multiple platforms
- Commits are clear and descriptive

---

Built with Python, PyQt6, and attention to detail.
