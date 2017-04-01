(function (sudoku) {

    var $form = $('#sudoku-form');

    $form.submit(function (event) {
        event.preventDefault();

        var data = $(this).find('input')
            .serializeArray();

        data.push({
            name: 'grid',
            value: JSON.stringify(sudoku.getValues())
        });

        $.get('/sudoku', data, function (data) {
            var parsed = JSON.parse(data);
            sudoku.fillGrid({
                state: parsed[0][1]
            });
        });
    });

})(sudoku);