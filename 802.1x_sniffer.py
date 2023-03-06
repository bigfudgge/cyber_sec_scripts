import pyshark
import time

# Определяем имя сетевого интерфейса, с которого будем захватывать пакеты

interface = input('Введите название сетевого интерфейса: ')

# Захват пакетов с указанного сетевого интерфейса
capture = pyshark.LiveCapture(interface=interface)

# Время захвата пакетов (в секундах)
capture_time = 30

# Захват пакетов в течение указанного времени
capture.sniff(timeout=capture_time)

# Перебираем все захваченные пакеты
for packet in capture:
    # Поиск пакетов EAPOL (Extensible Authentication Protocol Over LAN)
    if 'EAPOL' in packet:
        # Проверка, что пакет является пакетом аутентификации 802.1x
        if packet.eapol.type == '3':
            # Вывод сообщения, что безопасность 802.1x включена
            print("802.1x Port Security включен")




#capture = pyshark.LiveCapture(interface='eth0', bpf_filter='port 1812') #захватываем трафик на интерфейсе eth0 и фильтруем по порту 1812

#for packet in capture.sniff_continuously(): #захватываем пакеты непрерывно
   # if 'EAPOL' in packet: #проверяем, содержит ли пакет EAPOL-протокол
    #    print(packet)
