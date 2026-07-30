import logging
import uuid
from typing import Literal

import httpx

from app.database import connection as _db

logger = logging.getLogger(__name__)
LicenseStatus = Literal["OPEN", "NEEDS_REVIEW", "UNKNOWN"]


def _search_web(query: str) -> list[dict]:
    results = []
    try:
        resp = httpx.get(
            "https://api.duckduckgo.com",
            params={"q": query, "format": "json"},
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            for topic in data.get("RelatedTopics", []):
                if "Text" in topic and "FirstURL" in topic:
                    results.append(
                        {
                            "title": topic.get("Text", ""),
                            "url": topic.get("FirstURL", ""),
                            "source": "duckduckgo",
                        }
                    )
    except httpx.RequestError as e:
        logger.warning("Web search failed: %s", e)
    return results


def stage_media_for_concept(
    concept_id: str,
    media_type: Literal["IMAGE", "GIF"],
    source_url: str,
    license_status: LicenseStatus = "UNKNOWN",
) -> str:
    media_id = str(uuid.uuid4())
    with _db.authoring_db() as conn:
        conn.execute(
            "INSERT INTO concept_media (media_id, concept_id, media_type, source_url, license_status, admin_approved) VALUES (?, ?, ?, ?, ?, 0)",
            (media_id, concept_id, media_type, source_url, license_status),
        )
    return media_id


def search_and_stage_concept_media(concept_id: str, concept_title: str) -> list[dict]:
    results = _search_web(f"{concept_title} diagram illustration")
    staged = []
    for r in results[:5]:
        media_id = stage_media_for_concept(
            concept_id=concept_id,
            media_type="IMAGE",
            source_url=r["url"],
        )
        staged.append({"media_id": media_id, **r})
    return staged


def approve_media(media_id: str) -> None:
    with _db.authoring_db() as conn:
        conn.execute(
            "UPDATE concept_media SET admin_approved = 1 WHERE media_id = ?",
            (media_id,),
        )


def reject_media(media_id: str) -> None:
    with _db.authoring_db() as conn:
        conn.execute(
            "DELETE FROM concept_media WHERE media_id = ?", (media_id,)
        )
