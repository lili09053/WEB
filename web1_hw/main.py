import json
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/distribution')
def distribution():
    with open("distribution.json", "r", encoding="utf-8") as f:
        distribution_list = json.load(f)
    return render_template('distribution.html', distribution=distribution_list)


if __name__ == '__main__':
    app.run(port=8084, host='127.0.0.1')
