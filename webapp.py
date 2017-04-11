from flask import jsonify

from flask import Flask, render_template, redirect, url_for, request
import json
from forms import AlgorithmForm

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def home_page():
    form = AlgorithmForm(secret_key='myverylongsecretkey')
    if request.method == "GET":
        return render_template('index.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            print("Form is valid")
            return jsonify(json.dumps({'success':True}), 200, {'ContentType':'application/json'})
        # If form is invalid, render form template with errors visible.
        return render_template('form.html', form=form)


@app.route('/sudoku')
def sudoku():
    args = request.args
    print(args.get('grid'))

    # parse uploaded grid
    grid = json.loads(args.get('grid'))
    start_squares = {(i, j) for i in range(9) for j in range(9) if grid[i][j]}

    # fetch request params
    it = int(args.get('iterations_limit'))
    eb = int(args.get('employeed_bees'))
    ob = int(args.get('onlooker_bees'))
    sb = int(args.get('scout_bees'))

    return app.response_class(generate(grid, start_squares, it, eb, ob, sb),
                              mimetype="text/plain")


@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(error):
    return redirect(url_for('home_page'), 302)


def generate(board, squares, it_num, eb, ob, sb):
    from core.abc import forage
    from time import perf_counter

    gen = forage(board, squares, max_iterations=it_num,
                 employed_bees=eb, onlooker_bees=ob,
                 scout_bees=sb, yield_after=100)

    start = perf_counter()
    run = True
    while run:
        try:
            sol, iteration = next(gen)
        except StopIteration as ex:
            sol, iteration = ex.value
            run = False
        finally:
            end = perf_counter()
            yield json.dumps((sol, iteration, end - start)) + '\n'


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run()