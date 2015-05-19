var sleep = require('sleep');
var noble = require('noble');

var myServiceUuid = 'ff00';
var battCharacteristicUuid = 'ff02';
var moveCharacteristicUuid = 'ff01';

var args = process.argv.slice(2);
var targetAddr = args[0]
var num = args[1]

console.log(targetAddr);
console.log(num);

var battCharacteristic = null;
var moveCharacteristic = null;
var device = null;


noble.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    console.log('scanning...');
    noble.startScanning([myServiceUuid], true);
  }
  else {
    noble.stopScanning();
  }
})

noble.on('discover', function(peripheral) {
        console.log('found peripheral:', peripheral.advertisement);
        console.log('found peripheral:', peripheral.address);
        if(peripheral.address == targetAddr){
        noble.stopScanning();
        peripheral.connect(function(err) {
	    device = peripheral;
            peripheral.discoverServices([myServiceUuid], function(err, services) {
                services.forEach(function(service) {
                    console.log('found service:', service.uuid);
                    service.discoverCharacteristics([], function(err, characteristics) {
                        characteristics.forEach(function(characteristic) {
                            console.log('found characteristic:', characteristic.uuid);

                            if (battCharacteristicUuid == characteristic.uuid) {
                                battCharacteristic = characteristic;
                                handleBatt();
                            }
                            else if (moveCharacteristicUuid == characteristic.uuid) {
                                moveCharacteristic = characteristic;
                                handleMove();
                            }
                        })
                    })
                })
            })
        })
        }

        peripheral.on('disconnect', function() {
            console.log('disconnected!');
            //sleep.sleep(3)
            noble.startScanning([myServiceUuid], true);
            //process.exit(0);
        });
})


function handleMove() {
    console.log('move called');
    moveCharacteristic.notify(true);
    //moveCharacteristic.read();
    moveCharacteristic.on('data', function(data, isNotification){
        if(isNotification){
            console.log('get notify movement data:', data);
            moveCharacteristic.notify(true);
        }
        else{
            console.log('get read movement data:', data);
        }

	sendObservation("treemonitor".concat(num),data.readUInt8(0),new Date().getTime());
	});
}

function handleBatt() {
    console.log('batt called')
    battCharacteristic.notify(true);
    //battCharacteristic.read();
    battCharacteristic.on('data', function(data, isNotification){
        if(isNotification){
            console.log('get notify battery data:', data);
            battCharacteristic.notify(true);
        }
        else{
            console.log('get read battery data:', data);
        }

        sendObservation("treemonitorbattery".concat(num),data.readUInt8(0),new Date().getTime());
	});

}


var dgram = require('dgram');
var client = dgram.createSocket('udp4');

// UDP Options
var options = {
    host : '127.0.0.1',
    port : 41234
};

function sendObservation(name, value, on){
    var msg = JSON.stringify({
        n: name,
        v: value,
        on: on
    });

    var sentMsg = new Buffer(msg);
    console.log("Sending observation: " + sentMsg);
    client.send(sentMsg, 0, sentMsg.length, options.port, options.host);
};




 
