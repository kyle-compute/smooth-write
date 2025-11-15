"""Helper functions for the application."""

from .core import Note


def create_welcome_note() -> Note:
    """Create a welcome note for first-time users.

    Returns:
        Welcome note instance
    """
    note = Note()
    note.content = """
    <h1>Welcome to Smooth Write!</h1>
    <p>A beautiful, smooth writing app with a clean dark UI.</p>
    <br>
    <h2>Features:</h2>
    <ul>
        <li><b>Rich text support</b> - Write with HTML formatting</li>
        <li><b>Auto-save</b> - Your work is saved automatically</li>
        <li><b>Search</b> - Find notes quickly with Ctrl+F</li>
        <li><b>Keyboard shortcuts</b> - Ctrl+N for new note, Ctrl+S to save</li>
    </ul>
    <br>
    <p>Start writing by creating a new note with the + button or Ctrl+N!</p>
    """
    note.update_content(note.content)
    return note
