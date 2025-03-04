document.addEventListener('DOMContentLoaded', function() {
    const timerDisplay = document.getElementById('timer');
    const totalTime = 20 * 60; // Total time in seconds (20 minutes)
    let remainingTime = totalTime;

    function updateTimer() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        timerDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        remainingTime--;

        if (remainingTime < 0) {
            clearInterval(timerInterval);
            alert('Time is up!');
            // Handle time up (e.g., auto-submit the test)
            document.getElementById('test-form').submit(); // Change 'test-form' to your form ID
        }
    }

    // Update the timer every second
    const timerInterval = setInterval(updateTimer, 1000);

    // Optional: Stop timer if test is submitted manually
    document.getElementById('submit-button').addEventListener('click', function() {
        clearInterval(timerInterval);
    });
});

let testId;
let answers = {};

function startTest() {
    fetch('/start_test', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        testId = data.test_id;
        displayQuestions(data.questions);
    });
}

function displayQuestions(questions) {
    const questionsContainer = document.getElementById('questions-container');
    questionsContainer.innerHTML = '';
    Object.keys(questions).forEach(parameter => {
        questions[parameter].forEach((q, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            questionDiv.innerHTML = `
                <h3>${parameter} - Question ${index + 1}</h3>
                <p>${q.text}</p>
                <ul class="options">
                    <li><label><input type="radio" name="question-${q.id}" value="A" onclick="saveAnswer(${q.id}, 'A')"> ${q.options[0]}</label></li>
                    <li><label><input type="radio" name="question-${q.id}" value="B" onclick="saveAnswer(${q.id}, 'B')"> ${q.options[1]}</label></li>
                    <li><label><input type="radio" name="question-${q.id}" value="C" onclick="saveAnswer(${q.id}, 'C')"> ${q.options[2]}</label></li>
                    <li><label><input type="radio" name="question-${q.id}" value="D" onclick="saveAnswer(${q.id}, 'D')"> ${q.options[3]}</label></li>
                </ul>
            `;
            questionsContainer.appendChild(questionDiv);
        });
    });
    document.getElementById('submit-button').disabled = false;
}

function saveAnswer(questionId, answer) {
    answers[questionId] = answer;
}

function submitTest() {
    fetch('/submit_test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            test_id: testId,
            answers: answers
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('test-container').style.display = 'none';
        document.getElementById('result-container').style.display = 'block';
        document.getElementById('job-field').innerText = `Your Recommended Job Field: ${data.job_field}`;

    const scoresContainer = document.getElementById('scores-container');
    let scoresHtml = '<h3></h3><ul>';
    const colors = [
        '#e57373', '#64b5f6', '#ba68c8', '#ffb74d', '#ef5350',
        '#4db6ac', '#9575cd', '#ff8a65', '#ffd54f', '#81c784'
    ];

    Object.entries(data.scores).forEach(([parameter, score], index) => {
        scoresHtml += `
            <li style="list-style: none; margin-bottom: 10px; style=list-style-type: none;">
                <span style="display: inline-block; width: 12px; height: 12px; background-color: ${colors[index]}; border-radius: 50%; margin-right: 10px;"></span>
                ${parameter}: ${score}
            </li>`;
    });

    scoresHtml += `<li>Total Marks: ${Object.values(data.scores).reduce((a, b) => a + b, 0)}</li></ul>`;
    scoresContainer.innerHTML = scoresHtml;

    // Custom Chart.js Configuration
    const chartConfig = {
        type: 'bar',
        data: {
            labels: Object.keys(data.scores),
            datasets: [{
                label: 'Your Scores',
                data: Object.values(data.scores),
                backgroundColor: colors,
                borderColor: [
                    '#c62828', '#1565c0', '#7b1fa2', '#ff8f00', '#d32f2f',
                    '#00897b', '#512da8', '#d84315', '#f9a825', '#388e3c'
                ],
                borderWidth: 1
            }]
        },
        options: {
            animation: {
                duration: 1500,
                easing: 'easeInOutBounce'
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    };

    // Create the chart
    const ctx = document.getElementById('score-chart').getContext('2d');
    new Chart(ctx, chartConfig);




    const qualities = data.qualities;
    const qualityCounts = qualities.reduce((acc, quality) => {
        acc[quality] = (acc[quality] || 0) + 1;
        return acc;
    }, {});

    const labels = Object.keys(qualityCounts);
    const dataPoints = labels.map(label => qualityCounts[label]);

    const ctx1 = document.getElementById('qualities-pie-chart').getContext('2d');
    new Chart(ctx1, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Qualities',
                data: dataPoints,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(199, 199, 199, 0.2)',
                    'rgba(83, 102, 255, 0.2)',
                    'rgba(255, 99, 255, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(155, 162, 135, 0.2)',
                    'rgba(231, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(199, 199, 199, 1)',
                    'rgba(83, 102, 255, 1)',
                    'rgba(255, 99, 255, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(155, 162, 135, 1)',
                    'rgba(231, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
        datalabels: {
            formatter: (value, ctx) => {
                let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                let percentage = (value / sum * 100).toFixed(2) + "%";
                return percentage;
            },
            color: '#fff',
            font: {
                weight: 'bold'
            }
        }
    }
},
plugins: [ChartDataLabels]
        }
    )});
}
// Start the test as soon as the page loads
window.onload = startTest;
//<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0/dist/chartjs-plugin-datalabels.min.js"></script>
