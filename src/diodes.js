const {autoDetect} = require('@serialport/bindings-cpp')
// import {autoDetect} from '@serialport/bindings-cpp'
// const fs = require('fs')

const Bindings = autoDetect()

async function main(port_path) {
    // await Bindings.list().then(res=>console.log(res))
    // console.log('readDiodes/main');
    // query = new Buffer.from('getT?\r\n', 'utf8')    // console.log(query)
    query = new Buffer.from('V? 0\r\n', 'utf8')    // console.log(query)
    // console.log(query.length);
    response = new Buffer.alloc(255);
    let port = await Bindings.open({path:port_path, baudRate:9600, lock:false});
    // console.log('isOpen', port.isOpen)
    await port.write(query)
    // console.log('finished writing query');
    var len = 0
    var result
    do {  // read until we get \r\n after len>7
        // console.log('try to read');
        result = await port.read(response, len, 255-len)
        len += result.bytesRead
        //console.log(JSON.stringify(response.slice(0, len).toString()));
        // console.log(response.slice(0, len).toString().endsWith('\r\n'), len<=query.length);
    } while (!(response.slice(0, len).toString().endsWith('\r\n')) || len<=query.length);
    response = response.slice(0, len).toString()
    // console.log(response)
    response = response.trim().split('\r\n')[0]
    // console.log(response)
    // console.log('replace', response.replaceAll("'", '"'))
    // nor sure why we need to replace the ' with "
    // response = response.replaceAll("'", '"')
    // console.log(response)
    response = JSON.parse(response)
    // console.log(response)
    await port.close();
    return response; 

}
// main('/dev/ttyACM0')
// main('/dev/ttyUSB0')
exports.readDiodes = main;
