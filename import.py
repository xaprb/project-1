from pathlib import Path
import os
import json
import csv
import requests

CSV_FILES = {
    "1860_census_free_blacks": {
        "spreadsheet": "1kJaSr0Aota8Hp59_aLo8ElKiQFSKP20w",
        "pcb": "Interpret-MotherFN-ChildFN-ChildBirthYear",
    },
    "free_blacks_rockbridge_county": {
        "spreadsheet": "1LCrMNdAevfAT8n6YvcX2exVaRV8rsxmiZ-E--BggGi0",
    },
    "freedmens_marriage_records": {
        "spreadsheet": "12Hk_VxV9XR0I3Ccvq1RokF_Nhw2_ilke",
    },
    "us_colored_troops_born_in_rc": {
        "spreadsheet": "1EtGNZgHzr7u8KecPk1vO-ixDS3WQo1NR",
    }
}

for key, info in CSV_FILES.items():
    directory = "content/" + key + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Delete old page files except _index.md
    for f in os.listdir(directory):
        if not f.startswith("_") and f.endswith(".md"):
            os.remove(directory + f)

    i = 0
    with requests.get("https://docs.google.com/spreadsheets/d/" + info["spreadsheet"] + "/export?format=csv", stream=True) as r:
        if r.status_code >= 400:
            print("Error accessing", key, r.raise_for_status())
            continue
        lines = (line.decode('utf-8') for line in r.iter_lines())
        for row in csv.DictReader(lines):
            i = i + 1
            # row["id"] = str(i)
            frontmatter = {
                "title": row.get("First Name", "") + " " + row.get("Surname", ""),
                "kv": row,
            }
            if "pcb" in info:
                tmp = row.pop(info["pcb"], "")
                if tmp != "":
                    frontmatter["pcb"] = [tmp]
            new_page = open(os.path.join(directory, str(i) + ".md"), 'w')
            new_page.write(json.dumps(frontmatter, indent=1)+"\n\n")
            new_page.close()
        print("finished processing", key)
