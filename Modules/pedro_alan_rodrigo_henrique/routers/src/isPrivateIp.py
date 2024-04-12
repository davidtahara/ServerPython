def isPrivateIp(ip: str):
    ip = ip.split(".")
    if ip[0] == "10":
        return True
    if ip[0] == "192" and ip[1] == "168":
        return True
    if ip[0] == "172" and 16 <= int(ip[1]) <= 31:
        return True
    return False
