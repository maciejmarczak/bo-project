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

  function fillGrid(data, validate) {
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

    if (validate) {
      validateGrid();
    }
  }

  function validateGrid() {

    var i, j, k, l;

    for (i = 0; i < 9; i++) {
      for (j = 0; j < 8; j++) {
        for (k = j + 1; k < 9; k++) {

          if (table[i][j].html() === table[i][k].html()) {
            table[i][j].addClass('err');
            table[i][k].addClass('err');
          }

          if (table[j][i].html() === table[k][i].html()) {
            table[j][i].addClass('err');
            table[k][i].addClass('err');
          }

        }
      }
    }

    for (i = 0; i < 9; i += 3) {
      for (j = 0; j < 9; j += 3) {

        for (k = 0; k < 8; k++) {
          for (l = k + 1; l < 9; l++) {

            var x1 = i + Math.floor(k / 3),
                y1 = j + k % 3,
                x2 = i + Math.floor(l / 3),
                y2 = j + l % 3;

            if (table[x1][y1].html() === table[x2][y2].html()) {
              table[x1][y1].addClass('err');
              table[x2][y2].addClass('err');
            }

          }
        }

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

  function markUserInput() {
    var i, j;
    for (i = 0; i < 9; i++) {
      for (j = 0; j < 9; j++) {
        if (parseInt(table[i][j].html())) {
          table[i][j].addClass('fxd');
        }
      }
    }
  }

  return {
    fillGrid: fillGrid,
    getValues: getValues,
    markUserInput: markUserInput
  }

})(jQuery);
