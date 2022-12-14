const express = require('express')
const app = express()
const path = require('path');
const {spawn} = require('child_process'); 
const port = 3000

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname+'/index.html'));
})


app.post('/call_script', (req,res)=> {
    // Code to call script.
    const py = spawn('python', ['./dobot_execute.py']);
    // Return prediction on completion of python code 
    py.on('close', (code) => {
        console.log(`Exited with code: ${code}`);
        if(code > 0){
            console.log("Something went wrong");
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