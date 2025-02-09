from debugspray.models import Issue


def parse_markdown_issue(markdown: str) -> Issue:
    sections = re.split(r"###\s+", markdown)
    data = {}

    for section in sections[1:]:  # Skip the first empty split
        lines = section.strip().split("\n", 1)
        title = lines[0].strip().lower().replace(" ", "_")
        content = lines[1].strip() if len(lines) > 1 else ""

        # Special handling for logs to remove triple backticks
        if title == "logs":
            content = re.sub(r"```[\s\S]*?```", lambda m: m.group(0).strip("```").strip(), content)

    return BugReport(**data)