// ========== THEME TOGGLE ==========
const themeBtn = document.getElementById('theme-btn');
const backBtn = document.getElementById('back-btn');

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

// ========== BACK BUTTON ==========
backBtn.addEventListener('click', () => {
  window.history.back();
});

// ========== GET URL PARAMETERS ==========
const urlParams = new URLSearchParams(window.location.search);
const selectedTopic = urlParams.get('topic');

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
    // Page Title
    // ==============================
    const pageTitle = document.getElementById("page-title");
    const problemsHeader = document.getElementById("problems-header");
    
    if (selectedTopic) {
      pageTitle.textContent = selectedTopic + " - Solved Problems";
      problemsHeader.textContent = selectedTopic;
    } else {
      pageTitle.textContent = "All Solved Problems";
      problemsHeader.textContent = "All Problems";
    }

    // ==============================
    // Problems Table
    // ==============================
    const problemsTable = document.getElementById("problems-table");
    problemsTable.innerHTML = `
      <tr>
        <th>#</th>
        <th>Problem</th>
        <th>Topic</th>
        <th>Pattern</th>
        <th>Difficulty</th>
        <th>Solution</th>
      </tr>
    `;

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

    // If a topic was selected, set it in the filter
    if (selectedTopic) {
      topicFilter.value = selectedTopic;
    }

    function renderProblemsTable() {
      const topicValue = topicFilter.value;
      const difficultyValue = difficultyFilter.value;

      problemsTable.innerHTML = `
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
        const rawGithubUrl =
          `https://raw.githubusercontent.com/tusarmahapatra/prep-2026/main/${p.solution_path}`;

        problemsTable.innerHTML += `
          <tr>
            <td>${count}</td>
            <td>${p.problem}</td>
            <td>${p.topic}</td>
            <td>${p.pattern}</td>
            <td><span class="badge badge-${p.difficulty.toLowerCase()}">${p.difficulty}</span></td>
            <td><button class="button code-btn" data-url="${rawGithubUrl}" data-name="${p.problem}"><span class="material-icons">code</span>View Code</button></td>
          </tr>
        `;
      });

      if (count === 0) {
        problemsTable.innerHTML += `
          <tr>
            <td colspan="6" style="text-align: center; padding: 32px; color: var(--text-tertiary);">
              <span class="material-icons" style="font-size: 48px; display: block; margin-bottom: 16px; opacity: 0.5;">search_off</span>
              No problems found for the selected filters.
            </td>
          </tr>
        `;
      }
    }

    // Initial render
    renderProblemsTable();

    // Re-render on filter change
    topicFilter.addEventListener("change", renderProblemsTable);
    difficultyFilter.addEventListener("change", renderProblemsTable);

    // ========== CODE MODAL FUNCTIONALITY ==========
    const modal = document.getElementById("code-modal");
    const modalClose = document.getElementById("modal-close");
    const codeContent = document.getElementById("code-content");
    const modalTitle = document.getElementById("modal-title");

    // Close modal on close button click
    modalClose.addEventListener("click", () => {
      modal.classList.remove("active");
    });

    // Close modal on outside click
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("active");
      }
    });

    // Close modal on Escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        modal.classList.remove("active");
      }
    });

    // Handle code button clicks (delegated event)
    problemsTable.addEventListener("click", async (e) => {
      const btn = e.target.closest(".code-btn");
      if (!btn) return;

      const codeUrl = btn.getAttribute("data-url");
      const problemName = btn.getAttribute("data-name");

      try {
        const response = await fetch(codeUrl);
        const code = await response.text();
        
        codeContent.textContent = code;
        modalTitle.textContent = problemName;
        
        // Re-highlight the code
        hljs.highlightElement(codeContent);
        
        modal.classList.add("active");
      } catch (err) {
        console.error("Error fetching code:", err);
        codeContent.textContent = "Error loading code. Please try again.";
        modal.classList.add("active");
      }
    });
  })
  .catch(err => {
    console.error(err);
    document.getElementById("error").textContent =
      "Failed to load problems data: " + err.message;
  });
