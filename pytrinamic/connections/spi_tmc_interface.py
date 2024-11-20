################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved.
# This software is proprietary to Analog Devices, Inc. and its licensors.
################################################################################

import logging
import struct
import spidev
from os import listdir

REGISTER_PACKAGE_STRUCTURE = ">BI"
REGISTER_PACKAGE_LENGTH = 5


class RegisterRequest:
    def __init__(self, address, value):
        self.address = address
        self.value = value

    def to_buffer(self):
        return struct.pack(REGISTER_PACKAGE_STRUCTURE, self.address, self.value)

    def __str__(self):
        return "RegisterRequest: [Addr:{:02x}, Value:{}]".format(self.address, self.value)


class RegisterReply:
    def __init__(self, reply_struct):
        self.address = reply_struct[0]
        self.value = reply_struct[1]

    def __str__(self):
        return "RegisterReply:   [Addr:{:02x}, Value:{}]".format(self.address, self.value)

    def value(self):
        return self.value


class SpiIcInterface:
    def __init__(self, bus=1, device=0, datarate=524288, spi_mode=0b01, timeout_s=5, lsbfirst=False):
        if timeout_s == 0:
            timeout_s = None

        self.logger = logging.getLogger("{}.{}".format(self.__class__.__name__, device))

        self.spi_bus = bus
        self.spi_device = device
        self.logger.debug("Opening port (baudrate=%s).", datarate)
        self.spi = spidev.SpiDev()
        self.spi.max_speed_hz = datarate
        self.spi.mode = spi_mode
        self.spi.lsbfirst = lsbfirst

        self.spi.open(self.spi_bus, self.spi_device)

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        """
        Close the connection at the end of a with-statement block.
        """
        del exit_type, value, traceback
        self.close()

    def close(self):
        self.logger.info("Closing port.")
        self.spi.close()

    @staticmethod
    def supports_tmcl():
        return False

    def send(self, address, value):
        # prepare TMCL request
        data = RegisterRequest(address, value)

        # send request, wait, and handle reply
        self.logger.debug("Tx %s", data)
        previous_data = self.spi.xfer(data)
        reply = RegisterReply(struct.unpack(REGISTER_PACKAGE_STRUCTURE, previous_data))
        self.logger.debug("Rx previous %s", reply)

        return reply
    
    def write(self, address, value):
        address = address & 0b10000000
        received = self.send(address, value)

        return received
    def read(self, address, value):
        self.send(address, value)
        received = self.send(address, value)
        return received
    
    @staticmethod
    def list():
        """
            Return a list of available connection ports as a list of strings.

            This function is required for using this interface with the
            connection manager.
        """
        connected = []

        for device in listdir("/dev"):
            if device.startswith("spidev"):
                connected.append("/dev/"+device)

        connected = ["/dev/spidev"]
        return connected

    def __str__(self):
        return "Connection: type={} bus={} device={} baudrate={}".format(type(self).__name__, self.bus, self.baudrate)