import subprocess
import time

def run(path):
    f = open(path)
    for linha in f:
        commands = linha.split('|')
        subprocess.call("irsend SEND_ONCE LED_24_KEY " + commands[0], shell=True)
        time.sleep(int(commands[1]))
        
def on():
    subprocess.call("irsend SEND_ONCE LED_24_KEY ON", shell=True)
    
def off():
    subprocess.call("irsend SEND_ONCE LED_24_KEY OFF", shell=True)
    
