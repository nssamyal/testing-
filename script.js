document.addEventListener("DOMContentLoaded", function () {
    const predictBtn = document.getElementById("predictBtn");
    const fileInput = document.getElementById("fileInput");
    const resultDiv = document.getElementById("result");
    
    if (!predictBtn || !fileInput || !resultDiv) {
        console.error("Missing elements in HTML");
        return;
    }

    predictBtn.addEventListener("click", function () {
        console.log("Predict Button Clicked!");
        
        const file = fileInput.files[0];
        if (!file) {
            alert("Please upload a CSV file first.");
            return;
        }
        
        const formData = new FormData();
        formData.append("file", file);
        
        fetch("/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("API Response:", data);
            if (data.error) {
                resultDiv.innerText = "Error: " + data.error;
            } else {
                resultDiv.innerText = "Prediction: " + JSON.stringify(data.prediction);
                renderCharts(data.prediction);
            }
        })
        .catch(error => {
            console.error("Error in fetching prediction:", error);
            resultDiv.innerText = "Error in fetching prediction";
        });
    });

    function renderCharts(predictionData) {
        const binaryCtx = document.getElementById("binaryChart").getContext("2d");
        const multiCtx = document.getElementById("multiChart").getContext("2d");
        
        if (!binaryCtx || !multiCtx) {
            console.error("Canvas elements not found");
            return;
        }
        
        new Chart(binaryCtx, {
            type: "bar",
            data: {
                labels: Object.keys(predictionData.binary),
                datasets: [{
                    label: "Binary Classification",
                    data: Object.values(predictionData.binary),
                    backgroundColor: "rgba(54, 162, 235, 0.6)"
                }]
            }
        });

        new Chart(multiCtx, {
            type: "bar",
            data: {
                labels: Object.keys(predictionData.multi),
                datasets: [{
                    label: "Multiclass Classification",
                    data: Object.values(predictionData.multi),
                    backgroundColor: "rgba(255, 99, 132, 0.6)"
                }]
            }
        });
    }
});
