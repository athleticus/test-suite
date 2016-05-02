#!/usr/bin/env python3
# ##################################################################
#
#   CSSE1001/7030 - Assignment 1
#
#   Student Username: s4032681
#
#   Student Name: David Wells
#
###################################################################
"""
----------------------------------------------
MARKING:   

Total: 

Meeting comments: 

General comments:

----------------------------------------------
TEST RUN:


END TEST

"""
# 2.2.1 make an initial state:

def make_initial_state(supporters):
    return 'TA' * supporters + '__'


# 2.2.2 make a position string:
def make_position_string(state):
    """

    """
    res = []
    for i, c in enumerate(state):
        res.append(i % 10)
    return res

def make_position_string_working(length):
    return ('0123456789' * (length // 10 + 1))[:length]


# 2.2.3 number of differences:

def num_diffs(state):
    """Returns the sum of differences found left to right
    along the state string

    num_diffs(str) -> int
    """
    length = len(state)  #Then length variable for ease of understanding
    diffs = 0  # need diffs set to zero so that it can be added to as the loop identifies differences
    for i in range(length - 1):  #range is used over the length - 1 as the starting point is 0.
        if state[i] != state[i + 1]:
            diffs += 1  # the above if conditional is met then add 1 to the variable diffs.
    return diffs


# 2.2.4 position of blanks:

def postion_of_blanks(state):
    """Returns the index of the state string where the first
    blank is identified

    position_of_blanks(str) -> int
    """
    return state.find('_')


# 2.2.5 Make a move:

def mak_mov(state, pos):
    blanks = '__'  #for making the new state
    a = state.replace(state[state.find('_'):state.find('_') + 2], state[pos:pos + 2])  #replaces blanks with pos slice
    b = a[0:pos] + blanks + a[pos + 2::]  #remaking the state after a move from slices

    return b


# 2.2.6 Outputting the state information

def two_point_two_point_six(states):
    """Returns the current state string from a list of the past states generated from
    previous moves

    show_current_state([str]) -> str
    """
    current = states[-1]  #The last state in the list states
    return print(make_position_string_working(len(states[-1])) + '\n' + current, num_diffs(current), len(states) - 1)

show_current_state = two_point_two_point_six

# 2.2.7 Top level interface:

def interact():
    """Begins the game and continues until the solution to the puzzle is reached

    No input into the interact function as the game begins automatically
    """
    supporters = int(input('How many supporters from each team? '))  #intializations
    state = make_initial_state(supporters)
    length = len(state)
    states = [state]  #The list to append to
    while num_diffs(states[-1]) > 2:  #while loop due to unknown number of moves
        two_point_two_point_six(states)  #current state after each iteration
        state = states[-1]  #writes over state for make_move_function to work on current state
        pos = input('? ')
        if pos == 'b':
            states.remove(states[-1])  #removes the last state in list states
        elif pos == 'q':
            quit()
            return
        else:
            mak_mov(states[-1], int(pos))  #If while loop true and q and b not entered move is made
            states.append(mak_mov(states[-1], int(
                pos)))  #the move must be appended to the list states and while loop begins again
        #print("Input: " + pos)
    return print(states[-1] + "\n" + ' :-) Congratulations you have separated these green street hooligans !!!')

    pass


##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()
