from time import sleep
from motion_class import Motion

m =  Motion()
color = m.collect_block()
m.device.suck(False)

colors = ["red", "green", "blue"]
print("This is the color", colors[color])
