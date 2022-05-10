#!/usr/bin/env python
import os

def sb_write(fd, servo, pulse):
    try:
        os.write(fd, '%d=%d\n' % (servo,pulse))
    except IOError as e:
        print e

def write(servo, pulse):
    if servo == 1:
        if pulse < 100 or pulse > 200:
            print 'PWM %d out of range!' % (pulse)
            return
            
    if servo == 2:
        if pulse < 100 or pulse > 200:
            print 'PWM %d out of range!' % (pulse)
            return
        
    sb_write(fd, servo, pulse)

try:
    fd = os.open('/dev/servoblaster', os.O_WRONLY)
except OSError as e:
    print 'could not open /dev/servoblaster'
    raise SystemExit(5)
except (KeyboardInterrupt, SystemExit):
    os.close(fd)
    pass


