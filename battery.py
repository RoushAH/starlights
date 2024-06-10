from machine import ADC, Pin

class batteryPack():
    def __init__(self):

        self.vsys = ADC(29)                      # reads the system input voltage
        self.chargingcharging = Pin(24, Pin.IN)          # reading GP24 tells us whether or not USB power is connected
        self.conversion_factor = 3 * 3.3 / 65535

        self.full_battery = 4.2                  # these are our reference voltages for a full/empty battery, in volts
        self.empty_battery = 3

    def read_battery(self):
        voltage = self.vsys.read_u16() * self.conversion_factor
        percentage = ((voltage - self.empty_battery) / (self.full_battery - self.empty_battery)) * 100
        return min(percentage, 100)

    def view_battery(self):
        percent = self.read_battery()
        percent //= 20
        if percent < 0:
            percent = 0
        if percent > 4:
            percent = 4
        if percent == 0:
            return '<i class="fa fa-battery-0 flash" style="color:red"></i>'
        return f'<i class="fa fa-battery-{percent}"></i>'