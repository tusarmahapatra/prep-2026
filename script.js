// Make sure this URL matches your public repo
const DATA_URL =
  "https://raw.githubusercontent.com/tusarmahapatra/prep-2026/main/data/dashboard.json";

fetch(DATA_URL)
  .then(res => {
    if (!res.ok) {
      throw new Error(`HTTP status ${res.status}`);
    }
    return res.json();
  })
  .then(data => {
    document.getElementById("updated").textContent =
      "Last updated: " + new Date(data.updated_at).toLocaleString();

    document.getElementById("score").innerHTML =
      `<h2>📈 Readiness Score: ${data.score} / 100</h2>`;

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
  })
  .catch(err => {
    console.error("Failed to fetch data:", err);
    document.getElementById("error").textContent =
      "⚠️ Could not load dashboard data: " + err.message;
  });

function progressEmoji(p) {
  if (p >= 70) return "🟩";
  if (p >= 30) return "🟨";
  return "🟥";
}
