var temperatureSocket = new WebSocket('ws://127.0.0.1:8000/ws/temperature_realtime_chart/');
// var socket = new WebSocket('ws://' + window.location.host +':' + window.location.port + '/ws/charts/' + '0' + '/');

// 'ws://' + window.location.host + '/ws/charts/' + '0' + '/'

// var myChart = echarts.init(document.getElementById('chart-temperature-10s'));
//
// // Specify the configuration items and data for the chart
// var option = {
//     title: {
//         text: 'Temperature in the past 10 seconds',
//         textStyle: {
//             fontSize: '15',
//         },
//     },
//     color: [
//         '#358ccb',
//         '#2f4554',
//         '#61a0a8',
//         '#d48265',
//         '#91c7ae',
//         '#749f83',
//         '#ca8622',
//         '#bda29a',
//         '#6e7074',
//         '#546570',
//         '#c4ccd3'
//     ],
//
//     tooltip: {},
//     legend: {
//         data: ['sensor 1'],
//         orient: 'vertical',
//         x: 'right',
//         y: 'top',
//         padding: 0,
//         itemGap: 0,
//         textStyle: {
//             fontSize: '15',
//         },
//     },
//     xAxis: {
//         data: ['-9s', '-8s', '-7s', '-6s', '-5s', '-4s', '-3s', '-2s', '-1s', 'now']
//     },
//     yAxis: {},
//     series: [
//         {
//             name: 'sensor 1',
//             type: 'line',
//             data: [5, 20, 36, 10, 10, 20, 12, 13, 13, 10]
//         }
//     ]
// };
//
// // Display the chart using the configuration items and data just specified.
// myChart.setOption(option);





temperatureSocket.onmessage = function (e) {
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    $('#chart_temperature').text = djangoData.data;

    // var newChartData = option.series[0].data;
    // newChartData.shift();
    // newChartData.push(djangoData.value);
    //
    // option.series[0].data = newChartData;
    //
    // myChart.setOption(option);

    document.querySelector('#chart_temperature').innerText = djangoData.value;


    // var newCurrentTemperature = option_current_temperature.series[0].data;
    // newCurrentTemperature = [{value: djangoData.value}];
    //
    // option_current_temperature.series[0].data = newCurrentTemperature;
    //
    // myChart_current_temperature.setOption(option_current_temperature);


}

temperatureSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};