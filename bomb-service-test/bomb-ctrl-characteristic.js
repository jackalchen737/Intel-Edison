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
    if (ctrl == 0x00){
        console.log("0x00 get: none");
    }
    else if (ctrl = 0x01){
        console.log("0x01 get: left");
    }
    else if (ctrl == 0x02){
        console.log("0x02 get: right");
    }   
    else if (ctrl == 0x03){
        console.log("0x03 get: up");
    }
    else if (ctrl == 0x04){
        console.log("0x04 get: down");
    }
    else if (ctrl == 0x05){
        console.log("0x05 get: fire");
    }

    callback(this.RESULT_SUCCESS);
  }
};

module.exports = BombCtrlCharacteristic;
