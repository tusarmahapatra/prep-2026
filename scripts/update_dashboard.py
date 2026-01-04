import os
import re
from collections import defaultdict
from datetime import datetime

# ---------------- CONFIG ---------------- #

TOPICS = {
    "arrays_strings": ("Arrays & Strings", 50),
    "hashmaps": ("Hashmaps", 40),
    "two_pointers": ("Two Pointers", 30),
    "stacks_queues": ("Stacks & Queues", 30),
    "linked_list": ("Linked Lists", 25),
    "trees": ("Trees", 50),
}

PROBLEM_RE = re.compile(r"#\s*Problem:\s*(.*)", re.IGNORECASE)
TIME_RE = re.compile(r"#\s*Time complexity:\s*(.*)", re.IGNORECASE)
SPACE_RE = re.compile(r"#\s*Space complexity:\s*(.*)", re.IGNORECASE)
PATTERN_RE = re.compile(r"#.*Pattern:\s*(.*)", re.IGNORECASE)
DIFFICULTY_RE = re.compile(r"#\s*Difficulty:\s*(.*)", re.IGNORECASE)

# ---------------- PARSER ---------------- #

def parse_metadata(filepath, topic_name):
    meta = {
        "topic": topic_name,
        "pattern": "—",
        "difficulty": "—"
    }

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if "problem" not in meta:
            m = PROBLEM_RE.match(line)
            if m:
                meta["problem"] = m.group(1)

        if "time" not in meta:
            m = TIME_RE.match(line)
            if m:
                meta["time"] = m.group(1)

        if "space" not in meta:
            m = SPACE_RE.match(line)
            if m:
                meta["space"] = m.group(1)

        m = PATTERN_RE.match(line)
        if m:
            meta["pattern"] = m.group(1)

        m = DIFFICULTY_RE.match(line)
        if m:
            meta["difficulty"] = m.group(1)

    if not all(k in meta for k in ("problem", "time", "space")):
        return None

    meta["date"] = datetime.fromtimestamp(
        os.path.getmtime(filepath)
    ).date().isoformat()

    return meta


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

            path = os.path.join(folder, file)
            meta = parse_metadata(path, topic_name)

            if not meta:
                continue

            solved.append(meta)
            topic_counter[topic_name] += 1
            pattern_counter[meta["pattern"]] += 1

    return solved, topic_counter, pattern_counter

# ---------------- DASHBOARD ---------------- #

def progress_color(p):
    if p >= 70:
        return "🟩"
    elif p >= 30:
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
    solved = sorted(solved, key=lambda x: x["date"])

    for i, s in enumerate(solved, 1):
        rows.append(
            f"| {i} | {s['problem']} | {s['topic']} | "
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

    avg = round(last_30 / 30, 2)
    return last_7, last_30, avg, len(active_days)


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
        if s["difficulty"] != "—":
            counter[s["difficulty"]] += 1

    if not counter:
        return "_Difficulty not tagged yet_"

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

def compute_score(solved, patterns):
    solved_count = len(solved)
    target = sum(t[1] for t in TOPICS.values())

    volume = (solved_count / target) * 40
    velocity = min(solved_count / 30, 1) * 20
    pattern_score = min(len(patterns), 10)

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
