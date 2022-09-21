from machine import Pin, Timer, PWM
import random, time

speaker = PWM(Pin(16))
VOLUME = 2**16//128

notes = [
    262,
    294,
    330,
    370,
    392
]

leds = [
    Pin(2, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(6, Pin.OUT),
    Pin(8, Pin.OUT),
    Pin(10, Pin.OUT)
]

buttons = [
    Pin(3, Pin.IN, Pin.PULL_UP),
    Pin(5, Pin.IN, Pin.PULL_UP),
    Pin(7, Pin.IN, Pin.PULL_UP),
    Pin(9, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP),
]

sequence = []
current_index = 0

def waitForButton(timeout=1000, display=True, sound=True):
    now = time.ticks_ms()
    while time.ticks_ms() - now < timeout:
        #listen for button press
        for i in range(len(buttons)):
            if not buttons[i].value():
                leds[i].value(display)
                speaker.freq(notes[i])
                if sound:
                    speaker.duty_u16(VOLUME)
                while not buttons[i].value():
                    pass
                time.sleep(0.2)
                leds[i].value(0)
                speaker.duty_u16(0)
                return i
    return -1
                

def init():
    global sequence
    global current_index
    
    beep(notes[1], 0)
    waitForButton(360000, False, False)
    for i in range(4):
        time.sleep(.15)
        beep(notes[4], .15)
    
    sequence = []
    current_index = 0
    for led in leds:
        led.value(0)
    generateStartSequence(1)

def loop():
    global sequence
    global current_index
    
    # sequence complete
    if current_index == len(sequence):
        incSequence()
    
    # new sequence
    if current_index == 0:
        displaySequence()
    
    # read player input
    pressed = waitForButton()
    
    # if wrong, end game
    if pressed != sequence[current_index]:
        gameOver()
        
    # if correct, increase current_index
    else:
        current_index += 1

def displaySequence():
    time.sleep(.25)
    for i in sequence:
        leds[i].value(1)
        beep(notes[i], .4)
        leds[i].value(0)
        time.sleep(.4)

def generateStartSequence(length=5):
    for i in range(length):
        sequence.append(random.randrange(0, len(buttons)))

def incSequence():
    global current_index
    sequence.append(random.randrange(0, len(buttons)))
    current_index = 0
    
def beep(frequency, duration):
    speaker.freq(frequency)
    speaker.duty_u16(VOLUME)
    time.sleep(duration)
    speaker.duty_u16(0)
    
def gameOver():
    for i in range(6):
        for led in leds:
            led.value(not led.value())
        if i != 3 or i != 4:
            beep(100, .25)
        else:
            time.sleep(.25)
    init()

if __name__ == '__main__':
    init()
    while True:
        loop()