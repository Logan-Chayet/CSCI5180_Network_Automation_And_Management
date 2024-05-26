from flask import Flask,render_template,request
import getconfig
import ospfconfig

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/get_config")
def get_config():
    result = getconfig.printConfigs()
    return render_template('get_config.html',result=result)

@app.route("/ospf_config", methods=["GET","POST"])
def ospf_config():
    if request.method == "POST":
        ospfconfig.getFormData()
        if ospfconfig.enoughEntry() == 4:
            #print("LETS GO")
            #print(ospfconfig.getValidIP())
            ospfconfig.createTable()
            ospfconfig.ospfConf()
    return render_template('ospf_config.html')

@app.route("/diff_config")
def diff_config():
    return render_template('diff_config.html')
