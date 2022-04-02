

from copy import copy, deepcopy
from logging import NullHandler
from threading import local
from numpy import positive
import pandas as pd
from collections import deque


goal_pos = [2,4],[2,5]
EMPTY_SPACE = '.'
solved = False


def welcome():
 print(" _____           _       _    _                     _____                      ")
 print("|  __ \         | |     | |  | |                   / ____|                     ")
 print("| |__) |   _ ___| |__   | |__| | ___  _   _ _ __  | |  __  __ _ _ __ ___   ___ ")
 print("|  _  / | | / __| '_  \ |  __  |/ _ \| | | | '__| | | |_ |/ _` | '_ ` _ \ / _ \ ")
 print("| | \ \ |_| \__ \ | | | | |  | | (_) | |_| | |    | |__| | (_| | | | | | |  __/")
 print("|_|  \_\__,_|___/_| |_| |_|  |_|\___/ \__,_|_|     \_____|\__,_|_| |_| |_|\___| ")
 print("\n")
 print("Welcome!")
                                                                                

def get_solutions(lines):
    sols = []
    phrase = 'Sol:'
    end = '.' 
    lineNum = 0        
    for line in lines:                              #reads each line
        if phrase in line:                          #if 'Sol:' appears in a line the algo will preform some steps to append the solution to a list
            sol = line
            loopCount = 1
            while end not in sol:
                nex = lines[lineNum + loopCount]
                new = sol + nex
                sol = new
                loopCount +=1
            arrsol = sol.split()
            del arrsol[0]
            del arrsol[(len(arrsol)-1)]
            sols.append(arrsol)
        lineNum += 1
    return sols


def structure_boards(boards):
    arrs = []
    arr = []
    for board in boards:
        row = []
        for letter in board:
            row.append(letter)
            if len(row) == 6:
                arr.append(row)
                row = []
        arrs.append(arr) 
        arr = []
    return arrs


def board_format(board):
    return '\n'.join(''.join(_) for _ in board)


def visual_board(board):
    print(" 0 1 2 3 4 5")
    print("+-----------+")
    print(" ", end="")
    print(*board_format(board))
    print("+-----------+")


def check_right(board, pos):
    if pos[1] < 5:
        return board[pos[0]][pos[1] + 1]

def check_left(board, pos):
    if pos[1] > 0:
        return board[pos[0]][pos[1] - 1] 

def check_down(board, pos):
    if pos[0] < 5:
        return board[pos[0] + 1][pos[1]]

def check_up(board, pos):
    if pos[0] > 0:
        return board[pos[0] - 1][pos[1]] 

def find_vehicles(board):
    
    queue = deque([[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5]])
    vehicle_dict = {"Location":[],"Size":[],"Axis":[],"Letter":[]}
    
    while queue: 

        pos = queue.popleft()                                           #pop left from the queue (FIFO)
        if board[pos[0]][pos[1]] != '.':                                #only look and letters
            letter = board[pos[0]][pos[1]]
            size = 0
            direction= ''

            if pos[1] != 5:
                size2 = check_right(board, pos)
                if size2 == letter:                                               #Checks for a size 2 vehicles
                    size = 2
                    pos[1] += 1
                    queue.remove(pos)                                   #removes pos from queue to search
                    direction = 'h'
                    index = [[pos[0], pos[1]-1], [pos[0], pos[1]]]      #stores the location of found vehicle
                    size3 = check_right(board, pos)             #check if its a truck with the size of 3
                    
                    if size3 == letter:                                           #Checks for a size 3 vehicle s
                        size = 3
                        pos[1] += 1
                        queue.remove(pos)                               #removes from queue
                        index = [[pos[0], pos[1]-2], [pos[0], pos[1]-1], [pos[0], pos[1]]]
                    vehicle_dict["Location"].append(index)              #append locations, size, axis, and letter of the vehicle to a dictionary
                    vehicle_dict["Size"].append(size)
                    vehicle_dict["Axis"].append(direction)
                    vehicle_dict["Letter"].append(letter)
                    #print(letter + ": size " + str(size) + " direction: " + direction)

            if pos[0] != 5:
                size2 = check_down(board, pos)   
                if size2 == letter:                                               
                    size = 2
                    pos[0] += 1
                    queue.remove(pos)                                  
                    direction = 'v'
                    index = [[pos[0]-1, pos[1]], [pos[0], pos[1]]]      
                    size3 = check_down(board, pos)              
                    
                    if size3 == letter:
                        size = 3
                        pos[0] += 1
                        queue.remove(pos)
                        index = [[pos[0]-2, pos[1]], [pos[0]-1, pos[1]], [pos[0], pos[1]]]
                    vehicle_dict["Location"].append(index)
                    vehicle_dict["Size"].append(size)
                    vehicle_dict["Axis"].append(direction)
                    vehicle_dict["Letter"].append(letter)
                    #print(letter + ": size " + str(size) + " direction: " + direction)
    
    return vehicle_dict

def next_depth_board(board, letter, location, axis, size):
    #print(location)
    og_board = deepcopy(board)
    og_location = deepcopy(location)
    
    if axis == "up":
        old = location[-1]
        board[old[0]][old[1]] = "."
        new = location[0]
        board[new[0]-1][new[1]] = letter  
        #visual_board(board) 
        return board, og_board

    if axis == "down":
        old = location[0]
        board[old[0]][old[1]] = "."
        new = location[-1]
        board[new[0]+1][new[1]] = letter   
        #visual_board(board)
        return board, og_board



    if axis == "left":
        print("left shifting")

        old = location[-1]
        print(old)

        board[old[0]][old[1]] = "."
        new = location[0]
        board[new[0]][new[1]-1] = letter   
        print(location) 
        
        for i in range(size):
            location[i][1] -=1
        print(location)    
        visual_board(board)
        return board, og_board, location, og_location


    if axis == "right":
        print("right shifting")

        old = location[0]
        print(old)

        board[old[0]][old[1]] = "."
        new = location[-1]
        board[new[0]][new[1]+1] = letter   
        print(location) 
        
        for i in range(size):
            location[i][1] += 1
        print(location)    
        visual_board(board)
        return board, og_board, location, og_location



next_boards = []

def possible_moves(board, location, size, axis, letter, direction):     #recursion function to find possible moves vehicles can make
    og_board = deepcopy(board)
    og_location = deepcopy(location)
    if axis == 'v':
        #check up
        
        if direction == NullHandler or direction == "up":
            pos = [location[0][0], location[0][1]]
            up = check_up(og_board, pos)
            if up == ".":
                #print(location)
                next, og_board = next_depth_board(og_board, letter, og_location, "up", size)
                print(letter)
                next_boards.append(next)
                #print(next_boards)
                #visual_board(next)
                print("Move up possible")
                pos = location
                pos[0][0] -= 1 
                possible_moves(og_board, pos, size, axis, letter, "up")
         
                
        #check down     
        if direction == NullHandler or direction == "down":
            pos = [location[-1][0], location[-1][1]]
            down = check_down(og_board, pos)
            if down == '.':
                next, og_board = next_depth_board(og_board, letter, og_location, "down", size)
                next_boards.append(next)
                #visual_board(next)
                #visual_board(og_board)
                print(letter)
                print("Move down possible")
                pos = location
                pos[-1][0] += 1 
                possible_moves(og_board, pos, size, axis, letter, "down")

   
    elif axis == 'h':
        
        #check left
        if direction == NullHandler or direction == "left":
            pos = [location[0][0], location[0][1]]
            left = check_left(og_board, pos)
            if left == ".":
                next, og_board, location, og_location = next_depth_board(og_board, letter, og_location, "left", size)
                print(location)
                print(og_location)
                print(letter)
                print("Move left possible")
                possible_moves(next, location, size, axis, letter, "left")

        
        #check right
        if direction == NullHandler or direction == "right":
            pos = [location[-1][0], location[-1][1]]
            right = check_right(og_board, pos)
            print(pos)
            if right == '.':
                next, og_board, location, og_location = next_depth_board(og_board, letter, og_location, "right", size)
                print(letter)
                print("Move right possible")
                pos = location
                possible_moves(og_board, location, size, axis, letter, "right")



def bfs(start, end, boards, sols):
    
    for i in range(start, end):
        
        print('[' , i+1 , ']') 
        
        start_board = boards[i]
        vehicle_dict = dict()
        explored = deque()
        queue = deque()
        queue.append(start_board)
        
        visual_board(queue[0])
        print('Proposed Solution:' , end=' ')
        print(*sols[i], sep = ", ")
        print('\n')
        
        
        if queue:
            current = queue.popleft();
            if current[2][4] == 'X' and current[2][5] == 'X':
                solved = True
                print('Solved!')
            else:
                vehicle_dict = find_vehicles(current)               #Find the vehicles on the current board  
                num_of_veh = len(vehicle_dict['Location']) 

                #print(vehicle_dict)
                
                for i in range(0,num_of_veh):
                    loc = vehicle_dict['Location'][i]
                    size = vehicle_dict['Size'][i]
                    axis = vehicle_dict['Axis'][i]
                    letter = vehicle_dict['Letter'][i]

                    moves = possible_moves(current, loc, size, axis, letter, NullHandler)       #Find possible moves with board and vehicles

        else:       

            print("FAILED")
        print('\n')



def main():

    file = open('rh.txt', 'r')
    lines = file.readlines()
    boards = lines[4:44]
    b_sols = get_solutions(lines)
    s_boards = structure_boards(boards)
    options = ['BFS']

    welcome()

    #while True:
        #try:
           # print("Choose formula by typing it in: ")
            #print("Options:", end=" ")
           # for i in options:
            #    print(i, end=" ")
           # op = input("\n$ ")

           # if op not in options:
           #     print("Sorry, I didn't understand that ... ")
           #     continue

        #except ValueError:
        #    print("Sorry, I didn't understand that.")
            # try again, return to the start of loop
         #   continue
    
        #else:
        #    break

   # while True:
    #    try:
    #        print("Enter range of problems to analyse: ")
     #       start = int(input("Enter first value in range:\n$ "))
      #      end = int(input("Enter second value in range:\n$ "))
#
 #           if start < 0 or start > 40 or end < 0 or end > 40 or start == 39 or end == 0:
  #              print("Sorry, not valid ... ")
   #             continue
#
 #           if start > end:
  #              print("Sorry, value 1 cant be larger than value 2 ... ")
   #             continue
            
    #        if not isinstance(start, int) or not isinstance(end, int):
     #           print("Sorry, value 1 and/or 2 is not a number ... ")
      #          continue

       # except ValueError:
        #    print("Sorry, I didn't understand that.")
         #   continue
    
       # else:
       #     break
    
    
    #if op == 'BFS':
    start = 0
    end = 1

    bfs(start, end, s_boards, b_sols)


if __name__ == "__main__":
    main()


