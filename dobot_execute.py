#input values max(3x3)
#example input

#[[1,1,1][0,0,0][2,2,2]]
#0 - red
#1 - green
#2 - blue

#block placement
#222
#000
#111

from time import sleep
from motion_class import Motion

m =  Motion()

inputList = [2, 2, 1, 1, 0, 0]
for i in inputList:        
    color = m.collect_block()
    m.stack(color)

for i in inputList:
    m.unstack(i)
    m.place(i)

m.disconnect()
