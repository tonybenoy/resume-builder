import json
import os
import platform
import subprocess
from typing import Optional

import pyperclip
import typer
from pathvalidate import sanitize_filename
from typing_extensions import Annotated

from utils.builder import build_old, build_resume
from utils.parse_job import get_job_details
from utils.utils import get_text_from_editor

app = typer.Typer()


@app.command()
def main(
    url: Annotated[Optional[str], typer.Argument()] = None,
    html: Annotated[str, typer.Option(help="Path to custom template html with jinja2 placeholders")] = "",
    resume: Annotated[str, typer.Option(help="Path to custom resume data json file")] = "",
    tailor: Annotated[str, typer.Option(help="Path to custom tailor json file")] = "",
    prompt: Annotated[str, typer.Option(help="Path to custom prompt json file")] = "",
):
    if not url:
        title = input("Enter the job title: ")
        org_name = input("Enter the organization name: ")
        typer.echo("Enter the job description in the text editor. Save and exit. Press enter to continue.")
        input()
        job_description = get_text_from_editor()
        url = input("Enter the job URL: ")
        result = {"job_title": title, "org_name": org_name, "job_description": job_description, "url": url}
    else:
        result = get_job_details(url)
    with open("./tailor.json" if tailor == "" else tailor) as f:
        tailor_data = json.load(f)
    with open("./prompt.json" if prompt == "" else prompt) as f:
        prompt_json = json.load(f)

    resume_prompt = prompt_json["resume"]
    prompt_final = f"{resume_prompt}.The job title is '{result['job_title']}' at {result['org_name']}. The job description is: {result['job_description']}. GO the company's website, careers page and information and also the job description page. Use that infomration to make resume more appropriate.The data to tailor is{ tailor_data}. The data is in json form and has the skills,experiene and the summary. Return the same json and add no extra keys such as education etc as they are handled externally."
    pyperclip.copy(prompt_final)
    typer.echo(
        "Prompt is copied to the clipboard. Enter the JSON from the model in the text editor. Save and exit. Press enter to continue."
    )
    input()
    tailored_json = get_text_from_editor()
    tailor_data.update(json.loads(tailored_json))
    path = f"resumes/{sanitize_filename(result['org_name'])}/{sanitize_filename(result['job_title'])}"
    try:
        os.mkdir("resumes")
    except FileExistsError:
        pass
    try:
        os.mkdir(f"resumes/{result['org_name']}")
    except FileExistsError:
        pass

    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    with open(f"{path}/tailor.json", "w") as f:
        json.dump(tailor_data, f)
    with open(f"{path}/jd.json", "w") as f:
        json.dump(result, f)

    build_resume(tailor_data, path, html)

    print(f"Resume generated at {path}")
    notes = input("Enter any notes you want to save: ")
    with open(f"{path}/notes.txt", "w") as f:
        f.write(notes)
    cl = input("Generate cover letter? (y/N)")
    if cl.lower() == "y":
        pyperclip.copy(prompt_json["cover_letter"])
        print("Prompt copied to clipboard")
        cover_letter = get_text_from_editor()
        with open(f"{path}/cover_letter.txt", "w") as f:
            f.write(cover_letter)
        print(f"Cover letter generated at {path}")
    resume = f"{path}/resume.pdf"
    cover_letter = f"{path}/cover_letter.txt"

    if platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", resume])
        if cl.lower() == "y":
            subprocess.Popen(["open", cover_letter])
    elif platform.system() == "Windows":  # Windows
        subprocess.Popen(["start", resume], shell=True)
        if cl.lower() == "y":
            subprocess.Popen(["start", cover_letter], shell=True)
    else:  # Linux and other Unix-like systems
        subprocess.Popen(["xdg-open", resume])
        if cl.lower() == "y":
            subprocess.Popen(["xdg-open", cover_letter])


@app.command()
def build(path=Annotated[str, typer.Argument(help="Path to resume data json file")]):
    if not os.path.exists(path):
        raise typer.BadParameter(f"File {path} does not exist")
    build_old(path)


if __name__ == "__main__":
    import sys

    from typer.main import get_command, get_command_name

    if len(sys.argv) == 1 or sys.argv[1] not in [get_command_name(key) for key in get_command(app).commands.keys()]:
        sys.argv.insert(1, "main")
    app()
