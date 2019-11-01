from flask import Flask,render_template
import glob
import os
import json
app = Flask(__name__)
#app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
fd = os.path.join(dir_path,"results")

def get_files():
    lst_files =[]
    folder =fd+"\\*.log"
    files = glob.glob(folder)
    for file in files:
        lst_files.append(os.path.splitext(os.path.basename(file))[0])
    return lst_files

def get_folders():
    lst_files =[]
    files = os.listdir(fd)
    return files

@app.route('/')
def index():
    lst_files =get_files()
    content = "please write chosse from the menu on the left side"
    return render_template("index.html",lst_files=lst_files,content=content)

@app.route('/<plug>')
def plugin(plug):
    lst = []
    lst_files =get_files()
    fle = fd+"\\"+plug+".log"
    with open(fle,"r") as f:
        content = f.read().splitlines()

    for con in content:
        cox = json.loads(con)
        lst.append(cox)
    #print (content)

    return render_template("index.html",lst_files=lst_files,content=lst)
def run_web():
    app.run()
