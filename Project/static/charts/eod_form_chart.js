(function breakdown_chart()
{
    const sample = document.getElementById('breakdown_chart');
    const myChart = new Chart(sample, {
        type: 'horizontalBar',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: 
            [
                {
                    data: [30, 45],
                    backgroundColor: [
                        'rgba(38, 144, 244, 1)',
                        'rgba(246, 51, 21, 1)',
                    ],
                },

            ],
            
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        min: 0 // Edit the value according to what you need
                    }
                }],
                yAxes: [{
                    stacked: true
                }]
            },
            legend: {
                display: false //This will do the task
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
