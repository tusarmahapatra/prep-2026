const DATA_URL =
  "https://raw.githubusercontent.com/tusar.mahapatra/prep-2026/main/data/dashboard.json";

fetch(DATA_URL)
  .then(res => {
    if (!res.ok) throw new Error("Failed to fetch dashboard data");
    return res.json();
  })
  .then(data => renderDashboard(data))
  .catch(err => {
    document.body.innerHTML += `<p style="color:red">${err.message}</p>`;
  });

function renderDashboard(data) {
  // Score
  document.getElementById("score").innerHTML =
    `<h2>📈 Readiness Score: ${data.score} / 100</h2>`;

  // Updated time
  document.getElementById("updated").textContent =
    `Last updated: ${new Date(data.updated_at).toLocaleString()}`;

  // Topics table
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
}

function progressEmoji(p) {
  if (p >= 70) return "🟩";
  if (p >= 30) return "🟨";
  return "🟥";
}
