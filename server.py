#!/usr/bin/python3

import dbus

from advertisement import Advertisement
from gatt import Application, Service, Characteristic
from datetime import date

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
DATE_SVC_UUID = "00000001-abcd-4321-89ab-a1b2c3d4e5f6"
DATE_CHRC_UUID = "00000002-abcd-4321-89ab-a1b2c3d4e5f6"
NOTIFY_TIMEOUT = 5000

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
    
    def get_date(self):
        return str(date.today())

    def ReadValue(self, options):
        value = []
        date = self.get_date()
        for c in date:
            value.append(dbus.Byte(c.encode()))

        return value

app = Application()
app.add_service(DateService(0))
app.register()

adv = DateAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()