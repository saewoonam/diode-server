// const {SerialPort} = require('serialport');
// const { autoDetect } = require('@serialport/bindings-cpp')

const polka = require('polka');
const app = polka();
const diodes = require('./diodes');
var busy = false;
app.get('/', (req, res) => {
      res.end(`Hello there ! ${Date()}`);
  })
app.get('/query/sensors', async(req, res) => {
    if (busy) {
        res.end(JSON.stringify({error: 'busy'}));
    } else {
        busy = true;
        // let stats = await diodes.readDiodes('/dev/ttyACM0');
        let stats = await diodes.readDiodes('/dev/diode');
        res.end(JSON.stringify(stats, null, "   "));
        busy = false;
    }
});


// Default route
app.get("*", (req, res) => {
    res.end("PAGE NOT FOUND");
});

// app.listen(3000)
app.listen(process.env.PORT || 3100, ()=> {
    console.log('polka server opened on ', process.env.POST || 3100)
});

