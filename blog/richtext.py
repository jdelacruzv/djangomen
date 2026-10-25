import nh3


RICH_TEXT_TAGS = {
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "del",
    "em",
    "h2",
    "h3",
    "hr",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "strong",
    "u",
    "ul",
}


def sanitize_rich_text(value):
    return nh3.clean(
        value or "",
        tags=RICH_TEXT_TAGS,
        attributes={"a": {"href", "title"}},
        clean_content_tags={"iframe", "object", "script", "style"},
    )
