from flask import Flask, render_template, request
from controller.tblDetails import DataProcessor
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
                data_processor = DataProcessor(file_path)
                data = data_processor.merged_dicts()
                tbl_header = data_processor.tblHeaders()
                phase_list = data_processor.getPhases()
                phase_tenure = data_processor.phaseTenure()
                # return render_template("Process.html", data=data, header=tbl_header, Tenure=phase_tenure)
                # return render_template("test.html", data=data, header=tbl_header, Tenure=phase_tenure)
                return (data)
            except Exception as e:
                return render_template("IncorrectFile.html")
        else:
            return render_template("badReq.html", message="No file uploaded.")
    else:
        return render_template("badReq.html", message="Invalid request.")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/test_api",  methods=['POST'])
def api():
    return "hi"

if __name__ == '__main__':
    app.run(debug=True)
    os.makedirs("uploads", exist_ok=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)