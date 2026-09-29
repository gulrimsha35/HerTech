
let currentMode = "tabular";

let generatedData = null;

const promptBox = document.getElementById("prompt");
const generateButton = document.getElementById("generateButton");
const resultBox = document.getElementById("result");

const tabularTab = document.getElementById("tabularTab");
const relationalTab = document.getElementById("relationalTab");

const downloadButtons = document.getElementById("downloadButtons");
const downloadCsvButton = document.getElementById("downloadCsvButton");
const downloadJsonButton = document.getElementById("downloadJsonButton");


generateButton.addEventListener("click", async function () {

    const prompt = promptBox.value.trim();

    if (prompt === "") {
        resultBox.innerHTML =
            "Please describe the data you want to generate.";
        return;
    }

    resultBox.innerHTML = "Generating data...";
    downloadButtons.style.display = "none";

    try {

        let endpoint;

        if (currentMode === "relational") {
            endpoint = "http://127.0.0.1:8000/generate-relational";
        } else {
            endpoint = "http://127.0.0.1:8000/generate";
        }

        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: prompt
            })
        });

        const result = await response.json();

        if (!response.ok) {
            resultBox.innerHTML =
                "Something went wrong.";

            console.error(result);
            return;
        }

        generatedData = result.data;

        displayData(generatedData);

        downloadButtons.style.display = "block";

    } catch (error) {

        resultBox.innerHTML =
            "Could not connect to the HackData AI backend.";

        console.error(error);
    }
});


function displayData(data) {

    if (currentMode === "relational") {

        let output = "";

        for (const tableName in data) {

            const records = data[tableName];

            output += `<h3>${tableName}</h3>`;

            if (records.length === 0) {
                output += "<p>No records generated.</p>";
                continue;
            }

            const columns = Object.keys(records[0]);

            output += "<table>";

            output += "<thead><tr>";

            columns.forEach(function (column) {
                output += `<th>${column}</th>`;
            });

            output += "</tr></thead>";

            output += "<tbody>";

            records.forEach(function (row) {

                output += "<tr>";

                columns.forEach(function (column) {
                    output += `<td>${row[column]}</td>`;
                });

                output += "</tr>";
            });

            output += "</tbody>";
            output += "</table>";
        }

        resultBox.innerHTML = output;

        return;
    }


    if (!Array.isArray(data) || data.length === 0) {

        resultBox.innerHTML =
            "No data was generated.";

        return;
    }

    const columns = Object.keys(data[0]);

    let table = "<table>";

    table += "<thead><tr>";

    columns.forEach(function (column) {
        table += `<th>${column}</th>`;
    });

    table += "</tr></thead>";

    table += "<tbody>";

    data.forEach(function (row) {

        table += "<tr>";

        columns.forEach(function (column) {
            table += `<td>${row[column]}</td>`;
        });

        table += "</tr>";
    });

    table += "</tbody>";
    table += "</table>";

    resultBox.innerHTML = table;
}


function downloadJSON() {

    const jsonData = JSON.stringify(generatedData, null, 2);

    const blob = new Blob(
        [jsonData],
        { type: "application/json" }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "hackdata_generated.json";

    link.click();

    URL.revokeObjectURL(url);
}


function downloadCSV() {

    if (currentMode === "relational") {

        let csvFiles = [];

        for (const tableName in generatedData) {

            const records = generatedData[tableName];

            if (!records || records.length === 0) {
                continue;
            }

            const columns = Object.keys(records[0]);

            let csv = columns.join(",") + "\n";

            records.forEach(function (row) {

                const values = columns.map(function (column) {

                    let value = row[column];

                    if (value === null || value === undefined) {
                        value = "";
                    }

                    value = String(value).replace(/"/g, '""');

                    return `"${value}"`;
                });

                csv += values.join(",") + "\n";
            });

            csvFiles.push({
                name: tableName,
                content: csv
            });
        }

        if (csvFiles.length === 0) {
            return;
        }

        csvFiles.forEach(function (file) {

            const blob = new Blob(
                [file.content],
                { type: "text/csv" }
            );

            const url = URL.createObjectURL(blob);

            const link = document.createElement("a");

            link.href = url;
            link.download = file.name + ".csv";

            link.click();

            URL.revokeObjectURL(url);
        });

        return;
    }


    if (!Array.isArray(generatedData) || generatedData.length === 0) {
        return;
    }

    const columns = Object.keys(generatedData[0]);

    let csv = columns.join(",") + "\n";

    generatedData.forEach(function (row) {

        const values = columns.map(function (column) {

            let value = row[column];

            if (value === null || value === undefined) {
                value = "";
            }

            value = String(value).replace(/"/g, '""');

            return `"${value}"`;
        });

        csv += values.join(",") + "\n";
    });

    const blob = new Blob(
        [csv],
        { type: "text/csv" }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "hackdata_generated.csv";

    link.click();

    URL.revokeObjectURL(url);
}


downloadJsonButton.addEventListener("click", downloadJSON);

downloadCsvButton.addEventListener("click", downloadCSV);


tabularTab.addEventListener("click", function () {

    currentMode = "tabular";

    promptBox.placeholder =
        "Example: Generate 10 students with student ID, name, email and city.";

    resultBox.innerHTML =
        "Tabular data generator selected.";

    downloadButtons.style.display = "none";
});


relationalTab.addEventListener("click", function () {

    currentMode = "relational";

    promptBox.placeholder =
        "Example: Generate 10 students, 5 courses and 20 enrollments.";

    resultBox.innerHTML =
        "Relational data generator selected.";

    downloadButtons.style.display = "none";
});

