import csv
import ipaddress


class IpToCountry:
    def __init__(self, csv_file):
        self.ip_ranges = []
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                start_ip = ipaddress.IPv4Address(row[0])
                end_ip = ipaddress.IPv4Address(row[1])
                country_name = row[2]
                self.ip_ranges.append((start_ip, end_ip, country_name))
        self.ip_ranges.sort(key=lambda x: x[0])

    def get_country(self, ip_address):
        ip = ipaddress.IPv4Address(ip_address)
        left, right = 0, len(self.ip_ranges) - 1
        while left <= right:
            mid = (left + right) // 2
            start_ip, end_ip, country_name = self.ip_ranges[mid]
            if start_ip <= ip <= end_ip:
                return country_name
            elif ip < start_ip:
                right = mid - 1
            else:
                left = mid + 1
        return "Unknown"
