"""Helpers for validating uploaded image files."""
from __future__ import annotations

from fastapi import UploadFile

from app.core.exceptions import ImageTooLargeError, InvalidImageError

ALLOWED_IMAGE_CONTENT_TYPES: frozenset[str] = frozenset(
    {"image/jpeg", "image/png", "image/webp"}
)


async def read_validated_image(upload: UploadFile, *, max_size_bytes: int) -> bytes:
    """Validate an uploaded image and return its raw bytes.

    Args:
        upload: the multipart file received by the endpoint.
        max_size_bytes: maximum accepted file size.

    Raises:
        InvalidImageError: unsupported content type or empty file.
        ImageTooLargeError: file larger than `max_size_bytes`.

    Note:
        Only content type and size are checked here. Decoding the image (and
        rejecting corrupted files) happens in the ML pre-processing step
        (OpenCV/Pillow) during the ML Integration task.
    """
    if upload.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_CONTENT_TYPES))
        raise InvalidImageError(
            f"Unsupported image type '{upload.content_type}'. Allowed types: {allowed}."
        )

    # Read at most max_size_bytes + 1 so oversized uploads are detected
    # without ever loading the whole file into memory.
    data = await upload.read(max_size_bytes + 1)

    if not data:
        raise InvalidImageError("The uploaded file is empty.")

    if len(data) > max_size_bytes:
        raise ImageTooLargeError(
            f"The image exceeds the maximum allowed size of {max_size_bytes // (1024 * 1024)} MB."
        )

    return data