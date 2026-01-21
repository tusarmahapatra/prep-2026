// ========== THEME TOGGLE ==========
const themeBtn = document.getElementById('theme-btn');
const htmlElement = document.documentElement;

// Initialize theme from localStorage
const savedTheme = localStorage.getItem('theme') || 'light';
if (savedTheme === 'dark') {
  document.body.classList.add('dark-theme');
  themeBtn.innerHTML = '<span class="material-icons">dark_mode</span>';
}

themeBtn.addEventListener('click', () => {
  document.body.classList.toggle('dark-theme');
  const isDark = document.body.classList.contains('dark-theme');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  themeBtn.innerHTML = isDark 
    ? '<span class="material-icons">dark_mode</span>' 
    : '<span class="material-icons">light_mode</span>';
});

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
    const lastUpdated = new Date(data.updated_at).toLocaleString();
    document.getElementById("updated").textContent = lastUpdated;
    document.getElementById("footer-updated").textContent = lastUpdated;

    // ==============================
    // Readiness Score
    // ==============================
    const scoreSection = document.getElementById("score");
    scoreSection.innerHTML = `
      <h2>Readiness Score</h2>
      <span class="score-value">${data.score}</span>
      <p class="score-label">out of 100</p>
    `;

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
      const progressIndicator = getProgressIndicator(percent);

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${topic}</td>
        <td>${solved}</td>
        <td>${target}</td>
        <td>
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${percent}%"></div>
          </div>
          <span class="progress-text">${progressIndicator} ${percent}%</span>
        </td>
      `;
      
      row.addEventListener("click", () => {
        window.location.href = `problems.html?topic=${encodeURIComponent(topic)}`;
      });
      
      table.appendChild(row);
    }
  })
  .catch(err => {
    console.error(err);
    document.getElementById("error").textContent =
      "Failed to load dashboard data: " + err.message;
  });

function getProgressIndicator(percent) {
  if (percent >= 70) return "✓";
  if (percent >= 40) return "◐";
  return "○";
}

function getDifficultyBadge(difficulty) {
  const badges = {
    'easy': '🟢',
    'medium': '🟡',
    'hard': '🔴'
  };
  return badges[difficulty.toLowerCase()] || difficulty;
}
