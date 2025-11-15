"""Main application window."""

import logging
from typing import Optional
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSplitter,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QKeySequence, QShortcut, QAction

from .core import Note, StorageManager, AutoSaveManager
from .ui import RichTextEditor, NotesList, get_stylesheet
from .ui.animations import animation_manager
from .helpers import create_welcome_note

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window with glassmorphism UI.

    Combines notes list sidebar and rich text editor with
    smooth transitions and auto-save functionality.

    Attributes:
        storage: Storage manager for persisting notes
        current_note: Currently active note
    """

    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.storage = StorageManager()
        self.current_note: Optional[Note] = None
        self._auto_save_manager: Optional[AutoSaveManager] = None
        self._is_closing = False  # Flag for smooth close animation

        self._setup_window()
        self._setup_ui()
        self._setup_shortcuts()
        self._load_notes()

        logger.info("Main window initialized")

    def _setup_window(self) -> None:
        """Set up window properties."""
        self.setWindowTitle("Smooth Write")
        self.setMinimumSize(QSize(900, 600))
        self.resize(QSize(1200, 800))

        # Apply stylesheet
        self.setStyleSheet(get_stylesheet())

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(24, 24, 24, 24)  # More generous margins
        layout.setSpacing(20)  # Better spacing between elements

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(10)  # Wider handle for easier grabbing

        # Notes list sidebar
        self._notes_list = NotesList()
        self._notes_list.setMinimumWidth(280)  # Wider for better readability
        self._notes_list.setMaximumWidth(400)
        splitter.addWidget(self._notes_list)

        # Rich text editor
        self._editor = RichTextEditor()
        splitter.addWidget(self._editor)

        # Set initial splitter sizes (30% sidebar, 70% editor)
        splitter.setSizes([300, 700])

        layout.addWidget(splitter)

        # Connect signals
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connect UI signals."""
        self._notes_list.note_selected.connect(self._on_note_selected)
        self._notes_list.new_note_requested.connect(self._create_new_note)
        self._notes_list.delete_note_requested.connect(self._delete_note)

        # Don't connect editor content_changed yet (will connect after loading)

    def _setup_shortcuts(self) -> None:
        """Set up keyboard shortcuts."""
        # Ctrl+N: New note
        new_note_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        new_note_shortcut.activated.connect(self._create_new_note)

        # Ctrl+S: Save now
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self._save_current_note)

        # Ctrl+Q: Quit
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)

        # Ctrl+F: Focus search
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(
            lambda: self._notes_list._search_box.setFocus()
        )

        # Delete: Delete selected note
        delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        delete_shortcut.activated.connect(self._delete_selected_note)

        logger.info("Keyboard shortcuts configured")

    def _load_notes(self) -> None:
        """Load all notes from storage."""
        notes = self.storage.load_all_notes()

        if not notes:
            # Create welcome note if no notes exist
            self._create_welcome_note()
            notes = self.storage.load_all_notes()

        self._notes_list.set_notes(notes)

        # Select first note
        if notes:
            self._notes_list.select_note(notes[0].id)
            self._on_note_selected(notes[0])

        logger.info(f"Loaded {len(notes)} notes")

    def _create_welcome_note(self) -> None:
        """Create a welcome note for first-time users."""
        welcome_note = create_welcome_note()
        self.storage.save_note(welcome_note)
        logger.info("Created welcome note")

    def _on_note_selected(self, note: Note) -> None:
        """Handle note selection.

        Args:
            note: Selected note
        """
        # Save current note before switching
        if self.current_note and self._auto_save_manager:
            self._auto_save_manager.save_now()

        # Disconnect auto-save temporarily
        if self._auto_save_manager:
            self._editor.content_changed.disconnect(
                self._auto_save_manager.trigger
            )

        # Load new note
        self.current_note = note
        self._editor.set_html(note.content)
        self._editor.set_modified(False)

        # Set up auto-save for new note
        self._auto_save_manager = AutoSaveManager(
            save_callback=self._save_current_note,
            delay_ms=1000
        )
        self._editor.content_changed.connect(
            self._auto_save_manager.trigger
        )

        logger.info(f"Loaded note: {note.id}")

    def _create_new_note(self) -> None:
        """Create a new note."""
        note = Note()
        note.content = ""
        note.update_content(note.content)

        # Save to storage
        if self.storage.save_note(note):
            # Add to list
            self._notes_list.add_note(note)

            # Select the new note
            self._notes_list.select_note(note.id)
            self._on_note_selected(note)

            # Focus editor
            self._editor.set_focus()

            logger.info(f"Created new note: {note.id}")
        else:
            logger.error("Failed to create new note")
            QMessageBox.warning(
                self,
                "Error",
                "Failed to create new note. Please try again."
            )

    def _save_current_note(self) -> None:
        """Save the current note."""
        if not self.current_note:
            return

        # Update note content
        content = self._editor.get_html()
        self.current_note.update_content(content)

        # Save to storage
        if self.storage.save_note(self.current_note):
            # Update in list
            self._notes_list.update_note(self.current_note)
            self._editor.set_modified(False)
            logger.debug(f"Saved note: {self.current_note.id}")
        else:
            logger.error(f"Failed to save note: {self.current_note.id}")

    def _delete_selected_note(self) -> None:
        """Delete the currently selected note."""
        selected_note = self._notes_list.get_selected_note()
        if selected_note:
            self._delete_note(selected_note.id)

    def _delete_note(self, note_id: str) -> None:
        """Delete a note.

        Args:
            note_id: ID of note to delete
        """
        reply = QMessageBox.question(
            self,
            "Delete Note",
            "Are you sure you want to delete this note?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.storage.delete_note(note_id):
                self._notes_list.remove_note(note_id)

                # Clear editor if current note was deleted
                if self.current_note and self.current_note.id == note_id:
                    self.current_note = None
                    self._editor.clear()

                logger.info(f"Deleted note: {note_id}")
            else:
                logger.error(f"Failed to delete note: {note_id}")
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to delete note. Please try again."
                )

    def closeEvent(self, event) -> None:
        """Handle window close event with smooth fade-out animation.

        Args:
            event: Close event
        """
        if self._is_closing:
            # Animation already in progress, accept the event
            event.accept()
            return

        # Start closing process with animation
        event.ignore()  # Ignore for now, will close after animation
        self._is_closing = True

        # Save current note before closing
        if self.current_note and self._auto_save_manager:
            self._auto_save_manager.save_now()

        # Clean up auto-save manager
        if self._auto_save_manager:
            self._auto_save_manager.cleanup()

        logger.info("Application closing")

        # Fade out and then close
        def actually_close():
            self.close()

        animation_manager.fade_out(self, duration=200, on_finished=actually_close)
