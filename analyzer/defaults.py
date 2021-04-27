from django.conf import settings

hash_table = {
    "ALLOW_FILE_ATTACHMENTS": True,
    "COMMENT_CLASSES": [],
    "DEFAULT_ASSIGNEE": None,
    "LIMIT_FILE_ATTACHMENTS": [".pdf"],
    "MAXIMUM_ATTACHMENT_SIZE": 5000000,
    "MAXIMUM_ATTACHMENT_FILES": 3,
    "PUBLIC_SUBMIT_REDIRECT": "/",
    "STAFF_ONLY": False,
}


def defaults(key: str):
    """Try to get a setting from project settings.
    If empty or doesn't exist, fall back to a value from defaults hash."""

    if hasattr(settings, key):
        val = getattr(settings, key)
    else:
        val = hash_table.get(key)
    return val
