from flask import Flask, render_template, request
from controller.exportExcel import exportExcel
import os

app = Flask(__name__)

@app.route('/process', methods=['POST','GET'])
def process():
    if request.method == 'POST':
        uploaded_file = request.files['files']
        if uploaded_file:
            file_path = os.path.join("uploads", "temp_uploaded_file.xlsx")
            uploaded_file.save(file_path)
            try : 
                exportExcel(file_path)
                return render_template("Process.html")
            except Exception as e:
                return render_template("IncorrectFile.html")
        else:
            return render_template("badReq.html", message="No file uploaded.")
    else:
        return render_template("badReq.html", message="Invalid request.")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/rem",  methods=['GET'])
def rem():
    file = os.path.join("static", "output", "output.xlsx")
    os.remove(file)
    return "<script> window.location.href = '/' </script>"

if __name__ == '__main__':
    app.run(debug=True)
    os.makedirs("uploads", exist_ok=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)