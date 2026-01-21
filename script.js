const DATA_URL =
  "https://raw.githubusercontent.com/tusarmahapatra/prep-2026/main/data/dashboard.json";

fetch(DATA_URL)
  .then(res => {
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    return res.json();
  })
  .then(data => {
    // ==============================
    // Last updated time
    // ==============================
    document.getElementById("updated").textContent =
      "Last updated: " + new Date(data.updated_at).toLocaleString();

    // ==============================
    // Readiness Score
    // ==============================
    document.getElementById("score").innerHTML =
      `<h2>📈 Readiness Score: ${data.score} / 100</h2>`;

    // ==============================
    // Topic Progress Table
    // ==============================
    const table = document.getElementById("topics");
    table.innerHTML = `
      <tr>
        <th>Topic</th>
        <th>Solved</th>
        <th>Target</th>
        <th>Progress</th>
      </tr>
    `;

    for (const topic in data.topics) {
      const solved = data.topic_counter[topic] || 0;
      const target = data.topics[topic];
      const percent = Math.floor((solved / target) * 100);

      table.innerHTML += `
        <tr>
          <td>${topic}</td>
          <td>${solved}</td>
          <td>${target}</td>
          <td>${progressEmoji(percent)} ${percent}%</td>
        </tr>
      `;
    }

    // ==============================
    // 🧠 Solved Problems + Filters
    // ==============================

    const solvedSection = document.createElement("section");
    solvedSection.innerHTML = "<h2>🧠 Solved Problems</h2>";

    const solvedTable = document.createElement("table");
    solvedSection.appendChild(solvedTable);
    document.body.appendChild(solvedSection);

    const topicFilter = document.getElementById("filter-topic");
    const difficultyFilter = document.getElementById("filter-difficulty");

    // Populate filter dropdowns
    const topicsSet = new Set();
    const difficultySet = new Set();

    data.solved.forEach(p => {
      topicsSet.add(p.topic);
      difficultySet.add(p.difficulty);
    });

    [...topicsSet].sort().forEach(t => {
      topicFilter.innerHTML += `<option value="${t}">${t}</option>`;
    });

    [...difficultySet].sort().forEach(d => {
      difficultyFilter.innerHTML += `<option value="${d}">${d}</option>`;
    });

    function renderSolvedTable() {
      const topicValue = topicFilter.value;
      const difficultyValue = difficultyFilter.value;

      solvedTable.innerHTML = `
        <tr>
          <th>#</th>
          <th>Problem</th>
          <th>Topic</th>
          <th>Pattern</th>
          <th>Difficulty</th>
          <th>Solution</th>
        </tr>
      `;

      let count = 0;

      data.solved.forEach(p => {
        if (topicValue && p.topic !== topicValue) return;
        if (difficultyValue && p.difficulty !== difficultyValue) return;

        count++;
        const githubUrl =
          `https://github.com/tusarmahapatra/prep-2026/blob/main/${p.solution_path}`;

        solvedTable.innerHTML += `
          <tr>
            <td>${count}</td>
            <td>${p.problem}</td>
            <td>${p.topic}</td>
            <td>${p.pattern}</td>
            <td>${p.difficulty}</td>
            <td>
              <a href="${githubUrl}" target="_blank">View Code</a>
            </td>
          </tr>
        `;
      });
    }

    // Initial render
    renderSolvedTable();

    // Re-render on filter change
    topicFilter.addEventListener("change", renderSolvedTable);
    difficultyFilter.addEventListener("change", renderSolvedTable);
  })
  .catch(err => {
    console.error(err);
    document.getElementById("error").textContent =
      "Failed to load dashboard data: " + err.message;
  });

function progressEmoji(p) {
  if (p >= 70) return "🟩";
  if (p >= 30) return "🟨";
  return "🟥";
}
