(function tx_provider_filter_chart()
{
    const sample = document.getElementById('tx_provider_filter_chart');
    const myChart = new Chart(sample, {
        type: 'doughnut',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [90, 10],
                backgroundColor: [
                    'rgba(38, 144, 244, 1)',
                    'rgba(246, 51, 21, 1)',
                    
                ],
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
})();

(function tx_procedure_filter_chart()
{
    const sample = document.getElementById('tx_procedure_filter_chart');
    const myChart = new Chart(sample, {
        type: 'doughnut',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [10, 90],
                backgroundColor: [
                    'rgba(38, 144, 244, 1)',
                    'rgba(246, 51, 21, 1)',
                ],
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true 
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
})();



(function tx_patient_filter_chart()
{
    const sample = document.getElementById('tx_patient_filter_chart');
    const myChart = new Chart(sample, {
        type: 'doughnut',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [30, 70],
                backgroundColor: [
                    'rgba(38, 144, 244, 1)',
                    'rgba(246, 51, 21, 1)',
                ],
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true 
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
})();

