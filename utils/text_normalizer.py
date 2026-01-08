"""Text normalization utilities for searching and comparison."""
import unicodedata
from typing import Literal


class TextNormalizer:
    """Normalize text for accent-insensitive comparison."""
    
    ENCODING_ASCII: Literal["ascii"] = "ascii"
    ENCODING_UTF8: Literal["utf-8"] = "utf-8"
    NORMALIZATION_FORM: Literal["NFD"] = "NFD"
    IGNORE_ERRORS: Literal["ignore"] = "ignore"
    
    @staticmethod
    def normalize_for_search(text: str) -> str:
        """Remove accents and convert to lowercase for searching."""
        normalized: str = unicodedata.normalize(
            TextNormalizer.NORMALIZATION_FORM, 
            text
        )
        ascii_text: bytes = normalized.encode(
            TextNormalizer.ENCODING_ASCII, 
            TextNormalizer.IGNORE_ERRORS
        )
        return ascii_text.decode(TextNormalizer.ENCODING_UTF8).lower()