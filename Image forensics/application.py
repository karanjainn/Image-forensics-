from utils.metadata_extraction import extract_the_data
from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)

app.config['UPLOAD_PATH'] = "C:\\Users\\HP\\Desktop\\Image forensics\\uploads"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
    if request.method == "POST":
        for f in request.files.getlist('photo'): 
            # f = request.files['photo']
            f.save(os.path.join(app.config['UPLOAD_PATH'],f.filename))  
        extract_the_data("C:\\Users\\HP\\Desktop\\Image forensics\\uploads")
        data = pd.read_csv("C:\\Users\\HP\\Desktop\\Image forensics\\image_metadata.csv")
        # print(type(df))
        return render_template("test.html",msg="Files Saved Successfully",tables = [data.to_html()],titles = [''])
    else:
        return render_template("test.html")


    # if 'files[]' not in request.files:
    #     return "No file part"

    # files = request.files.getlist('files[]')

    # for file in files:
    #     if file.filename == '':
    #         return "No selected file"
        
    #     # Handle the file as needed (e.g., save it to a folder)
    #     # Here, we are just printing the filenames for demonstration
    #     print("Uploaded file:", file.filename)

    # return "Files uploaded successfully!"

    if __name__ == '__application__':
        app.run(debug=True)
