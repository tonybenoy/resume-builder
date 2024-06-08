import os
from turtle import title
from builder import build_resume
from parse_job import get_job_details_linkedin
import json
import tempfile
import subprocess
import pyperclip

url = input("Enter the linkedin URL(Press enter to enter manually): ")
if url == "":
    title=input("Enter the job title: ")
    org_name=input("Enter the organization name: ")
    job_description=input("Enter the job description: ")
    url = input("Enter the job URL: ")
    result={"job_title":title,"org_name":org_name,"job_description":job_description,"url":url}
else:
    result=get_job_details_linkedin(url)
with open('./tailor.json') as f:
    tailor_data = json.load(f)
with open('./prompt.json') as f:
    prompt = json.load(f)

resume_prompt = prompt["resume"]
prompt_final =f"{resume_prompt}.The job title is '{result['job_title']}' at {result['org_name']}. The job description is: {result['job_description']}. The data to tailor is{ tailor_data}"
pyperclip.copy(prompt_final)
print("Prompt copied to clipboard")
def get_text_from_editor():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_filename = tmp_file.name

    if os.name == 'nt':  # For Windows
        editor = os.environ.get('EDITOR', 'notepad.exe')
    elif os.name == 'posix':  # For macOS and Linux
        editor = os.environ.get('EDITOR', 'nano')

    subprocess.call([editor, tmp_filename])

    with open(tmp_filename, 'r') as tmp_file:
        content = tmp_file.read()

    os.remove(tmp_filename)

    return content
tailored_json = get_text_from_editor()
tailor_data.update(json.loads(tailored_json))
path = f"resumes/{result['org_name']}/{result['job_title']}"
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

build_resume(tailor_data, path)

print(f"Resume generated at {path}")
notes = input("Enter any notes you want to save: ")
with open(f"{path}/notes.txt", "w") as f:
    f.write(notes)
cl=input("Generate cover letter? (y/N)")
if cl.lower() == "y":
    pyperclip.copy(resume_prompt["cover_letter"])
    print("Prompt copied to clipboard")
    cover_letter = get_text_from_editor()
    with open(f"{path}/cover_letter.txt", "w") as f:
        f.write(cover_letter)
    print(f"Cover letter generated at {path}")
