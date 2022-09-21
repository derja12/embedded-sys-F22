from machine import Pin
import time

lazer = Pin(2, Pin.IN, Pin.PULL_UP)

BUMP_VALUE = .001

COUNT = 0
NUMBERS = []

def waitForSignal():
    now = time.ticks_ms()
    while time.ticks_ms() - now < 22:
        if not lazer.value():
            t = time.ticks_ms() - now
            while not lazer.value():
                pass
            time.sleep(BUMP_VALUE)
            return t
    return -1

def printNumbers():
    if len(NUMBERS) == 0:
        print("no number provided")
    else:
        print(''.join([str(0) if n == 10 else str(n) for n in NUMBERS]))

def loop():
    global COUNT, NUMBERS
    t = waitForSignal()
    COUNT = 1
    NUMBERS = []
    startingDecoding = time.ticks_ms()
    endingDecoding = time.ticks_ms()
    while t != 1:
        t = waitForSignal()
        if t == -1:
            NUMBERS.append(COUNT)
            print("It took", ((endingDecoding - startingDecoding) / 1000.0) ,"seconds to decode the message:")
            printNumbers()
            break

        if t < 15:
            COUNT += 1
            endingDecoding = time.ticks_ms()
        else:
            NUMBERS.append(COUNT)
            COUNT = 1

def init():
    global COUNT, NUMBERS
    NUMBERS = []
    COUNT = 0
    
if __name__ == '__main__':
    init()
    while True:
        loop()
