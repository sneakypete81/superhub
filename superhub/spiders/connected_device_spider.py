import scrapy
from scrapy import log

from superhub.items import ConnectedDeviceItem

class ConnectedDeviceSpider(scrapy.Spider):
    name = "connected_device"

    def __init__(self, ip_address, password):
        self.ip_address = ip_address
        self.password = password
        self.allowed_domains = [ip_address]

    def start_requests(self):
        return [scrapy.Request("http://"+self.ip_address+"/VmLogin.html",
                              callback=self.parse_login),
                ]

    def parse_login(self, response):
        # Extract the name of the password field
        name = response.xpath("//form/div/input/@name").extract()[0]
        return scrapy.FormRequest.from_response(
            response,
            formdata={name: self.password},
            callback=self.parse_login_response)

    def parse_login_response(self, response):
        # Check if login was successful
        if "var res=\"0\";" in response.body:
            return [scrapy.Request("http://"+self.ip_address+"/home.html",
                    callback=self.parse_home_response),
                    ]
        else:
            self.log("Login failed", level=log.ERROR)

    def parse_home_response(self, response):
        return [scrapy.Request("http://"+self.ip_address+"/device_connection_status.html",
                callback=self.parse_device_connection_status),
                ]

    def parse_device_connection_status(self, response):
        log.msg(response.body, log.DEBUG)
        for script_text in response.xpath("//script"):
            for item in parse_devices(script_text.re("WiredDevicesList = (.*)"),
                                      is_wired=True):
                yield item
            for item in parse_devices(script_text.re("WifiDevicesList = (.*)"),
                                      is_wired=False):
                yield item

def parse_devices(device_text, is_wired):
    if device_text == []:
        return

    device_text = device_text[0].strip(";").strip("'")
    if device_text == "":
        return

    for device in device_text.split("|,|"):
        fields = device.split("}-{")
        yield ConnectedDeviceItem(mac_address=fields[0],
                                  ip_address=fields[1],
                                  device_name=fields[2],
                                  time_connected=fields[3],
                                  is_wired=is_wired)
