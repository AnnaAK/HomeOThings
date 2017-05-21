import subprocess
import os

from flask import Flask, current_app,send_from_directory
app = Flask(__name__)

@app.route('/')
def download_info():

    spider_name1 = "query_ym"
    subprocess.check_output(['scrapy', 'crawl', spider_name1, "-t", "urls.txt"])

    spider_name2 = "inf"
    subprocess.check_output(['scrapy', 'crawl', spider_name2, "-t", "data_scraped_common.db"])
    return "New item added to data base succesfuly!"

@app.route('/images/full', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)