(function (sudoku) {

    var $form = $('#sudoku-form');

    $form.submit(function (event) {
        event.preventDefault();

        $('.form-error').hide();

        var data = $(this).serializeArray();

        data.push({
            name: 'grid',
            value: JSON.stringify(sudoku.getValues())
        });

        $.post('/', data, function(data, status, xhr) {
            var contentType = xhr.getResponseHeader("content-type") || "";

            if(contentType.indexOf('json') > -1) {
                // If it is a JSON-type response, it is a result of the algorithm.
                var parsed = JSON.parse(data);
                sudoku.fillGrid({
                    state: parsed[0][1]
                });
            } else if(contentType.indexOf('html') > -1) {
                // If it is a HTML-type response, it is a form template rendered with errors visible.
                $form.empty().html(data);
            }
        });
    });

})(sudoku);
