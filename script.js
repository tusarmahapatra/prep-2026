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
  
  // Update chart legend color when theme changes
  if (window.topicsChart) {
    const legendColor = isDark ? '#ffffff' : '#212121';
    window.topicsChart.options.plugins.legend.labels.color = legendColor;
    window.topicsChart.update();
  }
});

// const DATA_URL =
//   "https://raw.githubusercontent.com/tusarmahapatra/prep-2026/main/data/dashboard.json";

const DATA_URL =
  "https://tusarmahapatra.github.io/prep-2026/data/dashboard.json";




fetch(`${DATA_URL}?t=${Date.now()}`)
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
    const scoreValue = document.getElementById("score-value");
    const scoreDesc = document.getElementById("score-desc");
    const progressCircle = document.getElementById("progress-circle");
    const circumference = 2 * Math.PI * 45; // radius is 45
    
    scoreValue.textContent = data.score;
    progressCircle.style.strokeDashoffset = circumference - (data.score / 100) * circumference;
    
    // Score description based on readiness
    if (data.score >= 80) {
      scoreDesc.textContent = "Excellent progress! Ready for interviews.";
    } else if (data.score >= 60) {
      scoreDesc.textContent = "Good foundation. Keep practicing!";
    } else if (data.score >= 40) {
      scoreDesc.textContent = "Making progress. Stay focused!";
    } else {
      scoreDesc.textContent = "Getting started. Keep going!";
    }

    // ==============================
    // Quick Stats
    // ==============================
    const totalSolved = Object.values(data.topic_counter).reduce((a, b) => a + b, 0);
    const totalTarget = Object.values(data.topics).reduce((a, b) => a + b, 0);
    const topicsCovered = Object.keys(data.topics).length;
    const completionRate = Math.floor((totalSolved / totalTarget) * 100);

    document.getElementById("total-solved").textContent = totalSolved;
    document.getElementById("topics-covered").textContent = topicsCovered;
    document.getElementById("completion-rate").textContent = completionRate + "%";

    // ==============================
    // Topic Progress Accordion
    // ==============================
    const accordion = document.getElementById("topics-accordion");
    accordion.innerHTML = "";
    const sectionToggle = document.querySelector(".section-toggle");
    const sectionContent = document.querySelector(".section-content");

    const topicLabels = [];
    const topicSolved = [];
    const topicColors = [
      "#4caf50", "#42a5f5", "#ff9800", "#f44336", "#9c27b0",
      "#00bcd4", "#e91e63", "#8bc34a", "#ffc107", "#673ab7",
      "#2196f3", "#ff5722", "#3f51b5", "#cddc39", "#00695c"
    ];

    for (const topic in data.topics) {
      const solved = data.topic_counter[topic] || 0;
      const target = data.topics[topic];
      const percent = Math.floor((solved / target) * 100);
      const progressIndicator = getProgressIndicator(percent);

      topicLabels.push(topic);
      topicSolved.push(solved);

      const topicItem = document.createElement("div");
      topicItem.className = "topic-item";
      topicItem.innerHTML = `
        <div class="topic-item-header">
          <div class="topic-item-content">
            <span class="topic-item-name">${topic}</span>
            <div class="topic-item-stats">
              <span class="topic-stat">${solved}/${target}</span>
            </div>
          </div>
          <div class="topic-item-progress">
            <div class="topic-progress-bar">
              <div class="topic-progress-fill" style="width: ${percent}%"></div>
            </div>
            <span class="topic-percentage">${percent}%</span>
          </div>
        </div>
      `;

      topicItem.addEventListener("click", () => {
        window.location.href = `problems.html?topic=${encodeURIComponent(topic)}`;
      });

      accordion.appendChild(topicItem);
    }

    // Create Pie Chart
    const ctx = document.getElementById("topicsChart");
    if (ctx) {
      const chartColors = topicColors.slice(0, topicLabels.length);
      const isDarkTheme = document.body.classList.contains('dark-theme');
      const legendColor = isDarkTheme ? '#ffffff' : '#212121';
      
      window.topicsChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: topicLabels,
          datasets: [
            {
              data: topicSolved,
              backgroundColor: chartColors,
              borderColor: getComputedStyle(document.documentElement).getPropertyValue("--bg-secondary").trim(),
              borderWidth: 2,
              borderRadius: 4,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                color: legendColor,
                font: {
                  family: "'Roboto', sans-serif",
                  size: 12,
                  weight: "500"
                },
                padding: 12,
                usePointStyle: true,
                pointStyle: "circle"
              }
            },
            tooltip: {
              backgroundColor: getComputedStyle(document.documentElement).getPropertyValue("--bg-secondary").trim(),
              titleColor: getComputedStyle(document.documentElement).getPropertyValue("--text-primary").trim(),
              bodyColor: getComputedStyle(document.documentElement).getPropertyValue("--text-secondary").trim(),
              borderColor: getComputedStyle(document.documentElement).getPropertyValue("--border-color").trim(),
              borderWidth: 1,
              padding: 12,
              titleFont: {
                size: 13,
                weight: "600"
              },
              bodyFont: {
                size: 12
              },
              callbacks: {
                label: function(context) {
                  return context.label + ": " + context.parsed + " problems";
                }
              }
            }
          }
        }
      });
    }

    // Section toggle functionality
    sectionToggle.addEventListener("click", () => {
      sectionToggle.classList.toggle("active");
      sectionContent.classList.toggle("active");
    });
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


// Auto-refresh dashboard every 5 minutes
setInterval(() => {
  location.reload();
}, 5 * 60 * 1000);
