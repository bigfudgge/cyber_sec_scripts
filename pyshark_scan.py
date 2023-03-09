import pyshark
import time
import subprocess




#выводим список сетевых интерфейсов
subprocess.run(['ifconfig', '-a'])

# Определяем имя сетевого интерфейса, с которого вы хотите захватывать пакеты
interface = input('\nВведите название сетевого интерфейса: ')

print(f"\n{'='*5}!!!Идет поиск пакетов 802.1x Authentication!!!{'='*5}")

# Через livecapture указываем захват пакетов с заданного сетевого интерфейса
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
            # Вывод сообщения, 802.1x включен
            print("802.1x Port Security включен")
    else:
        print("Пакеты с протоколом EAPOL не найдены!!!")
        break
