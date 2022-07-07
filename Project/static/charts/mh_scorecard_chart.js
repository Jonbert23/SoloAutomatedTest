(function brk_chart(){
    const ctx = document.getElementById('scorecard_chart');
    const metric_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Yesterday', 'Today', 'Tomorrow'],
            datasets: 
            [
                {
                    label: 'Mainview Production',
                    data: [40000, 30659, 25000],
                    backgroundColor: [
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                    ],
                },
                {
                    label: 'Scorecard Production',
                    data: [40000, 30659, 25000],
                    backgroundColor: [
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                    ],
                },
                {
                    label: 'Mainview Goal',
                    data: [31355, 41659, 45883  ],
                    backgroundColor: [
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                    ],
                },
                {
                    label: 'Scorecard Goal',
                    data: [31355, 41659, 45883  ],
                    backgroundColor: [
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
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