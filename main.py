from flask import Flask,redirect,url_for,render_template
import readExcel.temp as res
import readExcel.tempTable as tbl

app = Flask(__name__)


@app.route('/process')
def process():
    data =  res.merged_dict
    tblHeader = tbl.tblHeaders
    phaseList = tbl.phaseList
    groupList = tbl.groupList
    phaseTenure = tbl.phaseTenure
    products = tbl.products

    return render_template("index.html" , data = data, header = tblHeader, Tenure = phaseTenure)

@app.route("/")
def main():
    return "True"

if __name__ == '__main__':
    # app.run()
    app.run(debug= True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
