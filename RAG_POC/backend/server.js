const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/query', (req, res) => {

        console.log("api called")
  const userInput = req.body.question;

  const python = spawn('python3', ['semantic_rag_query.py', userInput]);

  let output = '';
  python.stdout.on('data', (data) => {
    output += data.toString();
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  python.on('close', (code) => {
    res.send({ result: output });
  });
});

app.listen(8000, () => console.log('🚀 Node server running on http://localhost:8000'));
