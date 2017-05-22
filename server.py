import subprocess
import os
from flask import Flask, request, redirect, url_for,flash,Response,send_from_directory,current_app
from werkzeug.utils import secure_filename
from flask import Flask, current_app,send_from_directory
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def download_info():
    if request.method == "POST":
        model = request.get_data()
        model = model.split("=")[1]
        model = model.replace("+"," ")
        with open ("model.txt","w") as m:
            m.write(model)
        spider_name1 = "query_ym"
        subprocess.check_output(['scrapy', 'crawl', spider_name1, "-t", "urls.txt"])

        spider_name2 = "inf"
        subprocess.check_output(['scrapy', 'crawl', spider_name2, "-t", "data_scraped_common.db"])
        with open("primary_key.txt","r")as f:
            pk = int(f.readline()) - 1

        con = sqlite3.connect("data_scraped_common.db")
        curr = con.cursor()
        curr.execute("SELECT width FROM commondata WHERE pk =" + str(pk))
        width = curr.fetchone()[0].split(" ")[0]
        curr.execute("SELECT height FROM commondata WHERE pk =" + str(pk))
        height = curr.fetchone()[0].split(" ")[0]
        curr.execute("SELECT deep FROM commondata WHERE pk =" + str(pk))
        deep = curr.fetchone()[0].split(" ")[0]
        curr.execute("SELECT weight FROM commondata WHERE pk =" + str(pk))
        weight = curr.fetchone()[0].split(" ")[0]
        curr.execute("SELECT link_mfr FROM commondata WHERE pk =" + str(pk))
        link_mfr = curr.fetchone()[0]
        curr.execute("SELECT url FROM commondata WHERE pk =" + str(pk))
        url = curr.fetchone()[0]
        curr.execute("SELECT img FROM commondata WHERE pk =" + str(pk))
        img = curr.fetchone()[0]
        curr.close()
        return str(img)+"\n"+str(width) + "\n"+str(height)+"\n"+str(deep)+"\n"+str(weight)+"\n"+str(url)+"\n"+str(link_mfr)

def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == '__main__':
    app.run(host='192.168.0.104',debug=True)