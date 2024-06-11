import os
import subprocess
import tempfile


def get_text_from_editor():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_filename = tmp_file.name

    if os.name == "nt":  # For Windows
        editor = os.environ.get("EDITOR", "notepad.exe")
    elif os.name == "posix":  # For macOS and Linux
        editor = os.environ.get("EDITOR", "vim")

    subprocess.call([editor, tmp_filename])

    with open(tmp_filename, "r") as tmp_file:
        content = tmp_file.read()

    os.remove(tmp_filename)

    return content
