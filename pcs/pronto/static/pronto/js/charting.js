function pronto_chart() {
    $.getJSON("get_pronto_charting_day", function(jsonData) {
        var chart = new Highcharts.Chart("container_line_char", {
            title: {
                text: 'PSW3 Pronto Statics'
            },
            xAxis: {
                title: "Date",
                categories : jsonData['date'],
                type : 'category'
            },
            yAxis: {
                title: {
                    text: 'Number of Pronto'
                },
                min:0
            },
            exporting: {
                enabled: true
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
            series: [{
                name: 'Num Of WOH(Total)',
                data: jsonData['total']
            },
            {
                name: 'Num Of Closed',
                data: jsonData['Closed']
            },
            {
                name: 'Num Of Transferred',
                data: jsonData['Transferred']
            },
            {
                name: 'Num Of CNN',
                data: jsonData['CNN']
            },
            {
                name: 'Num Of Block',
                data: jsonData['Block']
            },
            {
                name: 'Num Of Investigating',
                data: jsonData['Investigating']
            }]
        });
    });
};

function pie_chart(html_id, attribute) {
    url = "get_pronto_ratio?&attribute=" + attribute
    $.getJSON(url , function(jsonData) {
        var chart = new Highcharts.chart(html_id, {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Browser pronto ratio for ' + attribute
            },
            tooltip: {
                pointFormat: '</b>: {point.percentage:.1f} % ({point.y})</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}: </b>{point.percentage:.1f}%',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            series: [{
                name: attribute,
                colorByPoint: true,
                data: jsonData
            }]
        });
    });
};

function stacked_percentage_column(html_id) {
    url = "get_pronto_top"
    $.getJSON(url , function(jsonData) {
        Highcharts.chart(html_id, {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Top Pronto Ratio Statics'
            },
            xAxis: {
                categories: jsonData['date']
            },
            yAxis: {
                allowDecimals: false,
                min: 0,
                title: {
                    text: 'Distribution of Pronto numbers'
                },
                stackLabels: {
                enabled: true,
                    style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                    }
                }
            },
            legend: {
                align: 'right',
                x: -30,
                verticalAlign: 'top',
                y: 25,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false
            },
            tooltip: {
                headerFormat: '<b>{point.x}</b><br/>',
                pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: false
//                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                    }
                }
            },
            series: [{
                color: "red",
                name: 'TOP',
                data: jsonData["count_top"]
            },
            {
                color: "green",
                name: 'NO TOP',
                data: jsonData["count_no_top"]
            }]
        });
    });
};

function stacked_percentage_column_priority(html_id) {
    url = "get_pronto_priority"
    $.getJSON(url , function(jsonData) {
        Highcharts.chart(html_id, {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Pronto Priority Ratio Statics'
            },
            xAxis: {
                categories: jsonData['date']
            },
            yAxis: {
                allowDecimals: false,
                min: 0,
                title: {
                    text: 'Distribution of Pronto numbers'
                },
                stackLabels: {
                    enabled: true,
                        style: {
                        fontWeight: 'bold',
                        color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                    }
                }
            },
            legend: {
                align: 'right',
                x: -30,
                verticalAlign: 'top',
                y: 25,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                borderColor: '#CCC',
                borderWidth: 1,
                shadow: false
            },
            tooltip: {
                headerFormat: '<b>{point.x}</b><br/>',
                pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: false
//                        color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                    }
                }
            },
            series: [{
                color: "red",
                name: 'A - Critical',
                data: jsonData["A - Critical"]
            },
            {
                color: "yellow",
                name: 'B - Major',
                data: jsonData["B - Major"]
            },
            {
                color: "green",
                name: 'C - Minor',
                data: jsonData["C - Minor"]
            }]
        });
    });
};


function get_pronto_time(html_id) {
    url = "get_pronto_time"
    $.getJSON(url , function(jsonData) {
        Highcharts.chart(html_id, {
            chart: {
                type: 'column'
            },
            title: {
                text: 'Time Cost For Pronto'
            },
            subtitle: {
                text: 'Pronto Cost'
            },
            xAxis: {
                categories: jsonData['pronto_id'],
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Time Cost(Days)'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} days</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                },
                series: {
                    cursor: 'pointer',
                    events: {
                        click: function(event) {
                            window.open('https://pronto.int.net.nokia.com/pronto/problemReport.html?prid=' + event.point.category);
                        }
                    }
                }
            },
            series: [{
                name: 'Time For RFT',
                data: jsonData['time_rft']
            }, {
                name: 'Time For Test',
                data: jsonData['time_test']
            }]
        });
    });
};