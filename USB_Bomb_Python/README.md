python to control usb bomb device

Install dependencies

    sudo apt-get install python libusb-1.0-0-dev
    git clone https://github.com/walac/pyusb
    cd pyusb && sudo python setup.py install

Run the example

    python bomb_keyboard_control.py
