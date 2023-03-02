
import socket


ip_target = input("ip-адрес подсети: ")

#задаем диапазон ip-адресов для скана
ip_range = [ip_target + str(i) for i in range(1, 255)]

#определяем порты для проверки
port = 5000
port = 1900

#идентификатор строки в ответе, указывающий на miniupnpd
service_identifier = b"MiniUPnPd"

#проходим по всем ip и проверяем доступность порта
for ip in ip_range:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            #проверяем что ответ содержит идентиф сервиса miniupnpd
            data = sock.recv(1024)
            if service_identifier in data:
                print("Найдена камера hickvision на ip-адресе {ip}")
        sock.close()
    except:
        pass


#проверяем по порту 1900
for ip in ip_range:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.socktimeout(1)
        sock.sendto(b"M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nST:ssdp:all\r\nMan:\"ssdp:discover\"\r\nMX:3\r\n\r\n", (ip, port))
        data, _ = sock.recvfrom(1024)
        if service_identifier in data:
            version = data.decode().split("MiNIUPNPD/")[1].split("\r\n")[0]
            print("Найдена камера hickvision на ip-адресе: {ip}, версия miniupnpd: {version}")
        sock.close()
    except:
        pass
