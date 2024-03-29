from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import json
import openai

openai.api_key=''


class Student:
    def __init__(self, name, major, classes):
        self.name = name
        self.major = major
        self.classes = []
        for cls in classes:
            class_info = {
                'name': cls['name'],
                'partners': cls['partners'],
                'times': cls['time']
            }
            self.classes.append(class_info)

    def __str__(self):
        result = f"Name: {self.name}, Major: {self.major}\n"
        for cls in self.classes:
            times_str = '; '.join([f"{time['start']}-{time['end']}" for time in cls['times']])
            partners_str = ', '.join(cls['partners']) if cls['partners'] else 'None'
            result += f"  Class: {cls['name']}, Partners: {partners_str}, Times: {times_str}\n"
        return result

def load_data_from_file(filename='./src/data.json'):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def json_to_students(data):
    students = []
    for user in data["users"]:
        student = Student(name=user["Name"], major=user["Major"], classes=user["classes"])
        students.append(student)
    return students

def call_ai(request):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "For all responses, ONLY give me code, do not give me code blocks or any type of response beyond plaintext code."},
                {"role": "user", "content": request}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return "500\n"

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    data = load_data_from_file()
    students_instances = json_to_students(data)
    html_content = "<h1>Student Information</h1>"
    for student in students_instances:
        student_info = f"<p><strong>Name:</strong> {student.name}<br><strong>Major:</strong> {student.major}<br><strong>Classes:</strong><br>"
        for cls in student.classes:
            times_str = '; '.join([f"{time['start']}-{time['end']}" for time in cls['times']])
            partners_str = ', '.join(cls['partners']) if cls['partners'] else 'None'
            student_info += f" - {cls['name']} with partners {partners_str} at times {times_str}<br>"
        student_info += "</p>"
        html_content += student_info
    return html_content


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
        return jsonify({"message": "File processed successfully"}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

@app.route('/return', methods=['GET'])
def return_data_to_frontend():
    data = call_ai("Give me a sample json object")
    return data

if __name__ == '__main__':
    app.run(debug=True)
