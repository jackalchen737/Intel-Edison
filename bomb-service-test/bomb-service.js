var util = require('util'),
  bleno = require('bleno'),
  BlenoPrimaryService = bleno.PrimaryService,
  BombCtrlCharacteristic = require('./bomb-ctrl-characteristic');

function BombService() {
  BombService.super_.call(this, {
      uuid: 'FFF1',
      characteristics: [
          new BombCtrlCharacteristic()
      ]
  });
}

util.inherits(BombService, BlenoPrimaryService);

module.exports = BombService;
