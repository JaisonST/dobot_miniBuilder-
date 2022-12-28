const express = require('express')
const app = express()
const path = require('path');
const {spawn} = require('child_process'); 
const port = 3000
var bodyParser = require('body-parser')
app.use(express.static(path.join(__dirname, 'public')));

// parse application/x-www-form-urlencoded
// app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(express.json())

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname+'/Interface/index.html'));
})

app.post('/call_script', (req, res)=> {
  // Code to call script.
  console.log(req.body.input);
    const py = spawn('python3', ['./dobot_execute.py', JSON.stringify(req.body.input)]);
    // Return prediction on completion of python code
    py.stdout.on('data', (data) => {
	console.log(data.toString());
    });

   py.stderr.on('data', (data) => {
	console.log(data.toString());
   });
    py.on('close', (code) => {
        console.log(`Exited with code: ${code}`);
        if(code > 0){
            console.log("Something went wrong", code);
        }
        else{
            console.log("Done!");
        }
        res.end(JSON.stringify({ "status": 1 }));
    }); 
}); 

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
