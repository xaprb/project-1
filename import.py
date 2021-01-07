from pathlib import Path
import os
import json
import csv
import requests

CSV_FILES = {
    "1860_census_free_blacks": "1kJaSr0Aota8Hp59_aLo8ElKiQFSKP20w",
    "free_blacks_rockbridge_county": "1LCrMNdAevfAT8n6YvcX2exVaRV8rsxmiZ-E--BggGi0"
}

for key, url in CSV_FILES.items():
    directory = "content/" + key + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Delete old page files. Leave the _index.md file there.
    for f in os.listdir(directory):
        if not f.startswith("_") and f.endswith(".md"):
            os.remove(directory + f)

    # with open('census.csv', newline='') as csvfile:
    #   reader = csv.DictReader(csvfile)
    #   for row in reader:
    i = 0
    with requests.get("https://docs.google.com/spreadsheets/d/" + url + "/export?format=csv", stream=True) as r:
        if r.status_code >= 400:
            print("Error accessing", key, r.raise_for_status())
            continue
        lines = (line.decode('utf-8') for line in r.iter_lines())
        for row in csv.DictReader(lines):
            i = i + 1
            # row["id"] = str(i)
            row["title"] = row["First Name"] + " " + row["Surname"]
            new_page = open(os.path.join(directory, str(i) + ".md"), 'w')
            new_page.write(json.dumps(row, indent=1)+"\n\n")
            new_page.close()
