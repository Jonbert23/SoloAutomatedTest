(function ytd_breakdown_chart()
{
    const sample = document.getElementById('ytd_breakdown_chart');
    const myChart = new Chart(sample, {
        type: 'doughnut',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [40, 60],
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

(function tdy_breakdown_chart()
{
    const sample = document.getElementById('tdy_breakdown_chart');
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



(function trw_breakdown_chart()
{
    const sample = document.getElementById('trw_breakdown_chart');
    const myChart = new Chart(sample, {
        type: 'doughnut',
        data: {
            labels: ['Pass', 'Fail'],
            datasets: [{
                data: [50, 50],
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

