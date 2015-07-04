# -*- coding: utf-8 -*-
from Xlib import display
from random import randint

print("Crazy Mouse!")
print("~-"*50)
d = display.Display()
s = d.screen()
root = s.root
while True:
    x = randint(1, 1024)
    y = randint(1, 1024)
    root.warp_pointer(x, y)
    d.sync()
