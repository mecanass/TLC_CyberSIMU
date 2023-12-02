
###################################################
#                Anass Janah 2023                 #
###################################################
#                                                 #
#       Simulation de feu de circulation.         #
#  Ce projet est dans le cadre du cours INF6103.  #
#      script pour simuler le serveur modbus      #
#                                                 #
###################################################

from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
from art import *

# Créer une instance de modbusServer
server = ModbusServer('0.0.0.0', 502, no_block=True)

try:
    tprint("projet   INF6103")
    tprint("serveur Modbus")
    print("demarage du serveur...")
    server.start()
    print("Le serveur est en ligne.")
    state = [0]
    while True:
        if state != server.data_bank.get_holding_registers(1):
            state = server.data_bank.get_holding_registers(1)
            print("La valeur du registre 1 a changé:" + str(state))
            sleep(0.5)
except:
    print("Arret du serveur...")
    server.stop()
    print("Le serveur est hors ligne.")