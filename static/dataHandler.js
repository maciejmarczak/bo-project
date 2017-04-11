(function (sudoku) {

    var $form = $('#sudoku-form');
    var $chart = $('#chart');

    $form.submit(function (event) {
        event.preventDefault();

        $form.hide();
        $chart.show();

        sudoku.markUserInput();

        var data = $(this).find('input')
            .serializeArray();

        data.push({
            name: 'grid',
            value: JSON.stringify(sudoku.getValues())
        });

        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/sudoku?' + $.param(data));
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send();

        var position = 0;
        var result;
        function handleNewResponse() {
            var response = xhr.responseText.split('\n');
            response.slice(position).forEach(function (value) {
                if (value !== '') {
                    var parsed = JSON.parse(value);
                    dataChart.data.datasets[0].data.push({ x: parsed[1], y: parsed[0][0] });
                    dataChart.update();
                    result = parsed;
                }
            });
            position = response.length - 1;
        }

        var timer;
        timer = setInterval(function () {
            handleNewResponse();
            if (xhr.readyState == XMLHttpRequest.DONE) {
                clearInterval(timer);
                sudoku.fillGrid({ state: result[0][1] }, true);
                $('#res').html('Finished in ' + result[1] + ' iterations. ' +
                    'It took ' + result[2].toFixed(2) + ' seconds.');
            }
        }, 500);
    });

    var dataChart = new Chart("chart", {
        type: 'line',
        data: {
            datasets: [{
                label: 'Fitness per Iteration',
                data: []
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'linear',
                    position: 'bottom'
                }]
            }
        }
    });

})(sudoku);