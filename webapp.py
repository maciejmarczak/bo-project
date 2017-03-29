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

    # parse uploaded grid
    grid = json.loads(args.get('grid'))

    # fetch request params
    it = int(args.get('iterationsLimit'))
    eb = int(args.get('employedBees'))
    ob = int(args.get('onlookerBees'))
    sb = int(args.get('scoutBees'))

    from core.abc import forage
    gen = forage(grid, grid, max_iterations=it,
                 employed_bees=eb, onlooker_bees=ob,
                 scout_bees=sb, yield_after=20)

    pprint(gen)

    return json.dumps(gen)


@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(error):
    return redirect(url_for('home_page'), 302)

