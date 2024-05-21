import json

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Load the JSON data
with open('./resume_data.json') as f:
    resume_data = json.load(f)
with open('./tailor.json') as f:
    tailor_data = json.load(f)
resume_data.update(tailor_data)
# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('resume_template.html')

# Render the HTML with the JSON data
html_content = template.render(**resume_data)

# Save HTML content to a file
html_file_path = './resume.html'
with open(html_file_path, 'w') as f:
    f.write(html_content)

# Convert HTML to PDF using WeasyPrint
pdf_file_path = './resume.pdf'
HTML(html_file_path).write_pdf(pdf_file_path)

print("PDF generated successfully.")
