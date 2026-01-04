import os
import re

TOPICS = {
    "arrays_strings": ("Arrays & Strings", 50),
    "hashmaps": ("Hashmaps", 25),
    "two_pointers": ("Two Pointers", 20),
    "linked_list": ("Linked Lists", 20),
    "stacks_queues": ("Stacks & Queues", 20),
    "trees": ("Trees", 30),
}

def count_problems(folder):
    if not os.path.exists(folder):
        return 0
    return len([
        f for f in os.listdir(folder)
        if f.endswith(".py")
    ])

def progress_bar(done, total):
    blocks = 10
    filled = int((done / total) * blocks) if total else 0
    return "🟩" * filled + "⬜" * (blocks - filled)

def main():
    total_done = 0
    total_target = 0
    rows = []

    for folder, (name, target) in TOPICS.items():
        done = count_problems(folder)
        total_done += done
        total_target += target
        rows.append(f"| {name} | {done} | {target} | {progress_bar(done, target)} |")

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_table = (
        "| Topic | Solved | Target | Progress |\n"
        "|------|-------|--------|---------|\n"
        + "\n".join(rows)
        + f"\n| **Total** | **{total_done}** | **{total_target}** | 🚧 In Progress |"
    )

    content = re.sub(
        r"\| Topic \| Solved \| Target \| Progress \|[\s\S]*?\| \*\*Total\*\*.*?\|",
        new_table,
        content,
        flags=re.MULTILINE
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
