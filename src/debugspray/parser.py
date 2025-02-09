from debugspray.models import Issue
from markdown_it import MarkdownIt


def parse_markdown_issue(markdown_text: str) -> Issue:
    md = MarkdownIt()
    tokens = md.parse(markdown_text)

    data = {}
    current_section = None
    title_parsed = False

    for token in tokens:
        # Parse Title (First H1 `#` heading)
        if token.type == "heading_open" and token.tag == "h1" and not title_parsed:
            title_parsed = True  # Mark title as parsed
        elif token.type == "inline" and title_parsed and "title" not in data:
            data["title"] = token.content.strip()

        # Parse Sections (### H3 headings)
        elif token.type == "heading_open" and token.tag == "h3":
            current_section = None  # Reset before detecting new section
        elif token.type == "inline" and current_section is None:
            section_title = token.content.strip().lower().replace(" ", "_")
            current_section = section_title  # Set active section
            data[current_section] = ""
        elif token.type == "inline" and current_section:
            data[current_section] = token.content.strip()
        elif token.type == "fence" and current_section:  # Handles logs (code block)
            data[current_section] = token.content.strip()

    return Issue(**data)
