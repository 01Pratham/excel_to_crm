from flask import Flask,redirect,url_for,render_template

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def hello():
    return render_template("index2.html")

if __name__ == '__main__':
    app.run()