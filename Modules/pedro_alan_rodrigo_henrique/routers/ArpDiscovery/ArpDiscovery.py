import threading
import sys
from typing import List
from ping3 import ping
import ipaddress
from Modules.pedro_alan_rodrigo_henrique.routers.ArpDiscovery.get_manufacturer import (
    load_oui_database,
    get_mac_manufacturer,
)
from Modules.pedro_alan_rodrigo_henrique.routers.ArpDiscovery.get_device_info import (
    get_device_info,
)


class ArpDiscovery:
    __network = None
    __devices_discovered = []
    finished = False

    def __init__(self, network: str):
        self.__stop_arp = threading.Event()
        self.__network = network
        self.__arp_thread = None
        self.__mac_vendors = load_oui_database()

    def start(self):
        self.__devices_discovered = []
        if self.__arp_thread is None or not self.__arp_thread.is_alive():
            self.__arp_thread = threading.Thread(target=self.__start_arp)
            self.__arp_thread.start()
        else:
            print("ARP thread is already running.")

    def stop(self):
        self.__stop_arp.set()
        if self.__arp_thread is not None and self.__arp_thread.is_alive():
            self.__arp_thread.join()

    def get_all_ips_in_network(self):
        try:
            network = ipaddress.IPv4Network(self.__network, strict=False)
            ip_list = [str(ip) for ip in network.hosts()]
            return ip_list
        except ValueError as e:
            return str(e)

    def ping_and_print_info(self, ip, timeout, devices: list):
        response = ping(ip, timeout)
        if response is not None and response is not False:
            device_info = get_device_info(ip)
            if device_info is not None:
                new_device = Device(
                    ip,
                    device_info["mac"],
                    get_mac_manufacturer(device_info["mac"], self.__mac_vendors),
                    "on",
                )
                print(
                    ip,
                    new_device.macAddress,
                    new_device.vendor,
                    new_device.status,
                )
                devices.append(new_device)
            else:
                new_device = Device(ip, "-", "-", "off")
                print(
                    new_device.ipAddress,
                    new_device.macAddress,
                    new_device.vendor,
                    new_device.status,
                )
        else:
            new_device = Device(ip, "-", "-", "off")
            print(
                new_device.ipAddress,
                new_device.macAddress,
                new_device.vendor,
                new_device.status,
            )

    def __start_arp(self):
        self.finished = False
        timeout = 0.1
        ips_in_network = self.get_all_ips_in_network()
        print(ips_in_network)
        while len(ips_in_network) > 0:
            stopAt = 10
            if len(ips_in_network) < 10:
                stopAt = len(ips_in_network)
            for i in range(stopAt):
                self.ping_and_print_info(
                    ips_in_network[i], timeout, self.__devices_discovered
                )
            ips_in_network = ips_in_network[stopAt:]
        self.finished = True

    def set_network(self, network: str):
        self.__network = network
        self.__devices_discovered = []
        self.finished = False
        print("Network set to: " + self.__network)

    def get_devices(self):
        return self.__devices_discovered


class Device:
    def __init__(self, ipAddress: str, macAddress: str, vendor: str, status: str):
        self.ipAddress = ipAddress
        self.macAddress = macAddress
        self.vendor = vendor
        self.status = status
