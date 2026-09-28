import hashlib
import time
from typing import Tuple, Dict, Any, List

class SpamAndDuplicateDetector:
    """
    Guards the citizen demand analytics pipeline against spam, coordinated duplicate botting,
    and abuse from distorting hotspot counts.
    """

    def __init__(self):
        # Cache for deduplication: fingerprint -> list of submission timestamps
        self._submission_cache: Dict[str, List[float]] = {}
        # Rate limit thresholds
        self.MAX_IDENTICAL_SUBMISSIONS = 3
        self.WINDOW_SECONDS = 300  # 5 minutes
        self.ABUSIVE_KEYWORDS = [
            "free crypto", "buy followers", "click here", "lottery winner",
            "casino", "earn money online fast", "test spam 123", "fake fake fake"
        ]

    def _generate_fingerprint(self, text: str, sender_id: str) -> str:
        # Normalize text: strip punctuation, lowercase, collapse whitespace
        normalized = "".join(ch.lower() for ch in text if ch.isalnum() or ch.isspace())
        normalized = " ".join(normalized.split())
        return hashlib.sha256(f"{normalized}".encode("utf-8")).hexdigest()

    def check_request(self, text: str, sender_id: str) -> Tuple[bool, float, str]:
        """
        Returns: (is_flagged, spam_score, reason)
        spam_score: 0.0 (completely clean) to 1.0 (confirmed spam)
        """
        if not text or len(text.strip()) < 8:
            return True, 0.95, "Text too short or empty to constitute meaningful civic demand."

        # Check abusive keywords
        text_lower = text.lower()
        for kw in self.ABUSIVE_KEYWORDS:
            if kw in text_lower:
                return True, 0.90, f"Contains commercial or promotional spam pattern: '{kw}'"

        # Check repetitive spamming / bot flood
        fingerprint = self._generate_fingerprint(text, sender_id)
        now = time.time()
        
        # Clean older entries
        if fingerprint in self._submission_cache:
            timestamps = [t for t in self._submission_cache[fingerprint] if now - t < self.WINDOW_SECONDS]
            self._submission_cache[fingerprint] = timestamps
            if len(timestamps) >= self.MAX_IDENTICAL_SUBMISSIONS:
                return True, 0.85, f"Duplicate surge detected ({len(timestamps)} identical submissions in 5 mins). Throttled to prevent hotspot distortion."
            self._submission_cache[fingerprint].append(now)
        else:
            self._submission_cache[fingerprint] = [now]

        # Check repeated character spam (e.g., 'aaaaaaa' or '!!!!!!!')
        for word in text.split():
            if len(word) > 15 and len(set(word)) <= 2:
                return True, 0.80, "Repetitive character gibberish detected."

        return False, 0.05, "Clean validated civic demand submission."


spam_detector = SpamAndDuplicateDetector()
