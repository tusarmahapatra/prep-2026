import os
import re
from collections import defaultdict
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

TOPIC_TARGETS = {
    "Arrays & Strings": 50,
    "Hashmaps": 40,
    "Two Pointers": 30,
    "Stacks & Queues": 30,
    "Linked Lists": 25,
    "Trees": 50,
}

PROBLEM_RE = re.compile(r"#\s*Problem:\s*(.*)", re.IGNORECASE)
TIME_RE = re.compile(r"#\s*Time complexity:\s*(.*)", re.IGNORECASE)
SPACE_RE = re.compile(r"#\s*Space complexity:\s*(.*)", re.IGNORECASE)
PATTERN_RE = re.compile(r"#\s*Pattern:\s*(.*)", re.IGNORECASE)
DIFFICULTY_RE = re.compile(r"#\s*Difficulty:\s*(.*)", re.IGNORECASE)

# =========================================================
# METADATA PARSER
# =========================================================

def parse_metadata(filepath: str, topic: str):
    meta = {
        "topic": topic,
        "pattern": "—",
        "difficulty": "—",
        "problem": None,
        "time": None,
        "space": None,
    }

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not meta["problem"]:
                m = PROBLEM_RE.match(line)
                if m:
                    meta["problem"] = m.group(1)

            if not meta["time"]:
                m = TIME_RE.match(line)
                if m:
                    meta["time"] = m.group(1)

            if not meta["space"]:
                m = SPACE_RE.match(line)
                if m:
                    meta["space"] = m.group(1)

            m = PATTERN_RE.match(line)
            if m:
                meta["pattern"] = m.group(1)

            m = DIFFICULTY_RE.match(line)
            if m:
                meta["difficulty"] = m.group(1)

    if not all([meta["problem"], meta["time"], meta["space"]]):
        return None

    meta["date"] = datetime.fromtimestamp(
        os.path.getmtime(filepath)
    ).date().isoformat()

    return meta

# =========================================================
# DATA COLLECTION
# =========================================================

def collect_data():
    solved = []
    topic_counter = defaultdict(int)
    pattern_counter = defaultdict(int)

    for topic in TOPIC_TARGETS:
        if not os.path.isdir(topic):
            continue

        for file in os.listdir(topic):
            if not file.endswith(".py"):
                continue

            path = os.path.join(topic, file)
            meta = parse_metadata(path, topic)

            if not meta:
                continue

            solved.append(meta)
            topic_counter[topic] += 1
            pattern_counter[meta["pattern"]] += 1

    return solved, topic_counter, pattern_counter

# =========================================================
# DASHBOARD
# =========================================================

def progress_color(percent):
    if percent >= 70:
        return "🟩"
    elif percent >= 30:
        return "🟨"
    return "🟥"


def generate_dashboard(topic_counter):
    rows = []
    for topic, target in TOPIC_TARGETS.items():
        solved = topic_counter.get(topic, 0)
        percent = int((solved / target) * 100)
        rows.append(
            f"| {topic} | {solved} | {target} | {progress_color(percent)} {percent}% |"
        )

    return (
        "| Topic | Solved | Target | Progress |\n"
        "|------|-------|--------|----------|\n"
        + "\n".join(rows)
    )

# =========================================================
# SOLVED LOG
# =========================================================

def generate_solved_log(solved):
    solved = sorted(solved, key=lambda x: x["date"])
    rows = []

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

# =========================================================
# PATTERN TRACKER
# =========================================================

def generate_pattern_tracker(counter):
    if not counter:
        return "| Pattern | Count |\n|--------|-------|"

    rows = [f"| {k} | {v} |" for k, v in sorted(counter.items(), key=lambda x: -x[1])]
    return "| Pattern | Count |\n|--------|-------|\n" + "\n".join(rows)

# =========================================================
# VELOCITY
# =========================================================

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

# =========================================================
# DIFFICULTY
# =========================================================

def generate_difficulty(solved):
    counter = defaultdict(int)

    for s in solved:
        if s["difficulty"] != "—":
            counter[s["difficulty"]] += 1

    if not counter:
        return "_Difficulty not tagged yet_"

    total = sum(counter.values())
    rows = [
        f"| {k} | {v} | {round((v / total) * 100, 1)}% |"
        for k, v in counter.items()
    ]

    return "| Difficulty | Count | % |\n|-----------|-------|---|\n" + "\n".join(rows)

# =========================================================
# SCORE
# =========================================================

def compute_score(solved, pattern_counter):
    solved_count = len(solved)
    target = sum(TOPIC_TARGETS.values())

    volume = (solved_count / target) * 40
    velocity = min(solved_count / 30, 1) * 20
    pattern_score = min(len(pattern_counter), 10)

    return int(volume + velocity + pattern_score)

# =========================================================
# UTIL
# =========================================================

def replace_block(content, start, end, new):
    return re.sub(
        rf"{start}[\s\S]*?{end}",
        f"{start}\n{new}\n{end}",
        content
    )

# =========================================================
# MAIN
# =========================================================

def main():
    solved, topic_counter, pattern_counter = collect_data()

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_block(content, "<!-- DASHBOARD_START -->", "<!-- DASHBOARD_END -->",
                            generate_dashboard(topic_counter))

    content = replace_block(content, "<!-- VELOCITY_START -->", "<!-- VELOCITY_END -->",
                            generate_velocity_block(compute_velocity(solved)))

    content = replace_block(content, "<!-- SOLVED_LOG_START -->", "<!-- SOLVED_LOG_END -->",
                            generate_solved_log(solved))

    content = replace_block(content, "<!-- PATTERN_TRACKER_START -->", "<!-- PATTERN_TRACKER_END -->",
                            generate_pattern_tracker(pattern_counter))

    content = replace_block(content, "<!-- DIFFICULTY_START -->", "<!-- DIFFICULTY_END -->",
                            generate_difficulty(solved))

    score = compute_score(solved, pattern_counter)
    content = replace_block(content, "<!-- SCORE_START -->", "<!-- SCORE_END -->",
                            f"📈 **Google SDE Readiness Score:** `{score} / 100`")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
