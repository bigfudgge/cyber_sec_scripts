#! /usr/bin/env python3


import subprocess
import os


#Use ifconfig to display information about the state of active network interfaces
subprocess.run(['ifconfig', '-a'])


#Add the name of the network interface to the variable
interface = input("Введите имя сетевого интерфейса: ")

original_conf = subprocess.check_output(['ifconfig', interface])

factory_mac = subprocess.check_output(['ethtool', '-P', interface]).decode().split(" ")[-1].strip()

print(f"\n{'='*10}Текущий MAC-адрес: {factory_mac}")



#function for changing mac
def change_mac():
    mac_list = ['mac1', 'mac2', 'mac3', 'mac4']

    print("\nДоступные MAC-адреса:")
    print("1. TSV"),
    print("2. ARM_KIOSK")
    print("3. WiFi")
    print("4. Случайный")
    #for i, mac in enumerate(mac_list):
        #print(f"{i+1}: {mac}")

    mac_choice = int(input("\nВыберите номер MAC-адреса: "))
    mac_address = mac_list[mac_choice-1]

    command_down = f'sudo ifconfig {interface} down'
    subprocess.call(command_down, shell=True)
    command_hw = f'sudo ifconfig {interface} hw ether {mac_address}'
    subprocess.call(command_hw, shell=True)
    command_up = f'sudo ifconfig {interface} up'
    subprocess.call(command_up, shell=True)
    print(f"\n{'='*10}MAC-адрес изменен на {mac_address}")

#Function to return the mac address
def return_mac():
    choice = input("Хотите вернуть заводской MAC-адрес? (y/n): ")
    if choice.lower() == "y":
        subprocess.call(['sudo', 'ifconfig', interface, 'down'])
        subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', factory_mac])
        subprocess.call(['sudo', 'ifconfig', interface, 'up'])
        print(f"\n{'='*10}MAC-адрес вернулся на заводской: {factory_mac}")

    else:
        print("\nMAC-адрес оставлен без изменений")



#changing IP
def change_ip():
    new_ip = input("\nВведите новый IP-адрес: ")
    new_netmask = input("\nВведите новую маску подсети: ")

    subprocess.run(['sudo', 'ifconfig', interface, 'down'])
    subprocess.run(['sudo', 'ifconfig', interface, new_ip, 'netmask', new_netmask])
    subprocess.run(['sudo', 'ifconfig', interface, 'up'])
    print("\nIP-адрес и маска подсети изменены:")
    print(subprocess.check_output(['ifconfig', interface]))



#Cycle for selecting actions
while True:
    print("\nВыберите действие:")
    print("1. Сменить MAC-адрес")
    print("2. Вернуть заводской MAC")
    print("3. Сменить IP-адрес и маску подсети")
    print("4. Выйти")
    action = input("\nВыберите номер действия: ")
    if action == "1":
        change_mac()
    elif action == "2":
        return_mac()
    elif action == "3":
        change_ip()
    elif action == "4":
        break
    else:
        print("Некорректный выбор действия!")
