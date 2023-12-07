from flask import Flask, render_template, request
from tbl_details import DataProcessor

app = Flask(__name__)

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        file_path = "readExcel/template.xlsx"
        data_processor = DataProcessor(file_path)
        data_processor.process_data()

        data = data_processor.merged_dict
        tbl_header = data_processor.products
        phase_list = list(data_processor.group_list.keys())
        phase_tenure = data_processor.phase_tenure

        return render_template("Process.html", data=data, header=tbl_header, tenure=phase_tenure)
    else:
        return render_template("badReq.html")

@app.route("/")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
