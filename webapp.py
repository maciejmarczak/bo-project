from flask import Flask, render_template, redirect, url_for, request
from pprint import pprint
import json

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/sudoku')
def sudoku():
    args = request.args
    print(args.get('grid'))

    # parse uploaded grid
    grid = json.loads(args.get('grid'))

    # fetch request params
    it = int(args.get('iterationsLimit'))
    eb = int(args.get('employedBees'))
    ob = int(args.get('onlookerBees'))
    sb = int(args.get('scoutBees'))

    return app.response_class(generate(grid, grid, it, eb, ob, sb),
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
