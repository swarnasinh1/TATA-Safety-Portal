// Welcome Message
console.log("TATA Safety Portal Loaded");

// Generate Unique Report ID
function generateReportId() {
    return "TSR-" + Math.floor(Math.random() * 1000000);
}

// Save Incident Report
function saveReport(event) {
    event.preventDefault();

    const report = {
        reportId: generateReportId(),
        employeeName: document.getElementById("employeeName").value,
        employeeId: document.getElementById("employeeId").value,
        plant: document.getElementById("plant").value,
        location: document.getElementById("location").value,
        incidentType: document.getElementById("incidentType").value,
        severity: document.getElementById("severity").value,
        description: document.getElementById("description").value,
        date: document.getElementById("incidentDate").value,
        status: "Open"
    };

    let reports =
        JSON.parse(localStorage.getItem("reports")) || [];

    reports.push(report);

    localStorage.setItem(
        "reports",
        JSON.stringify(reports)
    );

    localStorage.setItem(
        "latestReportId",
        report.reportId
    );

    window.location.href = "success.html";
}

// Display Reports
function loadReports() {

    const tableBody =
        document.getElementById("reportsTableBody");

    if (!tableBody) return;

    let reports =
        JSON.parse(localStorage.getItem("reports")) || [];

    tableBody.innerHTML = "";

    reports.forEach(report => {

        tableBody.innerHTML += `
            <tr>
                <td>${report.reportId}</td>
                <td>${report.plant}</td>
                <td>${report.date}</td>
                <td>${report.location}</td>
                <td>${report.incidentType}</td>
                <td>${report.severity}</td>
                <td>${report.status}</td>
            </tr>
        `;
    });
}

// Display Latest Report ID
function loadSuccessPage() {

    const reportIdElement =
        document.getElementById("reportId");

    if (!reportIdElement) return;

    let reportId =
        localStorage.getItem("latestReportId");

    reportIdElement.textContent =
        reportId || "TSR-000000";
}

// Dashboard Statistics
function loadStatistics() {

    let reports =
        JSON.parse(localStorage.getItem("reports")) || [];

    const totalReports =
        document.getElementById("totalReports");

    if(totalReports){
        totalReports.textContent =
            reports.length;
    }

    const openCases =
        document.getElementById("openCases");

    if(openCases){
        openCases.textContent =
            reports.filter(r => r.status === "Open").length;
    }

    const closedCases =
        document.getElementById("closedCases");

    if(closedCases){
        closedCases.textContent =
            reports.filter(r => r.status === "Closed").length;
    }
}

// Register Validation
function validateRegisterForm(event) {

    const password =
        document.getElementById("password").value;

    const confirmPassword =
        document.getElementById("confirmPassword").value;

    if(password !== confirmPassword){

        alert("Passwords do not match!");
        event.preventDefault();
        return false;
    }

    return true;
}

// Search Reports
function searchReports() {

    const input =
        document.getElementById("searchInput").value
        .toUpperCase();

    const rows =
        document.querySelectorAll("#reportsTableBody tr");

    rows.forEach(row => {

        const reportId =
            row.cells[0].innerText.toUpperCase();

        row.style.display =
            reportId.includes(input)
            ? ""
            : "none";
    });
}

// Run on Page Load
window.onload = function() {

    loadReports();
    loadSuccessPage();
    loadStatistics();

};