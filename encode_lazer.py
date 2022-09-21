from machine import Pin
import time

lazer = Pin(2, Pin.OUT)

MESSAGE = "243-5124"
MESSAGE2 = "0123456789"
NUMBERS = []

def loop():
    print('\nsending: ', end="")
    x = .005
    y = .015
    z = .005
    for num in NUMBERS:
        time.sleep(y)
        for _ in range(num):
            now = time.time()
            time.sleep(x)
            lazer.value(1)
            time.sleep(x)
            lazer.value(0)
        print(num % 10, end="")
    time.sleep(z)

def init():
    global NUMBERS, MESSAGE2
    for textnum in MESSAGE2:
        try:
            if textnum == "0":
                NUMBERS.append(int(10))
            else:
                NUMBERS.append(int(textnum))
        except:
            continue
    print("Message to send:", MESSAGE2)

if __name__ == '__main__':
    init()
    while True:
        loop()
