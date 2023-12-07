from flask import Flask, render_template, request
from controller.tblDetails import DataProcessor
import os

app = Flask(__name__)

@app.route('/process', methods=['POST','GET'])
def process():
    if request.method == 'POST':
        # Get the uploaded file from the request
        # return request.form
        uploaded_file = request.files['files']


        if uploaded_file:
            # Save the file to a temporary location or your desired location
            file_path = os.path.join("uploads", "temp_uploaded_file.xlsx")
            uploaded_file.save(file_path)

            # Process the uploaded file using DataProcessor or any other logic
            data_processor = DataProcessor(file_path)
            data_processor.process_data()

            # Process the uploaded file using DataProcessor or any other logic
            data_processor = DataProcessor(file_path)
            data_processor.process_data()

            data = data_processor.merged_dict
            tbl_header = data_processor.products
            phase_list = list(data_processor.group_list.keys())
            phase_tenure = data_processor.phase_tenure

            # You can do something with the processed data, for example, render a template
            return render_template("Process.html", data=data, header=tbl_header, tenure=phase_tenure)
        else:
            return render_template("badReq.html", message="No file uploaded.")
    else:
        return render_template("badReq.html", message="Invalid request.")

@app.route("/")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
    os.makedirs("uploads", exist_ok=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
