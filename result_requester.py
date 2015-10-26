from flask import Flask, request

app= Flask(__name__)

@app.route('/result', methods=['POST'])
def result():
    msg = request.form['msg']
    print(msg)
    return 'done'
