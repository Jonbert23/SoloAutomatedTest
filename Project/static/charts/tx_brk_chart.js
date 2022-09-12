(function brk_chart(){
    const ctx = document.getElementById('brk_chart');
    const metric_chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan 2021', 'Feb 2021', 'Mar 2021', 'Apr 2021', 'May 2021', 'Jun 2021', 'Jul 2021', 'Aug 2021', 'Sep 2021', 'Oct 2021', 'Nov 2021', 'Dec 2021'],
            datasets: 
            [
                {
                    label: 'Main:Pending Sched',
                    data: [40000, 30659, 25000, 23000, 40000, 30659, 25000, 23000, 40000, 30659, 25000, 23000,],
                    backgroundColor: [
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                        'rgb(153, 107, 229)',
                    ],
                },
                {
                    label: 'Brk:Pending Sched',
                    data: [40000, 30659, 25000, 23000, 40000, 30659, 25000, 23000, 40000, 30659, 25000, 23000,],
                    backgroundColor: [
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                        'rgb(97, 67, 156)',
                    ],
                },
                {
                    label: 'Main:Pending Unsched ',
                    data: [31355, 41659, 45883,23000,31355, 41659, 45883,23000,31355, 41659, 45883,23000  ],
                    backgroundColor: [
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                        'rgb(109, 229, 193)',
                    ],
                },
                {
                    label: 'Brk:Pending Unsched ',
                    data: [31355, 41659, 45883,31355, 41659, 45883,31355, 41659, 45883, 31355, 50659, 45883 ],
                    backgroundColor: [
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                        'rgb(74, 192, 156)',
                    ],
                },
                {
                    label: 'Main:Active Production',
                    data: [25355, 45659, 23883, 27980,25355, 45659, 23883, 27980,25355, 45659, 23883, 27980  ],
                    backgroundColor: [
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                        'rgb(0, 194, 255)',
                    ],
                },
                {
                    label: 'Brk:Active Production',
                    data: [25355, 45659, 40659, 23883, 25980, 45659, 23883, 27980,20355, 40659, 23883, 25980  ],
                    backgroundColor: [
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                        'rgb(0, 102, 255)',
                    ],
                }
            ],
            
        },
        options: {
            indexAxis: 'x',
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