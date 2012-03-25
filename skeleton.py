#! /usr/bin/python -u
'''
This is a Skeleton file.  It provides a 
template to be used when writing a new
TouchPy application.
'''

from touch import *

screen_dimensions = (1280, 800)

class Observer(object):
	def __init__(self, subject):
		subject.push_handlers(self)

class touch_up(Observer):
	def TOUCH_UP(self,blobID, xpos, ypos):
		x = int(round(t.blobs[blobID].xpos * screen_dimensions[0]))
		y = int(round(t.blobs[blobID].ypos * screen_dimensions[1]))
		print 'Touch Up at ' + str(x) + ', ' + str(y)

class touch_down(Observer):
	def TOUCH_DOWN(self,blobID):
		x = int(round(t.blobs[blobID].xpos * screen_dimensions[0]))
		y = int(round(t.blobs[blobID].ypos * screen_dimensions[1]))
		print 'Touch Down at ' + str(x) + ', ' + str(y)

class touch_move(Observer):
	def TOUCH_MOVE(self,blobID):
		x = int(round(t.blobs[blobID].xpos * screen_dimensions[0]))
		y = int(round(t.blobs[blobID].ypos * screen_dimensions[1]))
		print 'Touch Move at ' + str(x) + ', ' + str(y)

t = touchpy()
tu = touch_up(t)
td = touch_down(t)
tm = touch_move(t)

try:
	while True:
		t.update()

except (KeyboardInterrupt, SystemExit):
	del t
