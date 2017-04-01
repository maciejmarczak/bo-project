var sudoku = (function ($) {

  var $grid = $('#sudoku');
  var table = [];

  // grid creation
  (function () {
    var i, j;

    for (i = 0; i < 9; i++) {
      var $row = $('<tr></tr>');
      table[i] = [];

      for (j = 0; j < 9; j++) {
        var $cell = $('<td contenteditable="true"></td>');

        table[i][j] = $cell;
        $row.append($cell);
      }

      $grid.append($row);
    }

    $('td[contenteditable="true"]').on('input', function () {
      var el = $(this);
      el.html(el.html().charAt(0));
    });

  })();

  function fillGrid(data) {
    // data should be an object containing:
    // * 2d array, called 'state', representing new grid values to insert
    // * 2d array, called 'meta', with information of whether a value at
    //   state[i][j] is fixed, wrong, or just normal

    var i, j, $cell;

    for (i = 0; i < 9; i++) {
      for (j = 0; j < 9; j++) {
        $cell = table[i][j];

        $cell.html(data.state[i][j]);
        // $cell.addClass(data.meta[i][j]);
      }
    }
  }

  function getValues() {
    var values = [];

    var i, j;
    for (i = 0; i < 9; i++) {
      values[i] = [];
      for (j = 0; j < 9; j++) {
        values[i][j] = parseInt(table[i][j].html());
      }
    }

    return values;
  }

  return {
    fillGrid: fillGrid,
    getValues: getValues
  }

})(jQuery);
