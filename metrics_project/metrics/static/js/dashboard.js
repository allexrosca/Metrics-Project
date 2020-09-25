$(document).ready(function() {

    var endpoint = 'http://127.0.0.1:8000/api/info/';
    var defaultData= [];
    var labels = [];

    $.ajax({
        method: 'GET',
        url: endpoint,
        success: function (data) {
            $.each(data, function(i,j) {
                defaultData.push(j['value'])
                labels.push(j['date'])
            })
            var ctx = document.getElementById('myChart');
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Value',
                        data: defaultData,
                        fill: false,
                        borderColor: [
                            'rgb(54, 162, 235)',
                        ],
                        borderWidth: 2,
                        pointBackgroundColor: 'rgb(238, 238, 0)',
                        pointBorderColor: 'rgb(238, 238, 0)',
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    },
                    tooltips: {
                        callbacks: {
                            title: function(t, d) {
                                let title = data[t[0]['index']];
                                return 'Id: ' + title.id + '\n' + 'Category: ' + title.category + '\n' + 'Tags: ' + title.tags + '\n' + 'Time: ' + title.time
                            },
                        }
                    },
                }
            });



        },
        error: function (error_data) {
            console.log("error");
            console.log(error_data)
        }
    });
});