def clean_string(s: str, name: bool = False):
    s = s.strip()
    if name:
        return s.title()
    return s
