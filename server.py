#!/usr/bin/python3

import dbus

from gatt import Advertisement, Application, Service, Characteristic, Descriptor
from datetime import date
import time

DATE_SVC_UUID = "00000001-abcd-4321-89ab-a1b2c3d4e5f6"
DATE_CHRC_UUID = "00000002-abcd-4321-89ab-a1b2c3d4e5f6"
TIME_CHRC_UUID = "00000003-abcd-4321-89ab-a1b2c3d4e5f6"
NOTIFY_TIMEOUT = 5000

def convert_to_dbus_array(string):
    value = []
    for c in string:
        value.append(dbus.Byte(c.encode()))
    return value

class DateAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Dummy GATT Server")
        self.include_tx_power = True
        self.add_service_uuid(DATE_SVC_UUID)

class DateService(Service):
    def __init__(self, index):
        Service.__init__(self, index, DATE_SVC_UUID, True)
        self.add_characteristic(DateCharacteristic(self))

class DateCharacteristic(Characteristic):
    def __init__(self, service):
        Characteristic.__init__(
            self, DATE_CHRC_UUID,
            ["read"], service
        )
        self.add_descriptor(DateDescriptor(self))
    
    def get_date(self):
        return str(date.today())

    def ReadValue(self, options):
        value = []
        date = self.get_date()
        for c in date:
            value.append(dbus.Byte(c.encode()))

        return value

class DateDescriptor(Descriptor):
    UUID = "2901"
    VALUE = "Today's Date"

    def __init__(self, characteristic):
        Descriptor.__init__(self, self.UUID, ["read"], characteristic)

    def ReadValue(self, options):
        value = []
        for c in self.VALUE:
            value.append(dbus.Byte(c.encode()))
        return value 

class TimeCharacteristic(Characteristic):
    def __init__(self, service):
        Characteristic.__init__(
            self, TIME_CHRC_UUID,
            ["read"], service
        )

    def ReadValue(self, options):
        now = str(time.asctime())
        return convert_to_dbus_array(now)

class TimeDescriptor(Descriptor):
    UUID = "2901"
    VALUE = "Current Time"

    def __init__(self, characteristic):
        Descriptor.__init__(self, self.UUID, ["read"], characteristic)

    def ReadValue(self, options):
        return convert_to_dbus_array(self.VALUE)

app = Application()
app.add_service(DateService(0))
app.register()

adv = DateAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()