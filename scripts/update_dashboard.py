import os
import re
from collections import defaultdict
from datetime import datetime, timedelta

# ---------------- CONFIG ---------------- #

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
    "difficulty": re.compile(r"# Difficulty:\s*(.*)"),
    "time": re.compile(r"# Time complexity:\s*(.*)"),
    "space": re.compile(r"# Space complexity:\s*(.*)"),
    "date": re.compile(r"# Solved on:\s*(.*)")
}

# ---------------- PARSING ---------------- #

def parse_metadata(filepath):
    meta = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f.readlines()[:15]:
            for key, regex in META_REGEX.items():
                match = regex.match(line.strip())
                if match:
                    meta[key] = match.group(1)

    if "date" not in meta:
        meta["date"] = datetime.fromtimestamp(
            os.path.getmtime(filepath)
        ).date().isoformat()

    return meta if {"problem", "pattern", "time", "space"} <= meta.keys() else None


def collect_data():
    solved = []
    topic_counter = defaultdict(int)
    pattern_counter = defaultdict(int)

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


# ---------------- DASHBOARD ---------------- #

def progress_color(percent):
    if percent >= 70:
        return "🟩"
    elif percent >= 30:
        return "🟨"
    return "🟥"


def generate_dashboard(topic_counter):
    rows = []
    for _, (name, target) in TOPICS.items():
        solved = topic_counter.get(name, 0)
        percent = int((solved / target) * 100)
        rows.append(
            f"| {name} | {solved} | {target} | {progress_color(percent)} {percent}% |"
        )

    return (
        "| Topic | Solved | Target | Progress |\n"
        "|------|-------|--------|----------|\n"
        + "\n".join(rows)
    )


# ---------------- SOLVED LOG ---------------- #

def generate_solved_log(solved):
    rows = []
    for i, s in enumerate(sorted(solved, key=lambda x: x["date"]), 1):
        rows.append(
            f"| {i} | {s['problem']} | {s.get('topic','—')} | "
            f"{s['pattern']} | {s['time']} | {s['space']} |"
        )

    return (
        "| # | Problem | Topic | Pattern | Time | Space |\n"
        "|--|--------|------|--------|------|-------|\n"
        + "\n".join(rows)
    )


# ---------------- PATTERN TRACKER ---------------- #

def generate_pattern_tracker(counter):
    rows = []
    for pattern, count in sorted(counter.items(), key=lambda x: -x[1]):
        rows.append(f"| {pattern} | {count} |")

    return (
        "| Pattern | Count |\n"
        "|--------|-------|\n"
        + "\n".join(rows)
    )


# ---------------- VELOCITY ---------------- #

def compute_velocity(solved):
    now = datetime.now()
    last_7 = last_30 = 0
    active_days = set()

    for s in solved:
        d = datetime.fromisoformat(s["date"])
        active_days.add(d.date())

        if (now - d).days <= 7:
            last_7 += 1
        if (now - d).days <= 30:
            last_30 += 1

    avg_per_day = round(last_30 / 30, 2)
    return last_7, last_30, avg_per_day, len(active_days)


def generate_velocity_block(v):
    w7, w30, avg, days = v
    return (
        "| Metric | Value |\n"
        "|------|------|\n"
        f"| Problems (7 days) | {w7} |\n"
        f"| Problems (30 days) | {w30} |\n"
        f"| Avg / Day | {avg} |\n"
        f"| Active Days | {days} |"
    )


# ---------------- DIFFICULTY ---------------- #

def generate_difficulty(solved):
    counter = defaultdict(int)
    for s in solved:
        if "difficulty" in s:
            counter[s["difficulty"]] += 1

    if not counter:
        return "_No difficulty metadata yet_"

    total = sum(counter.values())
    rows = []
    for k, v in counter.items():
        pct = round((v / total) * 100, 1)
        rows.append(f"| {k} | {v} | {pct}% |")

    return (
        "| Difficulty | Count | % |\n"
        "|-----------|-------|---|\n"
        + "\n".join(rows)
    )


# ---------------- SCORE ---------------- #

def compute_score(solved, pattern_counter):
    solved_count = len(solved)
    target = sum(t[1] for t in TOPICS.values())

    volume = (solved_count / target) * 40
    velocity = min(solved_count / 30, 1) * 20
    pattern_score = min(len(pattern_counter), 10)

    return int(volume + velocity + pattern_score)


# ---------------- UTIL ---------------- #

def replace_block(content, start, end, new):
    return re.sub(
        f"{start}[\\s\\S]*?{end}",
        f"{start}\n{new}\n{end}",
        content
    )


# ---------------- MAIN ---------------- #

def main():
    solved, topic_counter, pattern_counter = collect_data()

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_block(
        content, "<!-- DASHBOARD_START -->", "<!-- DASHBOARD_END -->",
        generate_dashboard(topic_counter)
    )

    content = replace_block(
        content, "<!-- SOLVED_LOG_START -->", "<!-- SOLVED_LOG_END -->",
        generate_solved_log(solved)
    )

    content = replace_block(
        content, "<!-- PATTERN_TRACKER_START -->", "<!-- PATTERN_TRACKER_END -->",
        generate_pattern_tracker(pattern_counter)
    )

    velocity = compute_velocity(solved)
    content = replace_block(
        content, "<!-- VELOCITY_START -->", "<!-- VELOCITY_END -->",
        generate_velocity_block(velocity)
    )

    content = replace_block(
        content, "<!-- DIFFICULTY_START -->", "<!-- DIFFICULTY_END -->",
        generate_difficulty(solved)
    )

    score = compute_score(solved, pattern_counter)
    content = replace_block(
        content, "<!-- SCORE_START -->", "<!-- SCORE_END -->",
        f"📈 **Google SDE Readiness Score:** `{score} / 100`"
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
