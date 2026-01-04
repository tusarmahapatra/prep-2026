import os
import re
from collections import defaultdict

TOPICS = {
    "arrays_strings": ("Arrays & Strings", 50),
    "hashmaps": ("Hashmaps", 40),
    "two_pointers": ("Two Pointers", 30),
    "stacks_queues": ("Stacks & Queues", 30),
    "linked_list": ("Linked Lists", 25),
    "trees": ("Trees", 50),
}

META_REGEX = {
    "problem": re.compile(r"# Problem:\s*(.*)"),
    "topic": re.compile(r"# Topic:\s*(.*)"),
    "pattern": re.compile(r"# Pattern:\s*(.*)"),
    "time": re.compile(r"# Time complexity:\s*(.*)"),
    "space": re.compile(r"# Space complexity:\s*(.*)")
}

def parse_metadata(filepath):
    meta = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f.readlines()[:10]:
            for key, regex in META_REGEX.items():
                match = regex.match(line.strip())
                if match:
                    meta[key] = match.group(1)
    return meta if len(meta) == 5 else None

def collect_data():
    solved = []
    pattern_counter = defaultdict(int)
    topic_counter = defaultdict(int)

    for folder, (topic_name, _) in TOPICS.items():
        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):
            if not file.endswith(".py"):
                continue

            meta = parse_metadata(os.path.join(folder, file))
            if not meta:
                continue

            solved.append(meta)
            topic_counter[topic_name] += 1
            pattern_counter[meta["pattern"]] += 1

    return solved, topic_counter, pattern_counter

def progress_color(percent):
    if percent >= 70:
        return "🟩"
    elif percent >= 30:
        return "🟨"
    return "🟥"

def generate_dashboard(topic_counter):
    rows = []
    for folder, (name, target) in TOPICS.items():
        solved = topic_counter.get(name, 0)
        percent = int((solved / target) * 100)
        rows.append(
            f"| {name} | {solved} | {target} | {progress_color(percent)} {percent}% |"
        )
    return "\n".join(rows)

def generate_solved_log(solved):
    rows = []
    for i, s in enumerate(solved, 1):
        rows.append(
            f"| {i} | {s['problem']} | {s['topic']} | {s['pattern']} | {s['time']} | {s['space']} |"
        )
    return "\n".join(rows)

def generate_pattern_tracker(counter):
    rows = []
    for pattern, count in sorted(counter.items(), key=lambda x: -x[1]):
        rows.append(f"| {pattern} | {count} |")
    return "\n".join(rows)

def replace_block(content, start, end, new):
    return re.sub(
        f"{start}[\\s\\S]*?{end}",
        f"{start}\n\n{new}\n\n{end}",
        content
    )

def main():
    solved, topic_counter, pattern_counter = collect_data()

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_block(
        content,
        "<!-- DASHBOARD_START -->",
        "<!-- DASHBOARD_END -->",
        generate_dashboard(topic_counter)
    )

    content = replace_block(
        content,
        "<!-- SOLVED_LOG_START -->",
        "<!-- SOLVED_LOG_END -->",
        generate_solved_log(solved)
    )

    content = replace_block(
        content,
        "<!-- PATTERN_TRACKER_START -->",
        "<!-- PATTERN_TRACKER_END -->",
        generate_pattern_tracker(pattern_counter)
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
