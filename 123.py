from ahk import AHK
import keyboard


a = AHK()



def df():
    while True:
        try:
            a.click()
        except:
            passa


keyboard.add_hotkey('a' , df)
keyboard.wait()