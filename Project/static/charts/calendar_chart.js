(function metric_chart(){
    const ctx = document.getElementById('metric_chart');
    const metric_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Scheduled Amount', 'Goal', 'Production'],
            datasets: 
            [
                {
                    label: 'Base Data',
                    data: [12123, 57000, 438441 ],
                    backgroundColor: [
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                    ],
                },
                {
                    label: 'Scrip Data',
                    data: [12123, 57000, 438441 ],
                    backgroundColor: [
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                    ],
                }
            ],
            
        },
        options: {
            scales: 
            {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
})();

(function metric_chart2(){
    const ctx = document.getElementById('metric_chart2');
    const metric_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Appointments', 'New Patients'], 
            datasets: 
            [
                {
                    label: 'Base Data',
                    data: [ 330, 123 ],
                    backgroundColor: [
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                    ],
                },
                {
                    label: 'Scrip Data',
                    data: [320, 100],
                    backgroundColor: [
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                        'rgba(222, 182, 23, 1)',
                    ],
                }
            ],
            
        },
        options: {
            scales: 
            {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
})();


(function filter_test(){
    const ctx = document.getElementById('bar');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Provider Filter', 'Procedure Filter', 'Patient Filter'],
            datasets: 
            [
                {
                    label: 'Pass',
                    data: [70, 55, 90],
                    backgroundColor: [
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)'
                    ],
                },
                {
                    label: 'Fail',
                    data: [30, 45, 10],
                    backgroundColor: [
                        'rgba(246, 51, 21, 1)',
                        'rgba(246, 51, 21, 1)',
                        'rgba(246, 51, 21, 1)'
                    ],
                }
            ],
            
        },
        options: {
            scales: 
            {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
})();


(function app_val_per_day()
{
    const sample = document.getElementById('app_val_per_day');
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

(function app_val_per_day()
{
    const sample = document.getElementById('app_val');
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
