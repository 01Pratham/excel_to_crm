from flask import Flask,redirect,url_for,render_template,request
import readExcel.temp as res
import readExcel.tempTable as tbl

app = Flask(__name__)


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        data =  res.merged_dict
        tblHeader = tbl.tblHeaders
        phaseList = tbl.phaseList
        groupList = tbl.groupList
        phaseTenure = tbl.phaseTenure
        products = tbl.products

        return render_template("Process.html" , data = data, header = tblHeader, Tenure = phaseTenure)
    else : 
        return render_template("badReq.html")


@app.route("/")
def main():
    return render_template("index.html")

if __name__ == '__main__':
    # app.run()
    app.run(debug= True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
