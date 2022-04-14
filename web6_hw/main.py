from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/reg', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('reg.html')
    elif request.method == 'POST':
        print(request.form['surname'])
        print(request.form['name'])

        print(request.form['email'])

        print(request.form['education'])
        print(request.form.getlist('add[]'))

        print(request.form['sex'])
        print(request.form['description'])

        print(request.form['file'])
        print(request.form['accept'])

        return "Заявка принята"


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')
