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
    // 🧠 Solved Problems Section
    // ==============================
    const solvedSection = document.createElement("section");
    solvedSection.innerHTML = "<h2>🧠 Solved Problems</h2>";

    const solvedTable = document.createElement("table");
    solvedTable.innerHTML = `
      <tr>
        <th>#</th>
        <th>Problem</th>
        <th>Topic</th>
        <th>Pattern</th>
        <th>Solution</th>
      </tr>
    `;

    data.solved.forEach((p, i) => {
      const githubUrl =
        `https://github.com/tusarmahapatra/prep-2026/blob/main/${p.solution_path}`;

      solvedTable.innerHTML += `
        <tr>
          <td>${i + 1}</td>
          <td>${p.problem}</td>
          <td>${p.topic}</td>
          <td>${p.pattern}</td>
          <td>
            <a href="${githubUrl}" target="_blank">View Code</a>
          </td>
        </tr>
      `;
    });

    solvedSection.appendChild(solvedTable);
    document.body.appendChild(solvedSection);
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
