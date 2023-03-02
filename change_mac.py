#! /usr/bin/env python3


import subprocess
import os


#Use ifconfig to display information about the state of active network interfaces
ifconfig = subprocess.run(['ifconfig'])

print(ifconfig)


#Add the name of the network interface to the variable
interface = input("Введите имя сетевого интерфейса: ")

factory_mac = subprocess.check_output(['ethtool', '-P', interface]).decode().split(" ")[-1].strip()

print(f"Текущий MAC-адрес: {factory_mac}")


#Function for changing mac address
def change_mac():
    mac_list = ['b0:5c:da:e2:61:aa', 'b0:5c:da:e2:61:ab', 'b0:5c:da:e2:61:ac', 'b0:5c:da:e2:61:cc']

    print("Доступные MAC-адреса: [1] TSV 601 vlan, [2] ARM_KIOSK 275 vlan, [3] Стандартный для WiFi vlan 808, [4] Случайный):")

    for i, mac in enumerate(mac_list):
        print(f"{i+1}: {mac}")

    mac_choice = int(input("Выберите номер MAC-адреса: "))
    mac_address = mac_list[mac_choice-1]

    command_down = f'sudo ifconfig {interface} down'
    subprocess.call(command_down, shell=True)
    command_hw = f'sudo ifconfig {interface} hw ether {mac_address}'
    subprocess.call(command_hw, shell=True)
    command_up = f'sudo ifconfig {interface} up'
    subprocess.call(command_up, shell=True)
    print(f"MAC-адрес изменен на {mac_address}")

#Function to return the mac address
def return_mac():
    choice = input("Хотите вернуть заводской MAC-адрес? (y/n): ")
    if choice.lower() == "y":
        subprocess.call(['sudo', 'ifconfig', interface, 'down'])
        subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', factory_mac])
        subprocess.call(['sudo', 'ifconfig', interface, 'up'])
        print(f"MAC-адрес вернулся на заводской: {factory_mac}")

    else:
        print("MAC-адрес оставлен без изменений")

#Cycle for selecting actions
while True:
    action = input("Выберите действие (1 - смена mac-адреса), (2 - вернуть заводской mac-адрес) (3 - выйти): ")
    if action == "1":
        change_mac()
    elif action == "2":
        return_mac()
    elif action == "3":
        break
    else:
        print("Некорректный выбор!")
