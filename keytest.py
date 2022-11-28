import keyboard
while True:

    keyboard.on_release(lambda e: print(e.name))