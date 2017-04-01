from flask import Flask, render_template, redirect, url_for, request
from pprint import pprint
import json
from forms import AlgorithmForm

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def home_page():
    form = AlgorithmForm(secret_key='myverylongsecretkey')
    if form.validate_on_submit():

        # default values for algorithm
        args = json.dumps({"iterationsLimit":1000,
                           "employedBees":30,
                           "onlookerBees":60,
                           "scoutBees":3})

        print("Form is okay")
        return redirect(url_for('/sudoku', args=args))
    return render_template('index.html', form=form)

@app.route('/sudoku')
def sudoku():
    args = json.loads(request.args['args'])

    # fetch request params
    it = int(args.get('iterationsLimit'))
    eb = int(args.get('employedBees'))
    ob = int(args.get('onlookerBees'))
    sb = int(args.get('scoutBees'))

    # parse uploaded grid
    grid = json.loads(args.get('grid'))

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

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run()