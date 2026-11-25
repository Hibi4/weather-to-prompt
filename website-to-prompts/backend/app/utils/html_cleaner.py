from bs4 import BeautifulSoup, Comment

def clean_html(raw_html: str, max_length: int = 20000) -> str:
    """
    Removes scripts, styles, SVGs, and clutter from raw HTML
    to optimize token usage for the LLM.
    """
    soup = BeautifulSoup(raw_html, "html.parser")

    # 1. Remove useless/heavy tags
    noisy_tags = [
        "script", "style", "svg", "noscript", "iframe",
        "meta", "link", "path", "canvas", "video"
    ]
    for tag in soup(noisy_tags):
        tag.decompose()

    # 2. Remove HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # 3. Strip noisy attributes (keep only structural ones)
    allowed_attrs = {"id", "class", "href", "type", "placeholder", "role", "aria-label"}
    for tag in soup.find_all(True):
        attrs = dict(tag.attrs)
        for attr in attrs:
            if attr not in allowed_attrs:
                del tag.attrs[attr]

    # 4. Collapse whitespace and truncate to fit context window
    cleaned_text = soup.prettify()
    lines = [line.strip() for line in cleaned_text.splitlines() if line.strip()]
    compact_html = "\n".join(lines)

    return compact_html[:max_length]