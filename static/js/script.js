document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("uploadForm").addEventListener("submit", function(e) {
        e.preventDefault();
        handleAnalyze();
    });
});

function toggleDark() {
    document.body.classList.toggle("dark");
}

async function handleAnalyze() {
    const form = document.getElementById("uploadForm");
    const loader = document.getElementById("loader");

    if (!form.job_description.value.trim()) {
        alert("Enter Job Description");
        return;
    }

    if (form.resumes.files.length === 0) {
        alert("Upload at least one resume");
        return;
    }

    loader.style.display = "block";

    try {
        const res = await fetch("/analyze", {
            method: "POST",
            body: new FormData(form)
        });

        const candidates = await res.json();

        if (window.showDashboard) window.showDashboard();

        showCards(candidates);
        drawCharts(candidates);

    } catch (err) {
        console.error(err);
        alert("Something went wrong, check the console");
    }

    loader.style.display = "none";
}

function showCards(candidates) {
    const list = document.getElementById("results");
    const stats = document.getElementById("summary");

    list.innerHTML = "";

    candidates.sort((a, b) => b.score - a.score);

    const count = candidates.length;
    const avgScore = (candidates.reduce((sum, c) => sum + c.score, 0) / count).toFixed(1);
    const best = candidates[0].score;

    stats.innerHTML = `
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-value">${count}</div>
            <div class="kpi-label">Resumes Analyzed</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-value">${avgScore}%</div>
            <div class="kpi-label">Average Score</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-value">${best}%</div>
            <div class="kpi-label">Top Candidate</div>
        </div>
    `;

    candidates.forEach((person, i) => {
        let color = "score-low";
        if (person.score > 70) color = "score-high";
        else if (person.score > 40) color = "score-mid";

        const card = document.createElement("div");
        card.className = "card " + (i === 0 ? "top" : "");

        card.innerHTML = `
            <div class="rank-badge">${i === 0 ? "" : i + 1}</div>

            <div class="card-body">
                <div class="card-name">
                    ${person.name}
                    ${i === 0 ? '<span class="top-badge">TOP PICK</span>' : ""}
                </div>
                <div class="sub-scores">
                    <span class="sub-pill"> Skills <strong>${person.skills}%</strong></span>
                    <span class="sub-pill"> Exp <strong>${person.experience}%</strong></span>
                    <span class="sub-pill"> Edu <strong>${person.education}%</strong></span>
                </div>
                <div class="progress-wrap">
                    <div class="progress">
                        <div class="bar" style="width:${person.score}%"></div>
                    </div>
                </div>
            </div>

            <div class="score-badge ${color}">${person.score}%</div>
        `;

        list.appendChild(card);
    });
}

let barChart, radarChart;

function drawCharts(candidates) {
    candidates.sort((a, b) => b.score - a.score);

    const names = candidates.map(c => c.name);

    const colors = {
        overall:    "rgba(0,51,255,0.75)",
        skills:     "rgba(232,160,0,0.75)",
        experience: "rgba(0,128,58,0.75)",
        education:  "rgba(255,59,0,0.75)"
    };

    const barStyle = { borderRadius: 5, borderWidth: 0 };

    const barCtx = document.getElementById("barChart");
    if (barChart) barChart.destroy();

    barChart = new Chart(barCtx, {
        type: "bar",
        data: {
            labels: names,
            datasets: [
                { label: "Overall",    data: candidates.map(c => c.score),      backgroundColor: colors.overall,    ...barStyle },
                { label: "Skills",     data: candidates.map(c => c.skills),     backgroundColor: colors.skills,     ...barStyle },
                { label: "Experience", data: candidates.map(c => c.experience), backgroundColor: colors.experience, ...barStyle },
                { label: "Education",  data: candidates.map(c => c.education),  backgroundColor: colors.education,  ...barStyle }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "top",
                    labels: {
                        font: { family: "'DM Mono', monospace", size: 11 },
                        usePointStyle: true,
                        pointStyle: "rectRounded"
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: "rgba(128,128,128,0.1)" },
                    ticks: { font: { family: "'DM Mono', monospace", size: 10 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: "'DM Mono', monospace", size: 10 } }
                }
            }
        }
    });

    // radar is just for the top person
    const winner = candidates[0];
    const radarCtx = document.getElementById("radarChart");
    if (radarChart) radarChart.destroy();

    radarChart = new Chart(radarCtx, {
        type: "radar",
        data: {
            labels: ["Overall", "Skills", "Experience", "Education"],
            datasets: [{
                label: winner.name,
                data: [winner.score, winner.skills, winner.experience, winner.education],
                backgroundColor: "rgba(0,51,255,0.12)",
                borderColor: "#0e440e",
                borderWidth: 2,
                pointBackgroundColor: "#0033ff",
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        font: { family: "'DM Mono', monospace", size: 11 },
                        usePointStyle: true
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { font: { family: "'DM Mono', monospace", size: 9 }, stepSize: 25 },
                    grid: { color: "rgba(128,128,128,0.15)" },
                    pointLabels: { font: { family: "'Syne', sans-serif", size: 11, weight: "600" } }
                }
            }
        }
    });
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFont("helvetica", "bold");
    doc.setFontSize(18);
    doc.text("RecruitTalent: Resume Analysis Report", 14, 20);

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.setTextColor(120);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 28);

    doc.setDrawColor(200);
    doc.line(14, 32, 196, 32);

    let y = 42;
    doc.setTextColor(0);

    document.querySelectorAll(".card").forEach(card => {
        const lines = card.innerText.split("\n").map(l => l.trim()).filter(Boolean);
        lines.forEach(line => {
            if (y > 270) { doc.addPage(); y = 20; }
            doc.setFontSize(10);
            doc.text(line.substring(0, 100), 14, y);
            y += 6;
        });
        y += 4;
    });

    doc.save("RecruitTalent_Report.pdf");
}
