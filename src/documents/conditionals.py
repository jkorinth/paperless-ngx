from datetime import datetime
from typing import Optional

from django.conf import settings
from django.core.cache import cache

from documents.caching import CACHE_5_MINUTES
from documents.caching import CLASSIFIER_HASH_KEY
from documents.caching import CLASSIFIER_MODIFIED_KEY
from documents.caching import CLASSIFIER_VERSION_KEY
from documents.classifier import DocumentClassifier
from documents.models import Document


def suggestions_etag(request, pk: int) -> Optional[str]:
    """
    Returns an optional string for the ETag, allowing browser caching of
    suggestions if the classifier has not been changed and the suggested dates
    setting is also unchanged

    TODO: It would be nice to not duplicate the partial loading and the loading
    between here and the actual classifier
    """
    if not settings.MODEL_FILE.exists():
        return None
    cache_hits = cache.get_many(
        [CLASSIFIER_VERSION_KEY, CLASSIFIER_HASH_KEY],
    )
    if (
        CLASSIFIER_VERSION_KEY in cache_hits
        and cache_hits[CLASSIFIER_VERSION_KEY] != DocumentClassifier.FORMAT_VERSION
    ):
        return None
    elif CLASSIFIER_HASH_KEY in cache_hits:
        cache.touch(CLASSIFIER_HASH_KEY, CACHE_5_MINUTES)
        return f"{cache_hits[CLASSIFIER_HASH_KEY]}:{settings.NUMBER_OF_SUGGESTED_DATES}"
    return None


def suggestions_last_modified(request, pk: int) -> Optional[datetime]:
    """
    Returns the datetime of classifier last modification.  This is slightly off,
    as there is not way to track the suggested date setting modification, but it seems
    unlikely that changes too often
    """
    if not settings.MODEL_FILE.exists():
        return None
    cache_hits = cache.get_many(
        [CLASSIFIER_VERSION_KEY, CLASSIFIER_MODIFIED_KEY],
    )
    if (
        CLASSIFIER_VERSION_KEY in cache_hits
        and cache_hits[CLASSIFIER_VERSION_KEY] != DocumentClassifier.FORMAT_VERSION
    ):
        return None
    elif CLASSIFIER_MODIFIED_KEY in cache_hits:
        cache.touch(CLASSIFIER_MODIFIED_KEY, CACHE_5_MINUTES)
        return cache_hits[CLASSIFIER_MODIFIED_KEY]
    return None


def metadata_etag(request, pk: int) -> Optional[str]:
    """
    Metadata is extracted from the original file, so use its checksum as the
    ETag
    """
    try:
        doc = Document.objects.get(pk=pk)
        return doc.checksum
    except Document.DoesNotExist:
        return None
    return None


def metadata_last_modified(request, pk: int) -> Optional[datetime]:
    """
    Metadata is extracted from the original file, so use its modified.  Strictly speaking, this is
    not the modification of the original file, but of the database object, but might as well
    error on the side of more cautious
    """
    try:
        doc = Document.objects.get(pk=pk)
        return doc.modified
    except Document.DoesNotExist:
        return None
    return None


def preview_etag(request, pk: int) -> Optional[str]:
    """
    ETag for the document preview, using the original or archive checksum, depending on the request
    """
    try:
        doc = Document.objects.get(pk=pk)
        use_original = (
            "original" in request.query_params
            and request.query_params["original"] == "true"
        )
        return doc.checksum if use_original else doc.archive_checksum
    except Document.DoesNotExist:
        return None
    return None
