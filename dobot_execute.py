#input values max(3x3)
#example input

#[[1,1,1][0,0,0][2,2,2]]
#0 - red
#1 - green
#2 - blue
#4 - null 

#block placement
#222
#000
#111

import sys
import ast
from time import sleep
from motion_class import Motion

def done(place_list):
    for i in place_list:
        if i != 4:
            return False 
    return True

def unstack_place(color, index, m): 
    m.unstack(color)
    m.place(index)

req = [4,4,4]



v = ast.literal_eval(sys.argv[1])

for i in v:
    print(i)
v.insert(0, [4,4,4])

pos1 = 3
pos2 = 3
pos3 = 3
req = [v[pos1][0],v[pos2][1], v[pos3][2]]

m =  Motion()

while not done(req):
    if m.has_stack(req[0]) or m.has_stack(req[1]) or m.has_stack(req[2]):
        if m.has_stack(req[0]):
            unstack_place(req[0], 0, m)
            pos1 -=1
            req[0] = v[pos1][0]
        elif m.has_stack(req[1]):
            unstack_place(req[1], 1, m)
            pos2 -=1
            req[1] = v[pos2][1]
        elif m.has_stack(req[2]):
            unstack_place(req[2], 2, m)
            pos3 -=1
            req[2] = v[pos3][2]
        continue
    color = m.collect_block()

    #if requiured place
    if req[0] == color:
        m.place(0)
        pos1 -=1
        req[0] = v[pos1][0]
    elif req[1] == color :
        m.place(1)
        pos2 -=1
        req[1] = v[pos2][1]
    elif req[2] == color :
        m.place(2)
        pos3 -= 1
        req[2] = v[pos3][2]
    else:
    #else stack
        m.stack(color)
        
m.disconnect()

'''


inputList = [2, 2, 1, 1, 0, 0]
for i in inputList:        
    color = m.collect_block()
    m.stack(color)

for i in inputList:
    m.unstack(i)
    m.place(i)


'''
