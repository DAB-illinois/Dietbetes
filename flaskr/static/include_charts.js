// get bar chart canvas
var serving_chart = document.getElementById("serving_chart").getContext("2d");
var carb_chart = document.getElementById("carb_chart").getContext("2d");
var compare_chart = document.getElementById("compare_chart").getContext("2d");

// bar chart data
mainGraphColorTransparent = "rgba(77, 255, 77, 0.6)";
mainGraphColorOpaque = "rgba(77, 255, 77, 1)";
barChartBorderWidth = 1.5;

steps = 10
max = 10
// draw bar chart

new Chart(serving_chart, {
    type: 'bar',
    data: {
        labels: [{% for item in serv_labels %}
            "{{item}}", {% endfor %}
        ],
        datasets: [{
            backgroundColor: mainGraphColorTransparent,
            borderColor: mainGraphColorOpaque,
            borderWidth: barChartBorderWidth,
            data: [{% for item in serv_values %} {{ item }},
                {% endfor %}
            ]
        }]
    },
    options: {
        legend: { display: false },
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                },
            scaleLabel: {
			        display: true,
			        labelString: 'Servings'
			    }    
            }],
            xAxes: [{ 
                scaleLabel: {
			        display: true,
			        labelString: 'Dates'
			    }
            }]
        }
	}
});

new Chart(carb_chart, {
    type: 'bar',
    data: {
        labels: [{% for item in carb_labels %}
            "{{item}}", {% endfor %}
        ],
        datasets: [{
            backgroundColor: mainGraphColorTransparent,
            borderColor: mainGraphColorOpaque,
            borderWidth: barChartBorderWidth,
            data: [{% for item in carb_values %} {{ item }},
                {% endfor %}
            ]
        }]
    },
    options: {
        legend: { display: false },
		maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                },
            scaleLabel: {
			        display: true,
			        labelString: 'Amount of Carbohydrate'
			    }
            }],
            xAxes: [{ 
                scaleLabel: {
			        display: true,
			        labelString: 'Dates'
			    }
            }]
        }
    }
});

new Chart(compare_chart, {
    type: 'scatter',
    data: {
        datasets: [{
            backgroundColor: mainGraphColorTransparent,
            fill: false,
            showLine: false,
            borderColor: mainGraphColorOpaque,
            data: [{% for item in scatter_values %} {
                    x: {{ item[0] }},
                    y: {{ item[1] }}
                },
                {% endfor %}
            ]
        }]
    },
    options: {
        legend: { display: false },
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                }, 
                scaleLabel: {
			        display: true,
			        labelString: 'Age'
			    }
            }],
            xAxes: [{
                ticks: {
                    beginAtZero:true,
                }, 
                scaleLabel: {
			        display: true,
			        labelString: 'A1C Level'
			    }
            }]
        }
    }
});