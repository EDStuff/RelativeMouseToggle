# Title: Trackball/Mouse to Analog Axis for Elite: Dangerous, with "Relative Mouse" additional axis emulation.
# Author: Andrea Spada
# Version: 3.4
#
# Features: Simulate analog axis from mouse for yaw and pitch. It use vJoy.
#
# Each mouse direction is mapped to two axis. So, for lateral movement, we have both X and RX axis.
# Vertical movements are mapped to Y and RY.
#
# X and Y give absolute mouse movement, like an analog joystick with no springs. They are smart auto-centering when near the center.
# The range of this self-centering (mostly for aim purpouse) is defined by a customizable radius. 
# They also has a small exponential curve, so near zaro they give a smooth movement. The farther, the coarser.
#
# RX and RY axis give relative mouse movement, not unlike a directional pad. It's perfect for flying FA-Off, or for 
# more precise situations: mining, landing, etc...
#
# Both movement can be easily tweaked in sensitivity.
#
# Two more axis are used for the SRV, configured differently: horizontal movement is steeering, vertical movement is throttle.

from System import Int16

if starting:
	# Timer, for auto-centering
	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5 # loop delay
	
	# Devices and axis initializing
	max =  Int16.MaxValue*0.5+0.5   #  16384
	min = -Int16.MaxValue*0.5-0.5   # -16384
	joystick[0].setRange(min, max)
	mouseX	= 0
	mouseY	= 0
	mouseXcurved = 0
	mouseYcurved = 0
	mouseRX	= 0
	mouseRY	= 0
	steerX = 0
	steerXcurved = 0
	srvthrottle = 0
	joyX = 0
	joyY = 0
	joyXcurved = 0
	joyYcurved = 0
	
	# Coordinates for self centering
	a = 0
	b = 0
	c = 0
	d = 0

	# toggles
	roll2yaw = False
	vertical2pitch = False
	mouse2joystick = False


# Global parameters
global absolute_sens, relative_sens, steering_sens, srvthrottle_sens, relative_range, smart_speed, rel_speed, curve, mradius, tradius, mcurve, mratio, jcurve, jratio, scurve, sratio

absolute_sens = 60		    	# absolute mouse mode sensitivity
relative_sens = 85	    		# relative mouse mode sensitivity
steering_sens = 70			# steering sensitivity
srvthrottle_sens = 18			# SRV throttle sensitivity

relative_range = 450			# relative mouse range for auto centering
smart_speed = 25 			# smart-centering speed, in absolute mouse mode
rel_speed = 500		    		# hard-centering speed, in relative mouse mode

mcurve = 1.35  			    	# exponential factor for the mouse axis curve
mratio = (max ** mcurve ) / max 	# ratio to normalize mouse range
jcurve = 2.0				# exponential factor for the joystick axis
jratio = (max ** jcurve ) / max		# ratio to normalize joystick range
scurve = 1.6				# exponential factor for the steering axis
sratio = (max ** scurve ) / max		# ratio to normalize steering range

mradius = 3000                      	# smart self-centering radius, for absolute mouse
tradius = 750				# SRV Throttle auto centering for easy halt
throttle_speed = 25
srvthrottle_inc = 250			# SRV Throttle increment multiplicator

#
###
##### Mouse

# axis definition
mouseX += mouse.deltaX * absolute_sens      # absolute mouse, lateral
mouseY += mouse.deltaY * absolute_sens      #                 vertical
mouseRX += mouse.deltaX * relative_sens     # relative mouse, lateral
mouseRY += mouse.deltaY * relative_sens     #                 vertical

# define a range and limit the axis values
if (mouseX > max):
  mouseX = max
elif (mouseX < min):
  mouseX = min

if (mouseY > max):
  mouseY = max
elif (mouseY < min):
  mouseY = min

if (mouseRX > max):
  mouseRX = max
elif (mouseRX < min):
  mouseRX = min

if (mouseRY > max):
  mouseRY = max
elif (mouseRY < min):
  mouseRY = min

# 
##
### Absolute Mouse

# smart centering
if (mouseX < mradius) and (mouseX > 0):
	mouseX = mouseX - smart_speed
elif (mouseX > (mradius * -1)) and (mouseX < 0):
	mouseX = mouseX + smart_speed

if (mouseY < mradius) and (mouseY > 0):
	mouseY = mouseY - smart_speed
elif (mouseY > (mradius * -1)) and (mouseY < 0):
	mouseY = mouseY + smart_speed

# lightly exponential curved axis
if (mouseX > 0):
	mouseXcurved = math.floor((mouseX ** mcurve) / mratio) 
if (mouseX < 0):
	mouseXn = mouseX * -1
	mouseXcurved = math.floor(((mouseXn ** mcurve) * -1) / mratio)

if (mouseY > 0):
	mouseYcurved = math.floor((mouseY ** mcurve) / mratio) 
if (mouseY < 0):
	mouseYn = mouseY * -1
	mouseYcurved = math.floor(((mouseYn ** mcurve) * -1) / mratio)

# Mouse Output
vJoy[0].x = filters.deadband(mouseXcurved, 20)
vJoy[0].y = filters.deadband(mouseYcurved, 20)

#
##
### Relative Mouse

# Self Centering Alternate Axis
a += mouse.deltaX
b += mouse.deltaX
if filters.stopWatch(True,60):
	c = a + 0
   
if filters.stopWatch(True,30):
	d = b + 0

if (c - d == 0):
	if mouseRX < -(relative_range):
		mouseRX += rel_speed
	elif mouseRX > relative_range:
		mouseRX -= rel_speed
	if mouseRY < -(relative_range):
		mouseRY += rel_speed
	elif mouseRY > relative_range:
		mouseRY -= rel_speed

# Mouse Output
vJoy[0].rx = filters.deadband(mouseRX, 500)
vJoy[0].ry = filters.deadband(mouseRY, 500)

#####
###
#

#
###
##### SRV

####### Steering
if (steerX > max):
  steerX = max
elif (steerX < min):
  steerX = min

steerX += mouse.deltaX * steering_sens

# exponential curved axis, for smooth steeering
if (steerX > 0):
	steerXcurved = math.floor((steerX ** scurve) / sratio) 
if (steerX < 0):
	steerXn = steerX * -1
	steerXcurved = math.floor(((steerXn ** scurve) * -1) / sratio)

# Steering Output
vJoy[0].slider = filters.deadband(steerXcurved, 20)

####### Throttle
if (srvthrottle > max):
  srvthrottle = max
elif (srvthrottle < min):
  srvthrottle = min

srvthrottle += mouse.deltaY * srvthrottle_sens

# Throttle will center itself if near the center, so to easily halt the SRV
if (srvthrottle < tradius) and (srvthrottle > 0):
	srvthrottle = srvthrottle - throttle_speed

if (srvthrottle > (tradius * -1)) and (srvthrottle < 0):
	srvthrottle = srvthrottle + throttle_speed

srvthrottle -= (mouse.wheelUp * srvthrottle_inc) 
srvthrottle += (mouse.wheelDown * srvthrottle_inc) 

# SRV Throttle Output
vJoy[0].dial = filters.deadband(srvthrottle, 100)

#####
###
#

#
###
##### Logitech G13 - UNCOMMENT IF NEED IT
#joyX = joystick[0].x
#joyY = joystick[0].y

# Exponential curved axis
#if (joyX > 0):
#	joyXcurved = math.floor((joyX ** jcurve) / jratio) 
#if (joyX < 0):
#	joyXn = joyX * -1
#	joyXcurved = math.floor(((joyXn ** jcurve) * -1) / jratio)
#
#if (joyY > 0):
#	joyYcurved = math.floor((joyY ** jcurve) / jratio) 
#if (joyY < 0):
#	joyYn = joyY * -1
#	joyYcurved = math.floor(((joyYn ** jcurve) * -1) / jratio)

# Joystick output
#vJoy[0].z = filters.deadband(joyXcurved, 50)
#vJoy[0].rz = filters.deadband(joyYcurved, 50)

#####
###
#

#
###
##### Axis fallback, for easy assignment

# Absolute Mouse
if keyboard.getKeyDown(Key.NumberPad4) and keyboard.getKeyDown(Key.RightShift):
	vJoy[0].x = max 
if keyboard.getKeyDown(Key.NumberPad2) and keyboard.getKeyDown(Key.RightShift):
	vJoy[0].y = max

# Relative Mouse
if keyboard.getKeyDown(Key.NumberPad6) and keyboard.getKeyDown(Key.RightShift):
	vJoy[0].rx = max
if keyboard.getKeyDown(Key.NumberPad8) and keyboard.getKeyDown(Key.RightShift):
	vJoy[0].ry = max

# Joystick Axis
#if keyboard.getKeyDown(Key.NumberPad4) and keyboard.getKeyDown(Key.LeftShift):
#	vJoy[0].z = min
#if keyboard.getKeyDown(Key.NumberPad2) and keyboard.getKeyDown(Key.LeftShift):
#	vJoy[0].rz = max
#if keyboard.getKeyDown(Key.NumberPad6) and keyboard.getKeyDown(Key.LeftShift):
#	vJoy[0].z = max 
#if keyboard.getKeyDown(Key.NumberPad8) and keyboard.getKeyDown(Key.LeftShift):
#	vJoy[0].rz = min

#####
###
#

#
###
##### Utilities

# Soft Centering - slow down axis values

if keyboard.getKeyDown(Key.LeftControl):
	if mouseX > 0:
		mouseX = mouseX - 100
	if mouseX < 0:
		mouseX = mouseX + 100
	
	if mouseY > 0:
		mouseY = mouseY - 100
	if mouseY < 0:
		mouseY = mouseY + 100
	
	if steerX > 0:
		steerX = steerX - 100
	if steerX < 0:
		steerX = steerX + 100
	
# Hard Centering (By press an hotkey)
# Useful when you need your mouse to return to the center, like when you switch workspaces or exiting galaxy map...

if keyboard.getKeyDown(Key.LeftControl) and keyboard.getPressed(Key.LeftWindowsKey):
	mouseX = 0
	mouseY = 0
	mouseXcurved = 0
	mouseYcurved = 0
	steerX = 0
	steerXcurved = 0

if keyboard.getKeyDown(Key.Backspace): 
	mouseX = 0
	mouseY = 0
	mouseXcurved = 0
	mouseYcurved = 0
	steerX = 0
	steerXcurved = 0
	srvthrottle = 0
	povX = 0
	povY = 0

if keyboard.getKeyDown(Key.M):
	mouseX = 0
	mouseY = 0
	mouseXcurved = 0
	mouseYcurved = 0
	steerX = 0
	steerXcurved = 0
	srvthrottle = 0
	povX = 0
	povY = 0
	
#####
###
#

#
###
##### Diagnostics

# vJoy
diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)
diagnostics.watch(vJoy[0].rx)
diagnostics.watch(vJoy[0].ry)
diagnostics.watch(vJoy[0].slider)
diagnostics.watch(vJoy[0].dial)
#diagnostics.watch(vJoy[0].z)
#diagnostics.watch(vJoy[0].rz)
