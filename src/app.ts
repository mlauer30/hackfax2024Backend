import express, { Request, Response } from 'express';
import { createReadStream } from 'fs';
import { createInterface } from 'readline';
import OpenAI from 'openai';
import multer from 'multer';

const app = express();
const PORT = process.env.PORT || 3000;
const openai = new OpenAI();
const upload = multer()

interface Class {
  name: string;
  partners: string[];
  times: { start: string; end: string }[];
}

class Student {
  name: string;
  major: string;
  classes: Class[];

  constructor(name: string, major: string, classes: any[]) {
    this.name = name;
    this.major = major;
    this.classes = classes.map((cls: any) => ({
      name: cls.name,
      partners: cls.partners,
      times: cls.time,
    }));
  }

  toString() {
    let result = `Name: ${this.name}, Major: ${this.major}\n`;
    this.classes.forEach((cls) => {
      const timesStr = cls.times.map((time) => `${time.start}-${time.end}`).join('; ');
      const partnersStr = cls.partners.length ? cls.partners.join(', ') : 'None';
      result += `  Class: ${cls.name}, Partners: ${partnersStr}, Times: ${timesStr}\n`;
    });
    return result;
  }
}

function loadFromFile(filename: string = './src/data.json'): any {
  // Assuming data.json contains the necessary JSON data
  const data = require(filename);
  return data;
}

function jsonToStudents(data: any): Student[] {
  return data.users.map((user: any) => new Student(user.Name, user.Major, user.classes));
}

async function callAI(request: string): Promise<string> {
    try {
      const response = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: request }],
        stream: true,
      });
  
      let responseData = '';
  
      // Listen for data events from the stream
      response.data.on('data', (chunk: any) => {
        responseData += chunk;
      });
  
      // Listen for error events from the stream
      response.data.on('error', (error: any) => {
        console.error('Error receiving data:', error);
      });
  
      // Wait for the stream to end
      await new Promise<void>((resolve, reject) => {
        response.data.on('end', () => {
          resolve();
        });
      });
  
      return responseData;
    } catch (error) {
      console.error('Error calling OpenAI API:', error);
      return "500\n";
    }
  }
  

app.get('/', (req: Request, res: Response) => {
  const data = loadFromFile();
  const students = jsonToStudents(data);
  let htmlContent = "<h1>Student Information</h1>";
  students.forEach((student) => {
    let studentInfo = `<p><strong>Name:</strong> ${student.name}<br><strong>Major:</strong> ${student.major}<br><strong>Classes:</strong><br>`;
    student.classes.forEach((cls) => {
      const timesStr = cls.times.map((time) => `${time.start}-${time.end}`).join('; ');
      const partnersStr = cls.partners.length ? cls.partners.join(', ') : 'None';
      studentInfo += ` - ${cls.name} with partners ${partnersStr} at times ${timesStr}<br>`;
    });
    studentInfo += "</p>";
    htmlContent += studentInfo;
  });
  res.send(htmlContent);
});

app.post('/upload', upload.single('csvfile'), (req: Request<any, any, any, multer.MulterFile>, res: Response) => {
    const file = req.file;
  if (!file) {
    return res.status(400).json({ error: "No file provided" });
  }
  if (!file.name) {
    return res.status(400).json({ error: "Empty file name" });
  }
  if (file && file.name.endsWith('.csv')) {
    const csvReader = createInterface({ input: createReadStream(file.name) });
    csvReader.on('line', (line) => {
      console.log(line);
    });
    return res.status(200).json({ message: "File processed successfully" });
  } else {
    return res.status(400).json({ error: "Invalid file format" });
  }
});

app.get('/return', async (req: Request, res: Response) => {
  const data = await callAI("Give me a sample json object");
  res.send(data);
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
