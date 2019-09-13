# RelativeMouseToggle
FreePIE script, using vJoy, which provide means to effectively be able to toggle your mouse behavior from relative to absolute.

### Preliminary Setup
You need both vJoy (https://github.com/shauleiz/vJoy) and FreePIE (https://github.com/AndersMalmgren/FreePIE) to use this script.

Adjust your device index in the script before running it. 

### How it works

It create two parallels axis couples - x, y, rx, ry - which emulate two differente analog behavior. The **x** and **y** axis are non-relative, which it means that after you moved the mouse, the axis values do not center itself. They center itself only if really near to the center, to help with aiming and scanning... **rx** and **ry** emulate a relative mouse, so they automatically center itself, no matter how far you are from the center of the axis: they are perfect for FA-Off flight, and for more precise operation.

They are intended to be used this way: **x** and **y** assigned in "alternate flight control", and **rx** and **ry** in "standard flight control". 
I prefer to use **x** and **rx** as Yaw, but you can use it for Roll as well, of course...

All axis can be curved, with a very simple exponential equation, to behave with a more natural and ergonomic feel. 
All parameters are freely adjustable, and normalize itself to avoid values beyond the axis range.

Use the Watch panel in FreePIE to see how the axis works.

---

The script also provide two more ready-to-use axis, **slider** and **dial**. I programmed them for SRV steering and throttle. You are free to use them the way you prefer, or skip them.

The **z** and **rz** axis are used for my Logitech G13 Joystick, which I use for Pitch and Vertical Thrust. They can be assigned to another functionality, or skipped.
