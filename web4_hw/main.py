import json
import random

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/member')
def func():
    with open("competitors.json", "r", encoding="utf-8") as f:
        competitors_list = json.load(f)
        k = random.randint(0, (len(competitors_list) - 1))
        haha = ", ".join(sorted(competitors_list[k]["profession"]))
    return render_template('lol.html', members=competitors_list, k=k, haha=haha)


if __name__ == '__main__':
    app.run(port=8084, host='127.0.0.1')