import os
import os.path
import sys
import time
import string
import usb
import array
import serial


class DeviceDescriptor(object) :
    def __init__(self, vendor_id, product_id, interface_id) :
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.interface_id = interface_id

    def getDevice(self) :
        """
        Return the device corresponding to the device descriptor if it is
        available on a USB bus.  Otherwise, return None.  Note that the
        returned device has yet to be claimed or opened.
        """
        buses = usb.busses()
        for bus in buses :
            for device in bus.devices :
                #print "%0X" % device.idVendor
                #print "%0X" % device.idProduct
                if device.idVendor == self.vendor_id :
                    if device.idProduct == self.product_id :
                        return device
        return None

class PlugUSBDevice(object) :

    PLUG_VENDOR_ID = 0x1941
    PLUG_PRODUCT_ID = 0x8021
    PLUG_INTERFACE_ID = 0
    #PLUG_BULK_IN_EP = 0x81
    #PLUG_BULK_OUT_EP = 0x01


    C_UP = (0x01,0,0,0,0,0,0,0)
    C_DOWN = (0x02,0,0,0,0,0,0,0)
    C_LEFT = (0x04,0,0,0,0,0,0,0)
    C_RIGHT = (0x08,0,0,0,0,0,0,0)
    C_FIRE = (0x10,0,0,0,0,0,0,0)
    C_NONE = (0,0,0,0,0,0,0,0)

    def __init__(self) :
        self.device_descriptor = DeviceDescriptor(PlugUSBDevice.PLUG_VENDOR_ID,
                                                  PlugUSBDevice.PLUG_PRODUCT_ID,
                                                  PlugUSBDevice.PLUG_INTERFACE_ID)
        self.device = self.device_descriptor.getDevice()
        self.handle = None

    def open(self) :
        self.device = self.device_descriptor.getDevice()
        self.handle = self.device.open()
        if os.name != "posix" :
            self.handle.setConfiguration(1)
        else :
            self.handle.reset()

        try :
            self.handle.detachKernelDriver(0)
        except:
            print "exception"

        self.handle.claimInterface(self.device_descriptor.interface_id)

    def close(self) :
        self.handle.releaseInterface()

    def up(self):
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_UP,0x0200,0x00)
        time.sleep(1)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)

    def down(self):
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_DOWN,0x0200,0x00)
        time.sleep(1)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)

    def right(self):
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_RIGHT,0x0200,0x00)
        time.sleep(1)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
    def left(self):
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_LEFT,0x0200,0x00)
        time.sleep(1)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
    def fire(self):
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_FIRE,0x0200,0x00)
        time.sleep(3)
        self.handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)

def init_serial():
    luart = serial.Serial()
    luart.port = "COM1"
    luart.baudrate = 19200
    luart.timeout = None
    luart.open()
    return luart



if __name__ == "__main__" :
    ausb = PlugUSBDevice()
    ausb.open()

    uart = init_serial()
    count = 0

    while 1:

        uart.timeout = None
        action1 = uart.read()
        action2 = uart.read()
        action3 = uart.read()
        action4 = uart.read()
        action5 = uart.read()
        action6 = uart.read()


        #if action1 != "" :
        action1 = ord(action1)
        action2 = ord(action2)
        action3 = ord(action3)
        action4 = ord(action4)
        action5 = ord(action5)
        action6 = ord(action6)

        if action1 == 3 and action3 == 3 and action5 == 3  :
            ausb.right()
            uart.flushInput()
            count = 0

        elif action1 == 4 and action3 == 4 and action5 == 4 :
            ausb.left()
            uart.flushInput()
            count = 0

        elif action1 == 1 and action3 == 1 and action5 == 1  :
            ausb.up()
            uart.flushInput()
            count = 0

        elif action1 == 2 and action3 == 2 and action5 == 2  :
            ausb.down()
            uart.flushInput()
            count = 0

        elif action1 == 5 and action3 == 5 and action5 == 5 :
            ausb.fire()
            uart.flushInput()
            count = 0

        else:
            pass

        count = count+1
        #print count

"""
    while True:
        str = raw_input("BOMB:$ ")

        if str == "w":
            ausb.up()
        elif str == "d":
            ausb.right()
        elif str == "a":
            ausb.left()
        elif str == "s":
            ausb.down()
        elif str == "p":
            ausb.fire()
        elif str == "q":
            ausb.close()
            sys.exit()
"""