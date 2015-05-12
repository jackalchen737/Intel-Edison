//usb bomb control
var usb = require('usb'),
    term = usb.findByIds(0x1941, 0x8021);

//make sure device exist
if (term == undefined){
     console.log("no such device of vid,pid = 0x1941, 0x8021");
    return;
}

//open device
term.open();
if(term.interfaces[0].isKernelDriverActive())
    term.interfaces[0].detachKernelDriver();

var C_UP = new Buffer([0x01,0,0,0,0,0,0,0]),
    C_DOWN = new Buffer ([0x02,0,0,0,0,0,0,0]),
    C_LEFT = new Buffer ([0x04,0,0,0,0,0,0,0]),
    C_RIGHT = new Buffer ([0x08,0,0,0,0,0,0,0]),
    C_FIRE = new Buffer ([0x10,0,0,0,0,0,0,0]),
    C_NONE = new Buffer ([0,0,0,0,0,0,0,0]);

function sleep(ms) {
    var unixtime_ms = new Date().getTime();
    while(new Date().getTime() < unixtime_ms + ms) {}
}

function ctrlMsgCB(err, data){
    if(err)
        console.log('send ctrl transfer error');
}


var util = require('util'),
  os = require('os'),
  exec = require('child_process').exec,
  bleno = require('bleno'),
  Descriptor = bleno.Descriptor,
  Characteristic = bleno.Characteristic;

var BombCtrlCharacteristic = function() {
  BombCtrlCharacteristic.super_.call(this, {
      uuid: 'AAA1',
      properties: ['write'],
      descriptors: [
        new Descriptor({
            uuid: '2901',
            value: 'Bomb Control'
        })
      ]
  });
};

util.inherits(BombCtrlCharacteristic, Characteristic);


BombCtrlCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
  if (offset) {
    callback(this.RESULT_ATTR_NOT_LONG);
  } else if (data.length !== 1) {
    callback(this.RESULT_INVALID_ATTRIBUTE_LENGTH);
  } else {
    var ctrl = data.readUInt8(0);
    if (ctrl == 0x01){
        console.log("0x01 get: left");
        term.controlTransfer(0x21,0x09,0,0,C_LEFT,ctrlMsgCB);
        sleep(1000);
        term.controlTransfer(0x21,0x09,0,0,C_NONE,ctrlMsgCB);
    }
    else if (ctrl == 0x02){
        console.log("0x02 get: right");
        term.controlTransfer(0x21,0x09,0,0,C_RIGHT,ctrlMsgCB);
        sleep(1000);
        term.controlTransfer(0x21,0x09,0,0,C_NONE,ctrlMsgCB);
    }   
    else if (ctrl == 0x03){
        console.log("0x03 get: up");
        term.controlTransfer(0x21,0x09,0,0,C_UP,ctrlMsgCB);
        sleep(1000);
        term.controlTransfer(0x21,0x09,0,0,C_NONE,ctrlMsgCB);
    }
    else if (ctrl == 0x04){
        console.log("0x04 get: down");
        term.controlTransfer(0x21,0x09,0,0,C_DOWN,ctrlMsgCB);
        sleep(1000);
        term.controlTransfer(0x21,0x09,0,0,C_NONE,ctrlMsgCB);
    }
    else if (ctrl == 0x05){
        console.log("0x05 get: fire");
        term.controlTransfer(0x21,0x09,0,0,C_FIRE,ctrlMsgCB);
        sleep(5000);
        term.controlTransfer(0x21,0x09,0,0,C_NONE,ctrlMsgCB);
        console.log("fire");
    }

    callback(this.RESULT_SUCCESS);
  }
};

module.exports = BombCtrlCharacteristic;
