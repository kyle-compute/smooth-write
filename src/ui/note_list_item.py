"""Note list item widget."""

from datetime import datetime, timedelta

from PyQt6.QtWidgets import QListWidgetItem

from ..core.note import Note


class NoteListItem(QListWidgetItem):
    """Custom list item for notes.

    Stores note reference and displays formatted preview.
    """

    def __init__(self, note: Note):
        """Initialize note list item.

        Args:
            note: Note instance
        """
        super().__init__()
        self.note = note
        self._update_display()

    def _update_display(self) -> None:
        """Update item display text."""
        preview = self._get_preview()
        time_str = self._format_time()
        display_text = f"{self.note.title}\n{preview}\n{time_str}"
        self.setText(display_text)

    def _get_preview(self) -> str:
        """Get preview text from note content.

        Returns:
            Preview text (first 60 chars of content)
        """
        # Use QTextDocument to properly convert HTML to plain text
        from PyQt6.QtGui import QTextDocument
        doc = QTextDocument()
        doc.setHtml(self.note.content)
        plain = doc.toPlainText().strip()

        # Get first line that's not the title
        lines = plain.split('\n')
        preview_text = ""

        for line in lines:
            line = line.strip()
            if line and line != self.note.title:
                preview_text = line
                break

        if not preview_text:
            preview_text = "No additional text"

        # Truncate to 60 characters
        if len(preview_text) > 60:
            preview_text = preview_text[:60] + "..."

        return preview_text

    def _format_time(self) -> str:
        """Format modification time as relative string.

        Returns:
            Relative time string (e.g., "2 hours ago")
        """
        now = datetime.now()
        delta = now - self.note.modified_at

        if delta < timedelta(minutes=1):
            return "Just now"
        elif delta < timedelta(hours=1):
            mins = int(delta.total_seconds() / 60)
            return f"{mins} min{'s' if mins > 1 else ''} ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta < timedelta(days=7):
            days = delta.days
            return f"{days} day{'s' if days > 1 else ''} ago"
        else:
            return self.note.modified_at.strftime("%b %d, %Y")

    def update_note(self, note: Note) -> None:
        """Update the associated note.

        Args:
            note: Updated note instance
        """
        self.note = note
        self._update_display()
