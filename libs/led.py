import subprocess, time

def run(file):
    on()
    with open(file) as temp_file:
        f = [line.rstrip('\n') for line in temp_file]        
        for linha in f:        
            commands = linha.split('|')            
            subprocess.call("irsend SEND_ONCE LED_24_KEY " + commands[0], shell=True)
            time.sleep(float(commands[1]))
        
def on():
    subprocess.call("irsend SEND_ONCE LED_24_KEY ON", shell=True)
    
def off():
    subprocess.call("irsend SEND_ONCE LED_24_KEY OFF", shell=True) 
