# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import csv
from openai import OpenAI


"""
client = OpenAI()

openai.key = ''
response = client.completions.create(
  engine='gpt-3.5-turbo', 
  prompt='', 
  temperature=0.7,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0)
print(response.choices[0].text.strip())

"""


app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/upload', methods=['POST'])
def upload_file():
  if 'csvfile' not in request.files:
    return jsonify({"error": "No file provided"}), 400
  
  file = request.files['csvfile']
  if file.filename == '':
     return jsonify({"error": "Empty file name"}), 400
  
  if file and file.filename.endswith(".csv"):
    file_content = file.read().decode('utf8')
    csv_reader = csv.reader(file_content.splitlines(), delimiter=',', quotechar='|')
    for row in csv_reader:
        print(", ".join(row))
    return



if __name__ == '__main__':
    app.run(debug=True)

def algorithm():
   return NotImplementedError