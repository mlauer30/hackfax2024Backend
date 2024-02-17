# -*- coding: utf-8 -*-
from flask import Flask
import openai
openai.key = ''

response = openai.Completion.create(
  engine="gpt-3.5-turbo", # Specify the model
  prompt="", # Your prompt
  temperature=0.7,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
print(response.choices[0].text.strip())


app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

if __name__ == '__main__':
    app.run(debug=True)
