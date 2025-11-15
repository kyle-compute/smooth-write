"""Notes list sidebar widget with search functionality."""

import logging
from typing import List, Optional

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QPushButton,
    QLabel,
    QMenu,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QAction

from ..core.note import Note
from .note_list_item import NoteListItem

logger = logging.getLogger(__name__)


class NotesList(QWidget):
    """Notes list sidebar with search and management.

    Displays a scrollable list of notes with search functionality
    and smooth selection transitions.

    Signals:
        note_selected: Emitted when a note is selected (passes Note)
        new_note_requested: Emitted when user requests new note
        delete_note_requested: Emitted when user requests delete (passes note_id)
    """

    note_selected = pyqtSignal(Note)
    new_note_requested = pyqtSignal()
    delete_note_requested = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize notes list.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._notes: List[Note] = []
        self._setup_ui()
        self._connect_signals()
        logger.info("Notes list initialized")

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Header with title and new note button
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        title_label = QLabel("Notes")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        new_note_btn = QPushButton("+")
        new_note_btn.setToolTip("New Note (Ctrl+N)")
        new_note_btn.setMaximumWidth(36)
        new_note_btn.setMaximumHeight(36)
        new_note_btn.clicked.connect(self.new_note_requested.emit)
        new_note_btn.setProperty("primary", True)
        header_layout.addWidget(new_note_btn)

        layout.addLayout(header_layout)

        # Search bar
        self._search_box = QLineEdit()
        self._search_box.setPlaceholderText("Search notes...")
        self._search_box.setClearButtonEnabled(True)
        layout.addWidget(self._search_box)

        # Notes list
        self._list_widget = QListWidget()
        self._list_widget.setSpacing(2)
        self._list_widget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        layout.addWidget(self._list_widget)

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self._list_widget.itemClicked.connect(self._on_item_clicked)
        self._search_box.textChanged.connect(self._on_search_changed)
        self._list_widget.customContextMenuRequested.connect(
            self._show_context_menu
        )

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        """Handle item click.

        Args:
            item: Clicked item
        """
        if isinstance(item, NoteListItem):
            self.note_selected.emit(item.note)
            logger.debug(f"Note selected: {item.note.id}")

    def _on_search_changed(self, text: str) -> None:
        """Handle search text change.

        Args:
            text: Search query
        """
        query = text.lower().strip()

        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if isinstance(item, NoteListItem):
                matches = (
                    query in item.note.title.lower() or
                    query in item.note.content.lower()
                )
                item.setHidden(not matches if query else False)

    def _show_context_menu(self, position) -> None:
        """Show context menu for note operations.

        Args:
            position: Position where context menu was requested
        """
        item = self._list_widget.itemAt(position)
        if not isinstance(item, NoteListItem):
            return

        menu = QMenu(self)

        # Delete action
        delete_action = QAction("Delete Note", self)
        delete_action.triggered.connect(
            lambda: self.delete_note_requested.emit(item.note.id)
        )
        menu.addAction(delete_action)

        # Show menu at cursor position
        menu.exec(self._list_widget.mapToGlobal(position))

    def set_notes(self, notes: List[Note]) -> None:
        """Set the list of notes.

        Args:
            notes: List of notes to display
        """
        self._notes = notes
        self._refresh_list()
        logger.info(f"Notes list updated with {len(notes)} notes")

    def add_note(self, note: Note) -> None:
        """Add a note to the list.

        Args:
            note: Note to add
        """
        self._notes.insert(0, note)
        item = NoteListItem(note)
        self._list_widget.insertItem(0, item)
        logger.debug(f"Note added to list: {note.id}")

    def update_note(self, note: Note) -> None:
        """Update a note in the list.

        Args:
            note: Updated note
        """
        for i, n in enumerate(self._notes):
            if n.id == note.id:
                self._notes[i] = note
                item = self._list_widget.item(i)
                if isinstance(item, NoteListItem):
                    item.update_note(note)
                logger.debug(f"Note updated in list: {note.id}")
                break

    def remove_note(self, note_id: str) -> None:
        """Remove a note from the list.

        Args:
            note_id: ID of note to remove
        """
        self._notes = [n for n in self._notes if n.id != note_id]

        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if isinstance(item, NoteListItem) and item.note.id == note_id:
                self._list_widget.takeItem(i)
                logger.debug(f"Note removed from list: {note_id}")
                break

    def select_note(self, note_id: str) -> None:
        """Select a note by ID.

        Args:
            note_id: ID of note to select
        """
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if isinstance(item, NoteListItem) and item.note.id == note_id:
                self._list_widget.setCurrentItem(item)
                logger.debug(f"Note selected programmatically: {note_id}")
                break

    def get_selected_note(self) -> Optional[Note]:
        """Get currently selected note.

        Returns:
            Selected note or None
        """
        item = self._list_widget.currentItem()
        if isinstance(item, NoteListItem):
            return item.note
        return None

    def _refresh_list(self) -> None:
        """Refresh the entire list display."""
        self._list_widget.clear()
        for note in self._notes:
            item = NoteListItem(note)
            self._list_widget.addItem(item)

    def clear_search(self) -> None:
        """Clear the search box."""
        self._search_box.clear()
