"""Note data model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Note:
    """Represents a single note with metadata.

    Attributes:
        id: Unique identifier for the note
        title: Note title (derived from first line of content)
        content: Rich text content (HTML format)
        created_at: Timestamp when note was created
        modified_at: Timestamp when note was last modified
        is_favorite: Whether note is marked as favorite
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Untitled"
    content: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    is_favorite: bool = False

    def update_content(self, content: str) -> None:
        """Update note content and refresh metadata.

        Args:
            content: New content for the note (HTML format)
        """
        self.content = content
        self.modified_at = datetime.now()
        self.title = self._extract_title(content)

    def _extract_title(self, content: str) -> str:
        """Extract title from content (first line, plain text).

        Args:
            content: HTML content

        Returns:
            Extracted title or 'Untitled' if content is empty
        """
        if not content or not content.strip():
            return "Untitled"

        # Use QTextDocument to properly convert HTML to plain text
        from PyQt6.QtGui import QTextDocument
        doc = QTextDocument()
        doc.setHtml(content)
        plain_text = doc.toPlainText().strip()

        if not plain_text:
            return "Untitled"

        # Get first line or first 50 characters
        first_line = plain_text.split('\n')[0]
        title = first_line[:50]

        if len(first_line) > 50:
            title += "..."

        return title or "Untitled"

    def to_dict(self) -> dict:
        """Convert note to dictionary for serialization.

        Returns:
            Dictionary representation of the note
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "is_favorite": self.is_favorite,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Note":
        """Create note from dictionary.

        Args:
            data: Dictionary containing note data

        Returns:
            Note instance
        """
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", "Untitled"),
            content=data.get("content", ""),
            created_at=datetime.fromisoformat(data["created_at"])
                if "created_at" in data else datetime.now(),
            modified_at=datetime.fromisoformat(data["modified_at"])
                if "modified_at" in data else datetime.now(),
            is_favorite=data.get("is_favorite", False),
        )
