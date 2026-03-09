let selectedFiles = [];
let latestResults = null;

const dropArea = document.getElementById("dropArea");
const fileInput = document.getElementById("resume");
const browseBtn = document.getElementById("browseBtn");
const fileList = document.getElementById("fileList");
const resultsDiv = document.getElementById("results");
const downloadBtn = document.getElementById("downloadBtn");

if (browseBtn) {
  browseBtn.addEventListener("click", () => fileInput.click());
}

if (fileInput) {
  fileInput.addEventListener("change", (e) => {
    selectedFiles = Array.from(e.target.files);
    renderFileList();
  });
}

if (dropArea) {
  ["dragenter", "dragover"].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropArea.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropArea.classList.remove("dragover");
    });
  });

  dropArea.addEventListener("drop", (e) => {
    selectedFiles = Array.from(e.dataTransfer.files).filter(file => file.name.endsWith(".pdf"));
    renderFileList();
  });
}

function renderFileList() {
  fileList.innerHTML = "";
  selectedFiles.forEach(file => {
    const div = document.createElement("div");
    div.className = "file-item";
    div.textContent = file.name;
    fileList.appendChild(div);
  });
}

async function loadTemplate(templateName) {
  const response = await fetch(`/jd-template/${templateName}`);
  const data = await response.json();
  document.getElementById("job_description").value = data.template;
}

function createTags(items, className) {
  if (!items || items.length === 0) return "<p>No data available</p>";
  return items.map(item => `<span class="tag ${className}">${item}</span>`).join("");
}

function createRoleList(roles) {
  if (!roles || roles.length === 0) return "<p>No recommended roles</p>";
  return `<ul>${roles.map(r => `<li>${r.role} (${r.score} matched skills)</li>`).join("")}</ul>`;
}

function createResumeCard(result, index) {
  return `
    <div class="result-card">
      <h2>Resume ${index + 1}: ${result.file_name}</h2>

      <div class="metrics">
        <div class="metric-card"><h3>Skill Match</h3><p>${result.skill_score}%</p></div>
        <div class="metric-card"><h3>Text Similarity</h3><p>${result.similarity_score}%</p></div>
        <div class="metric-card"><h3>ATS Score</h3><p>${result.ats_score}%</p></div>
        <div class="metric-card"><h3>Predicted Role</h3><p>${result.predicted_role}</p></div>
      </div>

      <h3>Resume Skills</h3>
      <div>${createTags(result.resume_skills, "skill")}</div>

      <h3>Matched Skills</h3>
      <div>${createTags(result.matched_skills, "matched")}</div>

      <h3>Missing Skills</h3>
      <div>${createTags(result.missing_skills, "missing")}</div>

      <h3>Recommended Roles</h3>
      ${createRoleList(result.recommended_roles)}

      <div class="chart-wrap">
        <canvas id="chart-${index}"></canvas>
      </div>
    </div>
  `;
}

document.getElementById("analyzeForm")?.addEventListener("submit", async function(e) {
  e.preventDefault();

  if (selectedFiles.length === 0) {
    alert("Please upload at least one PDF resume.");
    return;
  }

  const formData = new FormData();
  selectedFiles.forEach(file => formData.append("resumes", file));
  formData.append("job_description", document.getElementById("job_description").value);

  const response = await fetch("/analyze", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  latestResults = data;

  resultsDiv.classList.remove("hidden");
  downloadBtn.classList.remove("hidden");

  resultsDiv.innerHTML = data.results.map((result, index) => createResumeCard(result, index)).join("");

  data.results.forEach((result, index) => {
    const ctx = document.getElementById(`chart-${index}`).getContext("2d");
    new Chart(ctx, {
      type: "radar",
      data: {
        labels: ["Skill Match", "Similarity", "ATS"],
        datasets: [{
          label: result.file_name,
          data: [result.skill_score, result.similarity_score, result.ats_score]
        }]
      },
      options: {
        scales: {
          r: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  });
});

downloadBtn?.addEventListener("click", async function() {
  if (!latestResults) return;

  const response = await fetch("/download-pdf", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(latestResults)
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "resume_analysis_report.pdf";
  a.click();
  window.URL.revokeObjectURL(url);
});