(function brk_chart(){
    const ctx = document.getElementById('brk_chart');
    const metric_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Net Production', 'Gross Production', 'Collection', 'Adjustment'],
            datasets: 
            [
                {
                    label: 'Base Data',
                    data: [31355, 41659, 45883, -10303  ],
                    backgroundColor: [
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                    ],
                },
                {
                    label: 'Breakdown Data',
                    data: [31355, 41659, 45883, -10303  ],
                    backgroundColor: [
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

(function brk_chart2(){
    const ctx = document.getElementById('brk_chart2');
    const metric_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['New Patients Visits', 'Existing Patients Visits'],
            datasets: 
            [
                {
                    label: 'Base Data',
                    data: [45, 203 ],
                    backgroundColor: [
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                    ],
                },
                {
                    label: 'Breakdown Data',
                    data: [45, 203  ],
                    backgroundColor: [
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

(function production_figures_test(){
    const ctx = document.getElementById('production_figures_test');
    const metric_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Production Data'],
            datasets: 
            [
                {
                    label: "Financial Data",
                    backgroundColor: "rgba(38, 144, 244, 1)",
                    data: [45204],
                 },{
                    label: "Provider Data",
                    backgroundColor: "rgba(222, 182, 23, 1)",
                    data: [45204],
                 },{
                    label: "Table Total",
                    backgroundColor: " rgba(246, 51, 21, 1)",
                    data: [45204],
                 },{
                    label: "Payor Score",
                    backgroundColor: "rgba(164, 20, 195, 1)",
                    data: [40000],
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


(function services_test(){
    const ctx = document.getElementById('services_test');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Search Procedure', 'Count Breakdown'],
            datasets: 
            [
                {
                    label: 'Pass',
                    data: [70, 55],
                    backgroundColor: [
                        'rgba(38, 144, 244, 1)',
                        'rgba(38, 144, 244, 1)',
                    ],
                },
                {
                    label: 'Fail',
                    data: [30, 45],
                    backgroundColor: [
                        'rgba(246, 51, 21, 1)',
                        'rgba(246, 51, 21, 1)',
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

(function lob_filter_test()
{
    const lob = document.getElementById('lob_filter');
    const myChart = new Chart(lob, {
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