import os
import re

TARGETS = {
    "arrays_strings": 50,
    "hashmaps": 40,
    "two_pointers": 30,
    "stacks_queues": 30,
    "linked_list": 25,
    "trees": 50,
}

DISPLAY_NAMES = {
    "arrays_strings": "Arrays & Strings",
    "hashmaps": "Hashmaps",
    "two_pointers": "Two Pointers",
    "stacks_queues": "Stacks & Queues",
    "linked_list": "Linked Lists",
    "trees": "Trees",
}

def progress_bar(percent):
    if percent < 30:
        return f"🟥 {percent}%"
    elif percent < 70:
        return f"🟨 {percent}%"
    else:
        return f"🟩 {percent}%"

rows = []

for folder, target in TARGETS.items():
    if not os.path.exists(folder):
        solved = 0
    else:
        solved = len([
            f for f in os.listdir(folder)
            if f.endswith(".py")
        ])


    percent = int((solved / target) * 100) if target else 0
    rows.append(
        f"| {DISPLAY_NAMES[folder]} | {solved} | {target} | {progress_bar(percent)} |"
    )

table = (
    "| Topic | Solved | Target | Progress |\n"
    "|------|-------|--------|----------|\n"
    + "\n".join(rows)
)

with open("README.md", "r") as f:
    content = f.read()

new_content = re.sub(
    r"<!-- DASHBOARD_START -->.*?<!-- DASHBOARD_END -->",
    f"<!-- DASHBOARD_START -->\n\n{table}\n\n<!-- DASHBOARD_END -->",
    content,
    flags=re.S,
)

with open("README.md", "w") as f:
    f.write(new_content)

print("Dashboard updated.")
