from scapy.all import *
import threading

DNS_QUERY_CODE = 0
DNS_RESPONSE_CODE = 1


class UdpDns:
    def __init__(self):
        self.__stop_sniffing = threading.Event()
        self.__dns_queries = {}

    def __start_sniffing(self):
        filter_expression = "udp and port 53"
        while not self.__stop_sniffing.is_set():
            sniff(
                prn=self.__parse_packet,
                filter=filter_expression,
                count=1,
                timeout=1,
            )

    def __parse_packet(self, pkt):
        if DNS in pkt:
            dns = pkt[DNS]
            if dns.qr == DNS_QUERY_CODE:
                query_id = dns.id
                query_name = dns.qd.qname.decode()
                self.__upsert_dns_query(query_name, query_id)
                print(f"DNS Query: {query_name} (ID: {query_id})")
            elif dns.qr == DNS_RESPONSE_CODE:
                query_id = dns.id
                resolved_ips = []
                if dns.an != None:
                    resolved_ips = [
                        answer.rdata for answer in dns.an if answer.type == 1
                    ]
                self.__upsert_dns_response(query_id, resolved_ips)
                print(
                    f"DNS Response for Query (ID: {query_id}) - Resolved IPs: {resolved_ips}"
                )

    def __upsert_dns_query(self, query_name: str, query_id: str):
        value = self.__dns_queries.get(query_name)
        if value is None:
            self.__dns_queries[query_name] = {
                "lastQueryId": query_id,
                "count": 1,
            }
        else:
            self.__dns_queries[query_name]["lastQueryId"] = query_id
            self.__dns_queries[query_name]["count"] = value["count"] + 1

    def __upsert_dns_response(self, query_id: str, resolved_ips: list):
        for key, value in self.__dns_queries.items():
            dns_entry = self.__dns_queries[key]
            if dns_entry["lastQueryId"] == query_id and len(resolved_ips) > 0:
                dns_entry["resolvedIp"] = resolved_ips[0]

    def start(self):
        self.__stop_sniffing.clear()
        self.__sniffer_thread = threading.Thread(target=self.__start_sniffing)
        self.__sniffer_thread.start()

    def stop(self):
        self.__stop_sniffing.set()
        self.__sniffer_thread.join()
        self.__dns_queries = {}

    def get_dns_results(self):
        return self.__dns_queries
