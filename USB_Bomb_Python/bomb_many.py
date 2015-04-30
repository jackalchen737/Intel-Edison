import os
import os.path
import sys
import time
import string
import usb
import array


class DeviceDescriptor(object) :
    def __init__(self, vendor_id, product_id, interface_id) :
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.interface_id = interface_id

    def getDevices(self) :
        """
        Return the device corresponding to the device descriptor if it is
        available on a USB bus.  Otherwise, return None.  Note that the
        returned device has yet to be claimed or opened.
        """
        self.devices = []
        buses = usb.busses()
        for bus in buses :
            for device in bus.devices :
                #print str(bus.location) + ":" + str(bus.dirname) + ":" + str(device.filename)
                #print "%0X" % device.idVendor
                #print "%0X" % device.idProduct
                if device.idVendor == self.vendor_id and device.idProduct == self.product_id:
                    self.devices.append(device)

        return self.devices

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
        self.devices = self.device_descriptor.getDevices()
        self.handles = []

    def open(self) :
        if len(self.devices) == 0:
            print "no USB Bomb Now"
            return False

        for dev in self.devices :
            #get handle
            handle = dev.open()
            
            #choose config & reset
            if os.name != 'posix' :
                handle.setConfiguration(1)
            else :
                handle.reset()

            #detatch kernel driver (forlinux)
            try:
                handle.detachKernelDriver(0)
            except:
                pass
                #print "detatch kernel driver exception"

        
            #claim interface and add to list
            handle.claimInterface(self.device_descriptor.interface_id)
            self.handles.append(handle)

        print "open ok"
        print "threr are " + str(len(self.devices)) + " bomb devices" 

    def close(self) :
        for handle in self.handles :
            handle.releaseInterface()
        
        print "close ok"

    def up(self):
        for handle in self.handles :

            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_UP,0x0200,0x00)
        
        time.sleep(1)
        
        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)

    def down(self):
        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_DOWN,0x0200,0x00)
            
        time.sleep(1)

        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)

    def right(self):
        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_RIGHT,0x0200,0x00)
            
        time.sleep(1)

        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
    
    def left(self):
        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_LEFT,0x0200,0x00)
        
        time.sleep(1)

        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
    
    def fire(self):
        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_FIRE,0x0200,0x00)
        
        time.sleep(7)
        
        for handle in self.handles :
            handle.controlMsg(0x21, 0x09, PlugUSBDevice.C_NONE,0x0200,0x00)

if __name__ == "__main__" :
    ausb = PlugUSBDevice()
    if ausb.open() == False:
        sys.exit()

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
