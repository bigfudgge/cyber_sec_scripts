import pyshark

# Определение фильтра для захвата только EAPOL пакетов
capture_filter = "eapol"

# Создание экземпляра каптурера
capture = pyshark.LiveCapture(interface='<interface_name>', bpf_filter=capture_filter)

# Цикл по каждому пакету в захвате
for packet in capture.sniff_continuously():
    # Проверка, является ли пакет EAPOL
    if 'EAPOL' in packet:
        # Доступ к полям пакета
        print("Source MAC:", packet.eth.src)
        print("Destination MAC:", packet.eth.dst)
        print("EAPOL packet type:", packet.eapol.type)

# Остановка захвата пакетов
capture.close()
