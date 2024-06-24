import json

tailor_json = json.load(open("tailor.json"))
resume_data = json.load(open("resume_data.json"))


def convert_to_jsonresume(tailor_json, resume_data):
    jsonresume = {
        "basics": {
            "name": resume_data["header"]["name"],
            "label": tailor_json["title"],
            "email": resume_data["header"]["email"],
            "phone": resume_data["header"]["phone"],
            "location": {"address": resume_data["header"]["location"]},
            "profiles": [
                {
                    "network": "LinkedIn",
                    "username": resume_data["header"]["linkedin"].split("/")[-1],
                    "url": resume_data["header"]["linkedin"],
                },
                {
                    "network": "GitHub",
                    "username": resume_data["header"]["github"].split("/")[-1],
                    "url": resume_data["header"]["github"],
                },
            ],
            "summary": tailor_json["summary"],
        },
        "work": [
            {
                "name": exp["company"],
                "position": exp["title"],
                "location": exp["location"],
                "startDate": exp["dates"].split(" — ")[0],
                "endDate": exp["dates"].split(" — ")[1],
                "highlights": exp["details"],
            }
            for exp in tailor_json["experience"]
        ],
        "education": [
            {
                "institution": edu["institution"],
                "area": edu["degree"],
                "location": edu["location"],
                "startDate": edu["dates"].split(" — ")[0],
                "endDate": edu["dates"].split(" — ")[1],
            }
            for edu in resume_data["education"]
        ],
        "skills": [{"name": skill["category"], "keywords": skill["skill"]} for skill in tailor_json["skills"]],
        "projects": [
            {"name": project["name"], "description": " ".join(project["description"]), "url": project["link"]}
            for project in tailor_json["projects"]
        ]
        if "projects" in tailor_json
        else [],
    }

    return jsonresume


# Convert the input data
jsonresume_data = convert_to_jsonresume(tailor_json, resume_data)


def save_jsonresume(path_to_file, jsonresume_data):
    with open(path_to_file, "w") as f:
        json.dump(jsonresume_data, f)


# Save to file
save_jsonresume("jsonresume.json", jsonresume_data)
# Print the result in json format
print(json.dumps(jsonresume_data, indent=4))
