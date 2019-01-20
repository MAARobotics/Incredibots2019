from wallaby import *
import constants as c
import movement as m
import utils as u
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~HOW TO USE LFOLLOW COMMANDS~~~~~~~~~~~~~~~~~~~~~~~~
# All lfollow commands follow a certain pattern which if you learn, you can come up
# with commands without the need to look in this file. Keep in mind that these rules apply only to 
# lfollow commands, but once you learn their pattern you can figure out all other patterns.
# To start off, this is the pattern:
# lfollow_[left, right, backwards]_[inside_line]_[until_left_senses_black, until right senses black, until (event)]_[smooth]([time you want the lfollow to run in ms], [starting speed for left motor], [starting speed for right motor], [True or False whether or not you want the robot to stop after the commamds finishes], [refresesh rate for the lfollow in ms]) 
# - To signify that you want to run an lfollow command, write lfollow.
# - Then, you must choose which sensor you want to lfollow with (left tophat, right tophat, or the third tophat respectively)
# - After this, everything is optional and is only required if you choose to put it in and the situation calls for it.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~States~~~~~~~~~~~~~~~~~~~~~~~~

def BlackLeft():
    return(analog(c.LEFT_TOPHAT) > c.LEFT_TOPHAT_BW)

def NotBlackLeft():
    return(analog(c.LEFT_TOPHAT) < c.LEFT_TOPHAT_BW)

def BlackRight():
    return(analog(c.RIGHT_TOPHAT) > c.RIGHT_TOPHAT_BW)

def NotBlackRight():
    return(analog(c.RIGHT_TOPHAT) < c.RIGHT_TOPHAT_BW)

def BlackThird():
    return(analog(c.THIRD_TOPHAT) > c.THIRD_TOPHAT_BW)

def NotBlackThird():
    return(analog(c.THIRD_TOPHAT) < c.THIRD_TOPHAT_BW)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Basic Align Functions~~~~~~~~~~~~~~~~~~~~~~~~

def align_close():
# Aligns completely on the side of the line closest to the claw
    print "Starting align_close()"
    left_backwards_until_white()
    right_backwards_until_white()
    right_forwards_until_black()
    left_forwards_until_black()
    print "Aligned to close side of line\n"


def align_close_smart():
# Aligns completely on the side of the line closest to the claw
    print "Starting align_close_smart()"
    starting_left_time = seconds()
    if BlackLeft():
        left_backwards_until_white()
    else:
        left_forwards_until_black()
    total_left_time = seconds() - starting_left_time
    starting_right_time = seconds()
    if BlackRight():
        right_backwards_until_white()
    else:
        right_forwards_until_black()
    total_right_time = seconds() - starting_right_time
    print "Second motor run time: " + str(total_right_time)
    if total_right_time > .3:
        print "Another align is probably necessary here.\n"
        if BlackLeft():
            left_backwards_until_white()
        else:
            left_forwards_until_black()
    print "Aligned to close side of line\n"


def align_far(left_first = True):
# Aligns completely on the side of the line closest to the camera
    print "Starting align_far()"
    if left_first == True:
        right_forwards_until_white()
        left_forwards_until_white()
        left_backwards_until_black()
        right_backwards_until_black()
    else:
        left_forwards_until_white()
        right_forwards_until_white()
        right_backwards_until_black()
        left_backwards_until_black()
    print "Aligned to far side of line\n"


def align_far_safe():
# Aligns completely on the side of the line closest to the camera
    print "Starting align_far()"
    if u.not_bumped():
        right_forwards_until_white_safe()
    if u.not_bumped():
        left_forwards_until_white_safe()
    if u.not_bumped():
        left_backwards_until_black_safe()
    if u.not_bumped():
        right_backwards_until_black_safe()
    print "Aligned to far side of line\n"


def align_far_smart():
# Aligns completely on the side of the line closest to the camera
    print "Starting align_far_smart()"
    if BlackLeft() and BlackRight():
        drive_until_both_white()
    starting_left_time = seconds()
    if BlackLeft():
        left_forwards_until_white()
    else:
        left_backwards_until_black()
    total_left_time = seconds() - starting_left_time
    starting_right_time = seconds()
    if BlackRight():
        right_forwards_until_white()
    else:
        right_backwards_until_black()
    total_right_time = seconds() - starting_right_time
    print "Time difference: " + str(abs(total_left_time - total_right_time))
    if abs(total_left_time - total_right_time) > .5:
        print "Woah there! We probably need to do another align here./n"
        if total_left_time > total_right_time:
            if BlackRight():
                right_forwards_until_white()
            else:
                right_backwards_until_black()
        else:
            if BlackLeft():
                left_forwards_until_white()
            else:
                left_backwards_until_black()
    print "Aligned to far side of line\n"


def left_backwards_until_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes back until the left tophat senses white
    print "Starting left_backwards_until_white()"
    m.av(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def right_backwards_until_white(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Right motor goes back until right tophat senses white
    print "Starting right_backwards_until_white()"
    m.av(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def left_backwards_until_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes back until left tophat senses black
    print "Starting left_backwards_until_black()"
    m.av(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def left_backwards_until_black_safe(time = 1500, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes back until left tophat senses black
    print "Starting left_backwards_until_black_safe()"
    m.av(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while u.not_bumped() and seconds() < sec and NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def right_backwards_until_black(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Right motor goes back until right tophat senses black
    print "Starting right_backwards_until_black()"
    m.av(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def right_backwards_until_black_safe(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Right motor goes back until right tophat senses black
    print "Starting right_backwards_until_black_safe()"
    m.av(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while u.not_bumped() and seconds() < sec and NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def left_forwards_until_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes forwards until right tophat senses black
    print "Starting left_forwards_until_black()"
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def right_forwards_until_black(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Right motor goes forwards until right tophat senses black
    print "Starting right_forwards_until_black()"
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def left_forwards_until_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_white()"
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def left_forwards_until_white_safe(time = 1500, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_white_safe()"
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while u.not_bumped() and seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def left_forwards_until_third_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_third_senses_black()"
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def left_forwards_until_third_senses_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_third_senses_white()"
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def left_backwards_until_third_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_third_senses_black()"
    m.av(c.LEFT_MOTOR, -c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def left_backwards_until_third_senses_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_third_senses_white()"
    m.av(c.LEFT_MOTOR, -c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def right_forwards_until_third_senses_black(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_third_senses_black()"
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def right_forwards_until_third_senses_white(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting left_forwards_until_third_senses_white()"
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def right_backwards_until_third_senses_black(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting right_backwards_until_third_senses_black()"
    m.av(c.RIGHT_MOTOR, -c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def right_backwards_until_third_senses_white(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Left motor goes forwards until right tophat senses white
    print "Starting right_backwards_until_third_senses_white()"
    m.av(c.RIGHT_MOTOR, -c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def right_forwards_until_white(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
# Right motor goes forwards until right tophat senses white
    print "Starting right_forwards_until_white()"
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def right_forwards_until_white_safe(time = 1500, stop = True, starting_speed_right = c.NO_VALUE):
    print "Starting right_forwards_until_white_safe()"
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while u.not_bumped() and seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def left_point_turn_until_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting left_point_turn_until_black()"
    m.activate_motors(-1 * c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def left_point_turn_until_black_after(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting left_point_turn_until_black_after(" + str(time) + ")"
    m.activate_motors(-1 * c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    msleep(time)
    while NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def left_point_turn_until_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting left_point_turn_until_white()"
    m.activate_motors(-1 * c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def left_point_turn_until_right_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting left_point_turn_until_right_senses_black()"
    m.activate_motors(-1 * c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def left_point_turn_until_right_senses_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting left_point_turn_until_right_senses_white()"
    m.activate_motors(-1 * c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()
 

def right_point_turn_until_left_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting right_point_turn_until_left_senses_black()"
    m.activate_motors(c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def right_point_turn_until_left_senses_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting right_point_turn_until_left_senses_white()"
    m.activate_motors(c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def right_point_turn_until_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting right_point_turn_until_black()"
    m.activate_motors(c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def right_point_turn_until_black_after(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting right_point_turn_until_black_after(" + str(time) + ")"
    m.activate_motors(c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    msleep(time)  # Do a normal turn for "time" ms before checking for black
    while NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def right_point_turn_until_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting right_point_turn_until_white()"
    m.activate_motors(c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def right_forwards_until_left_senses_black(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
    print "Starting right_forwards_until_left_senses_black()"
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def right_forwards_until_left_senses_white(time = 10000, stop = True, starting_speed_right = c.NO_VALUE):
    print "Starting right_forwards_until_left_senses_white()"
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()


def left_forwards_until_right_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
    print "Starting left_forwards_until_right_senses_black()"
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def left_forwards_until_right_senses_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE):
    print "Starting left_forwards_until_right_senses_white()"
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()


def left_point_turn_until_third_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting left_point_turn_until_third_senses_black()"
    m.activate_motors(-1 * c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def right_point_turn_until_third_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting right_point_turn_until_third_senses_black()"
    m.activate_motors(c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def left_point_turn_until_third_senses_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting left_point_turn_until_third_senses_white()"
    m.activate_motors(-1 * c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackThird():
        pass
    if stop == True:
        m.deactivate_motors()


def right_point_turn_until_third_senses_white(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting right_point_turn_until_third_senses_white()"
    m.activate_motors(c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackThird():
        pass
    if stop == True:
        m.deactivate_motors()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Driving Align Functions~~~~~~~~~~~~~~~~~~~~~~~~

def snap_to_line_left():
    drive_through_line_third()
    left_point_turn_until_black()


def snap_to_line_right():
    drive_through_line_third()
    right_point_turn_until_black()


def drive_until_black_left(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_black_left()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()
    print "Line sensed, stopped driving\n"


def drive_until_black_right(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_black_right()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()
    print "Line sensed, stopped driving\n"


def drive_until_black_third(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_black_third()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        pass
    if stop == True:
        m.deactivate_motors()
    print "Line sensed, stopped driving\n"


def drive_until_black(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_black()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft() and NotBlackRight():
        pass
    if BlackLeft():
        sensor_on_black = c.LEFT_TOPHAT
    else:
        sensor_on_black = c.RIGHT_TOPHAT
    if stop == True:
        m.deactivate_motors()
    print "Line sensed, stopped driving\n"


def drive_until_both_black(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_both_black()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft() or NotBlackRight():
        pass
    if stop == True:
        m.deactivate_motors()
    print "Line sensed, stopped driving\n"


def drive_until_white_left(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_white_left()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def drive_until_white_right(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_white_right()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def drive_until_white_third(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_white_third()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackThird():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def drive_until_white(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_white()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft() and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def drive_until_both_white(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting drive_until_both_white()"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft() or BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def drive_through_line_left(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    drive_until_black_left(time, False, starting_speed_left, starting_speed_right)
    drive_until_white_left(time, stop, c.BASE_LM_POWER, c.BASE_RM_POWER)


def drive_through_line_right(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    drive_until_black_right(time, False, starting_speed_left, starting_speed_right)
    drive_until_white_right(time, stop, c.BASE_LM_POWER, c.BASE_RM_POWER)


def drive_through_line_third(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    drive_until_black_third(time, False, starting_speed_left, starting_speed_right)
    drive_until_white_third(time, stop, c.BASE_LM_POWER, c.BASE_RM_POWER)


def drive_through_two_lines_third(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):  # Drives without stopping the motors in between
    drive_until_black_third(time, False, starting_speed_left, starting_speed_right)
    drive_until_white_third(time, False, c.BASE_LM_POWER, c.BASE_RM_POWER)
    drive_until_black_third(time, False, c.BASE_LM_POWER, c.BASE_RM_POWER)
    drive_until_white_third(time, stop, c.BASE_LM_POWER, c.BASE_RM_POWER)


def backwards_until_black_left(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_black_left()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        pass        
    if stop == True:
        m.deactivate_motors()
    print "Line sensed, stopped driving\n"


def backwards_until_black_right(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_black_right()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        pass       
    if stop == True:
        m.deactivate_motors()
    print "Line sensed, stopped driving\n"


def backwards_until_black_third(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_black_third()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight() and NotBlackLeft():
        pass
    print "Line sensed, stopped driving\n"
    if stop == True:
        m.deactivate_motors()


def backwards_until_black_third_safe(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_black_third_safe()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while u.not_bumped() and seconds() < sec and NotBlackRight() and NotBlackLeft():
        pass
    print "Line sensed, stopped driving\n"
    if stop == True:
        m.deactivate_motors()


def backwards_until_white_left(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_white_left()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def backwards_until_white_right(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_white_right()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def backwards_until_white_third(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_white_third()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight() and BlackLeft():
        pass
    print "Line sensed, stopped driving\n"
    if stop == True:
        m.deactivate_motors()


def backwards_until_white(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_white()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight() and BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def backwards_until_both_white(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    print "Starting backwards_until_both_white()"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and BlackRight() or BlackLeft():
        pass
    if stop == True:
        m.deactivate_motors()
    print "White sensed, stopped driving\n"


def backwards_through_line_left(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE):
    backwards_until_black_left(time, False, starting_speed_left, starting_speed_right)
    backwards_until_white_left(time, stop, -1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER)


def backwards_through_two_lines_in_calibration(time = 1200):
    backwards_until_black_third(time, False, 0, 0)
    backwards_until_white_third(time, False, -1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER)
    if c.IS_CLONE_BOT:
        backwards_until_black_left(time, False, -1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER)
        # The need for this stems from a weird interaction. More testing is needed to discover the cause.
    backwards_until_white_left(time, False, -1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER)
    backwards_until_black_left(time, False, -1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER)
    backwards_until_white_left(time, True, -1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER)


def align_in_zone_safely():
    print "Starting align_in_zone_safely()"
    backwards_until_black_third_safe()
    align_far_safe()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Line Follow Functions~~~~~~~~~~~~~~~~~~~~~~~~

def lfollow_left(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the left tophat until time is reached.
    print "Starting lfollow_left()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if first_black and BlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = False
            first_white = True
        elif first_white and NotBlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_both_motors()


def lfollow_left_smooth(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the left tophat for time.
    print "Starting lfollow_left_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackLeft():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        else:
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_smooth_amount(time, left_speed = c.BASE_LM_POWER, right_speed = c.BASE_RM_POWER, left_smooth_speed = c.LFOLLOW_SMOOTH_LM_POWER, right_smooth_speed = c.LFOLLOW_SMOOTH_RM_POWER, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# IGNORE THIS, ALSO WORK ON THIS LATER
    print "Starting lfollow_left_smooth_amount()\n"
    m.activate_motors(left_speed, right_speed, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackLeft():
            mav(c.LEFT_MOTOR, left_speed)
            mav(c.RIGHT_MOTOR, right_smooth_speed)
        else:
            mav(c.LEFT_MOTOR, left_smooth_speed)
            mav(c.RIGHT_MOTOR, right_speed)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_until_right_senses_black(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the left tophat until right tophat senses black or time is reached.
    print "Starting lfollow_left_until_right_senses_black()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        if first_black and BlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = False
            first_white = True
        elif first_white and NotBlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_until_right_senses_black_smooth(time = 10000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the left tophat until right tophat senses black or time is reached.
    print "Starting lfollow_left_until_right_senses_black_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        if  NotBlackLeft():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        elif BlackLeft():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_inside_line(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the left tophat inside the line until time is reached.
    print "Starting lfollow_left_inside_line()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if first_black and BlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = False
            first_white = True
        elif first_white and NotBlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_inside_line_smooth(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the left tophat inside the line until time is reached.
    print "Starting lfollow_left_inside_line_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackLeft():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        else:
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_inside_line_until_right_senses_black(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the left tophat inside the line until the right tophat senses black or time is reached.
    print "Starting lfollow_left_inside_line_until_right_senses_black()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        if first_black and BlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = False
            first_white = True
        elif first_white and NotBlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_inside_line_until_right_senses_black_smooth(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the left tophat inside the line until the right tophat senses black or time is reached.
    print "Starting lfollow_left_inside_line_until_right_senses_black_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        if  NotBlackLeft():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        elif BlackLeft():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_both_motors()


def lfollow_left_inside_line_until_right_senses_black_smooth_amount(time = 20000, left_speed = c.BASE_LM_POWER, right_speed = c.BASE_RM_POWER, left_smooth_speed = c.LFOLLOW_SMOOTH_LM_POWER, right_smooth_speed = c.LFOLLOW_SMOOTH_RM_POWER, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# IGNORE THIS, ALSO WORK ON THIS LATER
    print "Starting lfollow_left_inside_line_until_right_senses_black_smooth_amount()\n"
    m.activate_motors(left_speed, right_speed, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        if  NotBlackLeft():
            mav(c.LEFT_MOTOR, left_speed)
            mav(c.RIGHT_MOTOR, right_smooth_speed)
        elif BlackLeft():
            mav(c.LEFT_MOTOR, left_smooth_speed)
            mav(c.RIGHT_MOTOR, right_speed)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_until_third_senses_black(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the left tophat until the third tophat senses black or the time is reached.
    print "Starting lfollow_left_until_third_senses_black()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        if first_black and BlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = False
            first_white = True
        elif first_white and NotBlackLeft():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_left_until_third_senses_black_smooth(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the left tophat until the third tophat senses black or the time is reached.
    print "Starting lfollow_left_until_third_senses_black_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        if  NotBlackLeft():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        elif BlackLeft():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the right tophat until time is reached.
    print "Starting lfollow_right()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if first_black and BlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = False
            first_white = True
        elif first_white and NotBlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_smooth(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the right tophat until time is reached.
    print "Starting lfollow_right_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackRight():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        elif NotBlackRight():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_until_left_senses_black(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the right tophat until left tophat senses black or time is reached.
    print "Starting lfollow_right_until_left_senses_black()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        if first_black and BlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = False
            first_white = True
        elif first_white and NotBlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_until_left_senses_black_smooth(time = 30000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):  # Must begin code while touching the line
# Line follow smoothly with the right tophat until left tophat senses black or time is reached.
    print "Starting lfollow_right_until_left_senses_black_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        if BlackRight():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        elif NotBlackRight():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_until_left_senses_black_smooth_amount(time, left_speed = c.BASE_LM_POWER, right_speed = c.BASE_RM_POWER, left_smooth_speed = c.LFOLLOW_SMOOTH_LM_POWER, right_smooth_speed = c.LFOLLOW_SMOOTH_RM_POWER, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):  # Must begin code while touching the line
# IGNORE THIS, ALSO WORK ON THIS LATER
    print "Starting lfollow_right_until_left_senses_black_smooth_amount()\n"
    m.activate_motors(left_speed, right_speed, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        if BlackRight():
            mav(c.LEFT_MOTOR, left_smooth_speed)
            mav(c.RIGHT_MOTOR, right_speed)
        elif NotBlackRight():
            mav(c.LEFT_MOTOR, left_speed)
            mav(c.RIGHT_MOTOR, right_smooth_speed)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_inside_line(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the right tophat inside the line until time is reached.
    print "Starting lfollow_right_inside_line()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if first_black and BlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = False
            first_white = True
        elif first_white and NotBlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_inside_line_smooth(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the right tophat inside the line until time is reached.
    print "Starting lfollow_right_inside_line_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackRight():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER )
        elif NotBlackRight():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER )
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_inside_line_until_left_senses_black(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the right tophat inside the line until the left tophat senses black or time is reached.
    print "Starting lfollow_right_inside_line_until_left_senses_black()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        if first_black and BlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = False
            first_white = True
        elif first_white and NotBlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_inside_line_until_left_senses_black_smooth(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the right tophat inside the line until the left tophat senses black or time is reached.
    print "Starting lfollow_right_inside_line_until_left_senses_black_smooth()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        if BlackRight():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        elif NotBlackRight():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_inside_line_until_left_senses_black_smooth_amount(time = 20000, left_speed = c.BASE_LM_POWER, right_speed = c.BASE_RM_POWER, left_smooth_speed = c.LFOLLOW_SMOOTH_LM_POWER, right_smooth_speed = c.LFOLLOW_SMOOTH_RM_POWER, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# IGNORE THIS, THIS IS A WORKING COMMAND BUT IS CONVALUTED.
    print "Starting lfollow_right_inside_line_until_left_senses_black_smooth_amount()\n"
    m.activate_motors(left_speed, right_speed, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        if BlackRight():
            mav(c.LEFT_MOTOR, left_speed)
            mav(c.RIGHT_MOTOR, right_smooth_speed)
        elif NotBlackRight():
            mav(c.LEFT_MOTOR, left_smooth_speed)
            mav(c.RIGHT_MOTOR, right_speed)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_until_third_senses_black(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow with the right tophat until the third tophat senses black or time is reached.
    print "Starting lfollow_right_until_third_senses_black()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        if first_black and BlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER, starting_speed_right)
            first_black = False
            first_white = True
        elif first_white and NotBlackRight():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, c.BASE_LM_POWER, starting_speed_left)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_right_until_third_senses_black_smooth(time = 20000, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow smoothly with the right tophat until the third tophat senses black or time is reached.
    print "Starting lfollow_right_until_third_senses_black_smooth()\n"
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackThird():
        if BlackRight():
            mav(c.LEFT_MOTOR, c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        elif NotBlackRight():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.LFOLLOW_SMOOTH_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_backwards(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow backwards with the third tophat until time is reached.
    print "Starting lfollow_backwards()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if first_black and BlackThird():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER, starting_speed_right)
            first_black = False
            first_white = True
        elif first_white and NotBlackThird():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER, starting_speed_left)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_backwards_smooth(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow backwards smoothly with the third tophat until time is reached.
    print "Starting lfollow_backwards_smooth()\n"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackThird():
            mav(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, -1 * c.LFOLLOW_SMOOTH_RM_POWER)
        elif NotBlackThird():
            mav(c.LEFT_MOTOR, -1 * c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_both_motors()


def lfollow_backwards_inside_line(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow backwards with the third tophat inside the line until time is reached.
    print "Starting lfollow_backwards_inside_line()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if first_black and BlackThird():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER, starting_speed_left)
            first_black = False
            first_white = True
        elif first_white and NotBlackThird():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER, starting_speed_right)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_backwards_inside_line_smooth(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow backwards smoothly with the third tophat inside the line until time is reached.
    print "Starting lfollow_backwards_inside_line_smooth()\n"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackThird():
            mav(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, -1 * c.LFOLLOW_SMOOTH_RM_POWER)
        elif NotBlackThird():
            mav(c.LEFT_MOTOR, -1 * c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_backwards_inside_line_until_right_senses_black(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow backwards with the third tophat inside the line until the right tophat senses black or time is reached.
    print "Starting lfollow_backwards_inside_line_until_right_senses_black()\n"
    first_black = True
    first_white = True
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        if first_black and BlackThird():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER, starting_speed_left)
            first_black = False
            first_white = True
        elif first_white and NotBlackThird():
            mav(c.LEFT_MOTOR, 0)
            mav(c.RIGHT_MOTOR, 0)
            m.av(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER, starting_speed_right)
            first_black = True
            first_white = False
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_backwards_inside_line_until_right_senses_black_smooth(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow backwards smoothly with the third tophat inside the line until the right tophat senses black or time is reached.
    print "Starting lfollow_backwards_inside_line_until_right_senses_black_smooth()\n"
    m.activate_motors(-1 * c.BASE_LM_POWER, -1 * c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        if BlackThird():
            mav(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, -1 * c.LFOLLOW_SMOOTH_RM_POWER)
        elif NotBlackThird():
            mav(c.LEFT_MOTOR, -1 * c.LFOLLOW_SMOOTH_LM_POWER)
            mav(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def lfollow_both(time, stop = True, starting_speed_left = c.NO_VALUE, starting_speed_right = c.NO_VALUE, refresh_rate = c.LFOLLOW_REFRESH_RATE):
# Line follow using both tophats until time is reached.
    print "Starting lfollow_both()\n"
    m.activate_motors(c.BASE_LM_POWER, c.BASE_RM_POWER, starting_speed_left, starting_speed_right)
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        if BlackRight() and BlackLeft():
            m.drive_no_print(30)
        elif BlackRight() and NotBlackLeft():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
        elif NotBlackRight() and BlackLeft():
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        elif NotBlackRight and NotBlackRight():
            mav(c.LEFT_MOTOR, c.BASE_LM_POWER)
            mav(c.RIGHT_MOTOR, c.BASE_RM_POWER)
        msleep(refresh_rate)
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_right(time, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.RIGHT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_RIGHT) / (c.MAX_TOPHAT_VALUE_RIGHT - c.MIN_TOPHAT_VALUE_RIGHT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        norm_reading = 100.0 * (analog(c.RIGHT_TOPHAT) - c.MIN_TOPHAT_VALUE_RIGHT) / (c.MAX_TOPHAT_VALUE_RIGHT - c.MIN_TOPHAT_VALUE_RIGHT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_RIGHT: " + str(c.MAX_TOPHAT_VALUE_RIGHT)
            print "c.MIN_TOPHAT_VALUE_RIGHT: " + str(c.MIN_TOPHAT_VALUE_RIGHT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        first_run_through = False
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_right_value_testing(time, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.RIGHT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_RIGHT) / (c.MAX_TOPHAT_VALUE_RIGHT - c.MIN_TOPHAT_VALUE_RIGHT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        norm_reading = 100.0 * (analog(c.RIGHT_TOPHAT) - c.MIN_VALUE_RIGHT) / (c.MAX_VALUE_RIGHT - c.MIN_VALUE_RIGHT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_RIGHT: " + str(c.MAX_TOPHAT_VALUE_RIGHT)
            print "c.MIN_TOPHAT_VALUE_RIGHT: " + str(c.MIN_TOPHAT_VALUE_RIGHT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        if u.right_pressed():
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_RIGHT: " + str(c.MAX_TOPHAT_VALUE_RIGHT)
            print "c.MIN_TOPHAT_VALUE_RIGHT: " + str(c.MIN_TOPHAT_VALUE_RIGHT)
            msleep(30)
        first_run_through = False
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_right_until_left_senses_black(time = 15000, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.RIGHT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_RIGHT) / (c.MAX_TOPHAT_VALUE_RIGHT - c.MIN_TOPHAT_VALUE_RIGHT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackLeft():
        norm_reading = 100.0 * (analog(c.RIGHT_TOPHAT) - c.MIN_VALUE_RIGHT) / (c.MAX_VALUE_RIGHT - c.MIN_VALUE_RIGHT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_RIGHT: " + str(c.MAX_TOPHAT_VALUE_RIGHT)
            print "c.MIN_TOPHAT_VALUE_RIGHT: " + str(c.MIN_TOPHAT_VALUE_RIGHT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        first_run_through = False
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_right_inside_line(time, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.RIGHT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_RIGHT) / (c.MAX_TOPHAT_VALUE_RIGHT - c.MIN_TOPHAT_VALUE_RIGHT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        norm_reading = 100.0 * (analog(c.RIGHT_TOPHAT) - c.MIN_TOPHAT_VALUE_RIGHT) / (c.MAX_TOPHAT_VALUE_RIGHT - c.MIN_TOPHAT_VALUE_RIGHT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_RIGHT: " + str(c.MAX_TOPHAT_VALUE_RIGHT)
            print "c.MIN_TOPHAT_VALUE_RIGHT: " + str(c.MIN_TOPHAT_VALUE_RIGHT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        first_run_through = False
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_left(time, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.LEFT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        norm_reading = 100.0 * (analog(c.LEFT_TOPHAT) - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_LEFT: " + str(c.MAX_TOPHAT_VALUE_LEFT)
            print "c.MIN_TOPHAT_VALUE_LEFT: " + str(c.MIN_TOPHAT_VALUE_LEFT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        first_run_through = False
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_left_value_testing(time, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.LEFT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        norm_reading = 100.0 * (analog(c.LEFT_TOPHAT) - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_LEFT: " + str(c.MAX_TOPHAT_VALUE_LEFT)
            print "c.MIN_TOPHAT_VALUE_LEFT: " + str(c.MIN_TOPHAT_VALUE_LEFT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        if u.right_pressed():
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_RIGHT: " + str(c.MAX_TOPHAT_VALUE_RIGHT)
            print "c.MIN_TOPHAT_VALUE_RIGHT: " + str(c.MIN_TOPHAT_VALUE_RIGHT)
            msleep(30)
        first_run_through = False
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_left_until_right_senses_black(time = 15000, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.LEFT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec and NotBlackRight():
        norm_reading = 100.0 * (analog(c.LEFT_TOPHAT) - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER - ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_LEFT: " + str(c.MAX_TOPHAT_VALUE_LEFT)
            print "c.MIN_TOPHAT_VALUE_LEFT: " + str(c.MIN_TOPHAT_VALUE_LEFT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        first_run_through = False
    if stop == True:
        m.deactivate_motors()


def pid_lfollow_left_inside_line(time, kp = c.KP, ki = c.KI, kd = c.KD, stop = True):
    first_run_through = True
    target = 100.0 * (c.LEFT_TOPHAT_BW - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
    base_power_left = c.BASE_LM_POWER
    base_power_right = c.BASE_RM_POWER
    last_error = 0
    integral = 0
    sec = seconds() + time / 1000.0
    while seconds() < sec:
        norm_reading = 100.0 * (analog(c.LEFT_TOPHAT) - c.MIN_TOPHAT_VALUE_LEFT) / (c.MAX_TOPHAT_VALUE_LEFT - c.MIN_TOPHAT_VALUE_LEFT)
        error = target - norm_reading  # Positive error means white, negative means black.
        derivative = error - last_error  # If rate of change is going negative, need to veer left
        last_error = error
        integral = 0.5 * integral + error  
        left_power = c.BASE_LM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))
        right_power = c.BASE_RM_POWER + ((kp * error) + (ki * integral) + (kd * derivative))  # Addition decreases power here
        if left_power > 1300:
            left_power = 1300
        elif left_power < -1000:
            left_power = -1000
        if right_power < -1300:
            right_power = -1300
        elif right_power > 1000:
            right_power = 1000
        if first_run_through == True:
            m.activate_motors(int(left_power), int(right_power))
            print "Norm reading: " + str(norm_reading)
            print "Error: " + str(error)
            print "Derivative: " + str(derivative)
            print "kd: " + str(kd)
            print "left_power: " + str(left_power)
            print "right_power: " + str(right_power)
            print "BASE_RM_POWER: " + str(c.BASE_RM_POWER)
            print "c.MAX_TOPHAT_VALUE_LEFT: " + str(c.MAX_TOPHAT_VALUE_LEFT)
            print "c.MIN_TOPHAT_VALUE_LEFT: " + str(c.MIN_TOPHAT_VALUE_LEFT)
        else:
            mav(c.LEFT_MOTOR, int(left_power))
            mav(c.RIGHT_MOTOR, int(right_power))
        first_run_through = False
    if stop == True:
        m.deactivate_motors()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Debug~~~~~~~~~~~~~~~~~~~~~~~~

def debug_right_tophat():
    if BlackRight():
        print "Right tophat senses black: " + str(analog(c.RIGHT_TOPHAT))
    elif NotBlackRight():
        print "Right tophat see white: " + str(analog(c.RIGHT_TOPHAT))
    else:
        print "Error in defining BlackRight and NotBlackRight"
        exit(86)


def debug_left_tophat():
    if BlackLeft():
        print "Left tophat senses black: " + str(analog(c.LEFT_TOPHAT))
    elif NotBlackLeft():
        print "Left tophat senses white: " + str(analog(c.LEFT_TOPHAT))
    else:
        print "Error in defining BlackLeft and NotBlackLeft"
        exit(86)
