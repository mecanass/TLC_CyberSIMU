###################################################
#                Anass Janah 2023                 #
###################################################
#                                                 #
#       Simulation de feu de circulation.         #
#  Ce projet est dans le cadre du cours INF6103.  #
#                                                 #
###################################################
import os
import sys
import optparse
import threading
import multiprocessing
import time
from art import *
from sumolib import checkBinary  # Checks for the binary in environ vars
import traci
from pyModbusTCP.client import ModbusClient

# on doit importer some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
client = ModbusClient(host="127.0.0.1", port=502)


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def show_lights_state():
    F1 = traci.trafficlight.getRedYellowGreenState("F1")
    F2 = traci.trafficlight.getRedYellowGreenState("F2")
    F3 = traci.trafficlight.getRedYellowGreenState("F3")
    F4 = traci.trafficlight.getRedYellowGreenState("F4")
    print("Etat du feu rouge")
    print("F1: " + F1)
    print("F2: " + F2)
    print("F3: " + F3)
    print("F4: " + F4)


def green_light_forever():
    traci.trafficlight.setRedYellowGreenState("F1",'GGGGG')
    traci.trafficlight.setRedYellowGreenState("F2",'GGGGG')
    traci.trafficlight.setRedYellowGreenState("F3",'GGGGG')
    traci.trafficlight.setRedYellowGreenState("F4",'GGGGGG')
    normal_phase_scadabr()

def step_up():
        show_lights_state()
        traci.simulationStep()
        time.sleep(1)

## fonction pour montrer un fonctionnement normal dans scadaBR
def normal_phase_scadabr():
    reg_zero = client.read_holding_registers(1)
    while reg_zero[0] == 1:
        client.write_single_coil(0,1)
        client.write_single_coil(1,0)
        client.write_single_coil(2,0)
        client.write_single_coil(3,1)
        client.write_single_coil(4,0)
        client.write_single_coil(5,0)
        client.write_single_coil(6,0)
        client.write_single_coil(7,0)
        client.write_single_coil(8,1)
        client.write_single_coil(9,0)
        client.write_single_coil(10,0)
        client.write_single_coil(11,1)
        for x in range(15):
            step_up()
        client.write_single_coil(0,0)
        client.write_single_coil(1,1)
        client.write_single_coil(2,0)
        client.write_single_coil(3,0)
        client.write_single_coil(4,1)
        client.write_single_coil(5,0)
        for x in range(3):
            step_up()
        client.write_single_coil(0,0)
        client.write_single_coil(1,0)
        client.write_single_coil(2,1)
        client.write_single_coil(3,0)
        client.write_single_coil(4,0)
        client.write_single_coil(5,1)
        client.write_single_coil(6,1)
        client.write_single_coil(7,0)
        client.write_single_coil(8,0)
        client.write_single_coil(9,1)
        client.write_single_coil(10,0)
        client.write_single_coil(11,0)
        for x in range(15):
            step_up()
        client.write_single_coil(6,0)
        client.write_single_coil(7,1)
        client.write_single_coil(8,0)
        client.write_single_coil(9,0)
        client.write_single_coil(10,1)
        client.write_single_coil(11,0)
        for x in range(3):
            step_up()

def run():

    while traci.simulation.getMinExpectedNumber() > 0:
        F1 = traci.trafficlight.getRedYellowGreenState("F1")
        F2 = traci.trafficlight.getRedYellowGreenState("F2")
        F3 = traci.trafficlight.getRedYellowGreenState("F3")
        F4 = traci.trafficlight.getRedYellowGreenState("F4")
        show_lights_state()
        ##
        traci.simulationStep()
        #print("La valeur du reg 1: " + client.read_holding_registers(1))
        if client.read_holding_registers(1)[0] != 1:
            if (F1[0] == "G"):
                client.write_single_coil(0,1)
                client.write_single_coil(1,0)
                client.write_single_coil(2,0)
            elif (F1[0] == "y"):
                client.write_single_coil(0,0)
                client.write_single_coil(1,1)
                client.write_single_coil(2,0)
            elif (F1[0] == "r"):
                client.write_single_coil(0,0)
                client.write_single_coil(1,0)
                client.write_single_coil(2,1)

            if (F2[0]=="G"):
                client.write_single_coil(3,1)
                client.write_single_coil(4,0)
                client.write_single_coil(5,0) 
            elif (F2[0]=="y"):
                client.write_single_coil(3,0)
                client.write_single_coil(4,1)
                client.write_single_coil(5,0)
            elif (F2[0]=="r"):
                client.write_single_coil(3,0)
                client.write_single_coil(4,0)
                client.write_single_coil(5,1)

            if (F3[0]== "G"):
                client.write_single_coil(6,1)
                client.write_single_coil(7,0)
                client.write_single_coil(8,0)
            elif (F3[0]== "y"):
                client.write_single_coil(6,0)
                client.write_single_coil(7,1)
                client.write_single_coil(8,0)

            elif (F3[0]== "r"):
                client.write_single_coil(6,0)
                client.write_single_coil(7,0)
                client.write_single_coil(8,1)

            if (F4[0] == "G"):
                client.write_single_coil(9,1)
                client.write_single_coil(10,0)
                client.write_single_coil(11,0)
            elif (F4[0] == "y"):
                client.write_single_coil(9,0)
                client.write_single_coil(10,1)
                client.write_single_coil(11,0)
            elif (F4[0] == "r"):
                client.write_single_coil(9,0)
                client.write_single_coil(10,0)
                client.write_single_coil(11,1)
        else:
            green_light_forever()
# main entry point
try:
    tprint("DEMO")
    tprint("projet   INF6103")
    tprint("")
    if __name__ == "__main__":
        options = get_options()

        # check binary
        if options.nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')

        # traci starts sumo as a subprocess and then this script connects and runs
        traci.start([sumoBinary, "-c", "SUMO_FILES\osm.sumocfg",
                                "--tripinfo-output", "tripinfo.xml"])
        run()
except:
    print("Arret du programme.")
    traci.close()
    client.close()