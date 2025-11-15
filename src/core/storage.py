"""Storage manager for persisting notes to disk."""

import json
import logging
from pathlib import Path
from typing import List, Optional

from .note import Note

logger = logging.getLogger(__name__)


class StorageManager:
    """Manages note persistence using JSON files.

    Each note is stored in a separate JSON file in the notes directory.
    This provides simple, human-readable storage with good performance.

    Attributes:
        storage_dir: Directory where notes are stored
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize storage manager.

        Args:
            storage_dir: Directory to store notes. Defaults to ./notes
        """
        if storage_dir is None:
            storage_dir = Path.cwd() / "notes"

        self.storage_dir = Path(storage_dir)
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists."""
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Storage directory initialized at {self.storage_dir}")
        except Exception as e:
            logger.error(f"Failed to create storage directory: {e}")
            raise

    def save_note(self, note: Note) -> bool:
        """Save a note to disk.

        Args:
            note: Note to save

        Returns:
            True if save was successful, False otherwise
        """
        try:
            file_path = self.storage_dir / f"{note.id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(note.to_dict(), f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved note {note.id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save note {note.id}: {e}")
            return False

    def load_note(self, note_id: str) -> Optional[Note]:
        """Load a note from disk.

        Args:
            note_id: ID of the note to load

        Returns:
            Note instance or None if not found/error
        """
        try:
            file_path = self.storage_dir / f"{note_id}.json"
            if not file_path.exists():
                logger.warning(f"Note {note_id} not found")
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Note.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to load note {note_id}: {e}")
            return None

    def load_all_notes(self) -> List[Note]:
        """Load all notes from disk.

        Returns:
            List of all notes, sorted by modification time (newest first)
        """
        notes = []
        try:
            for file_path in self.storage_dir.glob("*.json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    note = Note.from_dict(data)
                    notes.append(note)
                except Exception as e:
                    logger.error(f"Failed to load note from {file_path}: {e}")
                    continue

            # Sort by modification time, newest first
            notes.sort(key=lambda n: n.modified_at, reverse=True)
            logger.info(f"Loaded {len(notes)} notes")
            return notes
        except Exception as e:
            logger.error(f"Failed to load notes: {e}")
            return []

    def delete_note(self, note_id: str) -> bool:
        """Delete a note from disk.

        Args:
            note_id: ID of the note to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            file_path = self.storage_dir / f"{note_id}.json"
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted note {note_id}")
                return True
            else:
                logger.warning(f"Note {note_id} not found for deletion")
                return False
        except Exception as e:
            logger.error(f"Failed to delete note {note_id}: {e}")
            return False

    def get_note_count(self) -> int:
        """Get total number of notes.

        Returns:
            Number of notes in storage
        """
        try:
            return len(list(self.storage_dir.glob("*.json")))
        except Exception as e:
            logger.error(f"Failed to count notes: {e}")
            return 0
