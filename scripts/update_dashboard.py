import os
import re
from collections import defaultdict

README = "README.md"

TARGETS = {
    "arrays_strings": 50,
    "hashmaps": 40,
    "two_pointers": 30,
    "stacks_queues": 30,
    "linked_list": 25,
    "trees": 50,
}

DISPLAY = {
    "arrays_strings": "Arrays & Strings",
    "hashmaps": "Hashmaps",
    "two_pointers": "Two Pointers",
    "stacks_queues": "Stacks & Queues",
    "linked_list": "Linked Lists",
    "trees": "Trees",
}

def progress_bar(p):
    if p < 30: return f"🟥 {p}%"
    if p < 70: return f"🟨 {p}%"
    return f"🟩 {p}%"

# ------------------ PARSE PROBLEMS ------------------

problems = []
pattern_count = defaultdict(int)
topic_count = defaultdict(int)

for folder in TARGETS:
    if not os.path.isdir(folder):
        continue

    for file in os.listdir(folder):
        if not file.endswith(".py"):
            continue

        path = os.path.join(folder, file)
        with open(path, encoding="utf-8") as f:
            content = f.read()

        def extract(key):
            match = re.search(rf"#\s*{key}:\s*(.+)", content, re.I)
            return match.group(1).strip() if match else "—"

        problem = {
            "problem": extract("Problem"),
            "topic": extract("Topic"),
            "pattern": extract("Pattern"),
            "time": extract("Time complexity"),
            "space": extract("Space complexity"),
        }

        problems.append(problem)
        topic_count[folder] += 1

        for p in problem["pattern"].split(","):
            if p.strip() != "—":
                pattern_count[p.strip()] += 1

# ------------------ DASHBOARD TABLE ------------------

rows = []
for folder, target in TARGETS.items():
    solved = topic_count.get(folder, 0)
    percent = int((solved / target) * 100)
    rows.append(
        f"| {DISPLAY[folder]} | {solved} | {target} | {progress_bar(percent)} |"
    )

dashboard = (
    "| Topic | Solved | Target | Progress |\n"
    "|------|-------|--------|----------|\n"
    + "\n".join(rows)
)

# ------------------ SOLVED LOG ------------------

solved_rows = [
    "| # | Problem | Topic | Pattern | Time | Space |",
    "|--|--------|------|--------|------|-------|",
]

for i, p in enumerate(problems, 1):
    solved_rows.append(
        f"| {i} | {p['problem']} | {p['topic']} | "
        f"{p['pattern']} | {p['time']} | {p['space']} |"
    )

solved_table = "\n".join(solved_rows)

# ------------------ PATTERN TRACKER ------------------

pattern_rows = ["| Pattern | Count |", "|-------|------|"]
for k, v in sorted(pattern_count.items()):
    pattern_rows.append(f"| {k} | {v} |")

pattern_table = "\n".join(pattern_rows)

# ------------------ UPDATE README ------------------

with open(README, "r", encoding="utf-8") as f:
    readme = f.read()

readme = re.sub(
    r"<!-- DASHBOARD_START -->.*?<!-- DASHBOARD_END -->",
    f"<!-- DASHBOARD_START -->\n\n{dashboard}\n\n<!-- DASHBOARD_END -->",
    readme,
    flags=re.S,
)

readme = re.sub(
    r"<!-- SOLVED_LOG_START -->.*?<!-- SOLVED_LOG_END -->",
    f"<!-- SOLVED_LOG_START -->\n\n{solved_table}\n\n<!-- SOLVED_LOG_END -->",
    readme,
    flags=re.S,
)

readme = re.sub(
    r"<!-- PATTERN_TRACKER_START -->.*?<!-- PATTERN_TRACKER_END -->",
    f"<!-- PATTERN_TRACKER_START -->\n\n{pattern_table}\n\n<!-- PATTERN_TRACKER_END -->",
    readme,
    flags=re.S,
)

with open(README, "w", encoding="utf-8") as f:
    f.write(readme)

print("Full dashboard updated.")
