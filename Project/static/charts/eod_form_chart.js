(function breakdown_chart()
{
    const sample = document.getElementById('breakdown_chart');
    const myChart = new Chart(sample, {
        type: 'doughnut',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [35, 65],
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

(function mail_chart()
{
    const sample = document.getElementById('mail_chart');
    const myChart = new Chart(sample, {
        type: 'doughnut',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [65, 35],
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
