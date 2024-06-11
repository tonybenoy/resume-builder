import json

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


# Load the JSON data
def build_resume(tailor_data, path):
    with open("./resume_data.json") as f:
        resume_data = json.load(f)
    # with open('./tailor.json') as f:
    #     tailor_data = json.load(f)
    resume_data.update(tailor_data)
    # Set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("resume_template.html")

    # Render the HTML with the JSON data
    html_content = template.render(**resume_data)

    # Save HTML content to a file
    html_file_path = f"{path}/resume.html"
    with open(html_file_path, "w") as f:
        f.write(html_content)

    # Convert HTML to PDF using WeasyPrint
    pdf_file_path = f"{path}/resume.pdf"
    HTML(html_file_path).write_pdf(pdf_file_path)

    print("PDF generated successfully.")


def build_old(path):
    with open(f"{path}/tailor.json") as f:
        tailor_data = json.load(f)
    build_resume(tailor_data, path)


if __name__ == "__main__":
    path = input("Enter the path of the resume folder: ")
    build_old(path)
