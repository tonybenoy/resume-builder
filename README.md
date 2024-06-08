# Resume Builder
This is a simple resume builder that takes in a JSON files and outputs a PDF resume. The `resume_data.json` file contains all the personal information such as contact information, education and projects. The assumption is that this information does not need to be tailored for each job application. `tailor.json` file contains the information that needs to be tailored for each job application such as summary, work experience etc.

## Usage
1. Clone the repository
```bash
git clone git@github.com:tonybenoy/resume-builder.git
```
2. Install the dependencies
```bash
pip install -r requirements.txt
```
3. Make the `resume_data.json` and `tailor.json` files with the required information. Use the sample files as a reference. Add your prompts to `prompts.json` file.
4. Run the script
```bash
python main.py
```
5. Follow theinstructions to generate the resume.
6. The prompts will be copied to the clipboard and can be passed to LLM of your choice. Make sure that your prompt asks for a json. Paste the json value in the editor(Edit as needed) and save.
7. The generated resume will be saved in the `resume` folder.
## Custom templates
You can convert your resume template to a jinja2 template with the help of an LLM model. I found passing the image more useful than the pdf but your results may vary. Passing the template here as reference for the model should give your a custom template for your resume.
