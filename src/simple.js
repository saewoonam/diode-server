// const {SerialPort} = require('serialport');
// const { autoDetect } = require('@serialport/bindings-cpp')

const polka = require('polka');
const app = polka();
const diodes = require('./diodes');

app.get('/', (req, res) => {
      res.end('Hello there !');
  })
app.get('/query/sensors', async(req, res) => {
    let stats = await diodes.readDiodes('/dev/ttyACM0');
    res.end(JSON.stringify(stats, null, "   "));
});


// Default route
app.get("*", (req, res) => {
    res.end("PAGE NOT FOUND");
});

// app.listen(3000)
app.listen(process.env.PORT || 3100, ()=> {
    console.log('polka server opened on ', process.env.POST || 3100)
});

