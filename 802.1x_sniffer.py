import pyshark
import time
import subprocess




#выводим список сетевых интерфейсов
subprocess.run(['ifconfig', '-a'])

# Определяем имя сетевого интерфейса, с которого вы хотите захватывать пакеты
interface = input('\nВведите название сетевого интерфейса: ')

#сохраняем конфиг сети
original_conf = subprocess.check_output(['ifconfig', interface])

factory_mac = subprocess.check_output(['ethtool', '-P', interface]).decode().split(" ")[-1].strip()

print(f"\n{'='*10}ТЕКУЩИЙ MAC-адрес: {factory_mac}")


command_down = f'sudo ifconfig {interface} down'
subprocess.call(command_down, shell=True)
command_hw = f'sudo ifconfig {interface} hw ether b0:5c:da:e2:62:cc'
subprocess.call(command_hw, shell=True)
command_up = f'sudo ifconfig {interface} up'
subprocess.call(command_up, shell=True)
print(f"\n{'='*10}[[[[[MAC-адрес изменен]]]]]")

subprocess.run(['ifconfig', '-a', interface])

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


#capture.close()

choice = input("Хотите вернуть заводской MAC-адрес? (y/n): ")
if choice.lower() == "y":
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', factory_mac])
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])
    print(f"\n{'='*10}MAC-адрес вернулся на заводской: {factory_mac}")
else:
    print("\nMAC-адрес оставлен без изменений")

subprocess.run(['ifconfig', '-a', interface])
