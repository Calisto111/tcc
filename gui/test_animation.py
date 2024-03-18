from Blender import Redraw, Scene
from subprocess import Popen, PIPE
from select import poll, POLLIN
import bpy

# Handler function: plays differente animations
def playanim(scene_name):
    sce = Scene.Get(scene_name)
    sce.makeCurrent()
    sce.play(2)

# Create subprocess
my_child = Popen('./config_network.py', stdout=PIPE)

# Create polling object
p1 = poll()

# Register child's stdout for polling
p1.register(my_child.stdout, POLLIN)

line = '-1' # Stop condition initialization

while line != '0\n':
    Redraw()
    if p1.poll(10):                   
        line = my_child.stdout.readline()
        #if line == '1\n':
        #    playanim('HandExtension')
        #elif line == '2\n':
        #    playanim('HandFlexion')
        #elif line == '3\n':
        #    playanim('HandGrasp')
        #elif line == '4\n':
        #    playanim('HandPronSup')
        if line == '5\n':
            playanim('ElbolExtention')
        elif line == '6\n':
            playanim('ElbolFlexion')
        else:
            pass
