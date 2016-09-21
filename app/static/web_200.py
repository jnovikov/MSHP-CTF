# --encoding=utf-8--
from random import randrange

from flask import Flask, request, render_template, render_template_string

users = {}

app = Flask(__name__)
flag = "" # Find it


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        who = request.form['who']
        role = request.form['role']
        template = '''<h2> ''' + who + ''' ''' + role + '''</h2>'''

        return render_template_string(template, flag=flag)


if __name__ == '__main__':
    app.threaded = True
    app.processes = 10
    app.run(host='0.0.0.0', port=8080)
