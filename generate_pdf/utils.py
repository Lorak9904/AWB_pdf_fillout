import textwrap

def wrap_text(text, max_width=40, max_lines=3):
    wrapped_lines = textwrap.wrap(text, width=max_width)

    if len(wrapped_lines) > max_lines:
        wrapped_lines = wrapped_lines[:max_lines]
        wrapped_lines[-1] = wrapped_lines[-1][:max_width - 3] + "..."

    return wrapped_lines