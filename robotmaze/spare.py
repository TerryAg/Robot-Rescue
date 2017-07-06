def main3():
    found = 0
    curr_node = 0
    speedX = speedY = 70
    nodes_exploring = []
    drive(speedX, speedY)
    while True:
        if is_can() and not found:
            found = 1 # This avoids repeatedly finding the can when we already have it.
            Sound.tone([(400, 1000, 200)])
            stop_motors()
            grab()
            turn_left(reset=False) # reset=False so we can turn accurately South
            turn_left()
            # then find best node path
        spin_results = sensor_turning()
        if len(spin_results) == 1:
            # Then go in that direction
            if spin_results[0] == mid:
                drive(*balance(speedX, speedY))
            elif spin_results[0] == left:
                stop_motors()
                turn_left()
            elif spin_results[0] == right:
                stop_motors() # clone from above
                turn_right()
        elif len(spin_results) == 2:
            if mid in spin_results:
                # So it's either mid/left or mid/right
                if left in spin_results: # mid/left
                    # Create a new node
                    stop_motors()
                    NODES[NODE_COUNT] = ["mid", "left"]
                    NODE_COUNT += 1
                    #nodes_exploring.append(NODE_COUNT) #the current node we're exploring
                    which_way = random.choice(["mid", "left"])
                    # we'll need which_way later when we del it from list.
                    if which_way == "left":
                        # Then turn left
                        turn_left()
                    else:
                        continue # go straight
                elif right in spin_results:
                    stop_motors()
                    # Create a new node
                    NODES[NODE_COUNT] = ["mid", "right"]
                    NODE_COUNT += 1
                    which_way = random.choice(["mid", "right"])
                    if which_way == "right":
                        turn_right()
                    else:
                        continue
                    
                    # Now turn right
            else:
                # Left and right
                # Create new node, go random first
                stop_motors()
                turn_left()
        elif len(spin_results) == 3:
            # crossroad
            pass
        else: # dead end?? end node go back
            stop_motors()
            turn_left()
            turn_left()
            paths = NODES[NODE_COUNT-1]
            del NODES[NODE_COUNT-1][paths.index(which_way)]
            # now go back to the first intersection met and go the other direction
            # go back to intersection, turn :
            # 180 if u went mid
            # right if u went righ
            # left if u went left
            # now you're facing north again. go the remaining paths.
            while len(sensor_turning()) < 2: # while only one direction to go in... WATCH TURNS.
                if spin_results[0] == mid:
                    drive(*balance(speedX, speedY))
                elif spin_results[0] == left:
                    stop_motors()
                    turn_left()
                elif spin_results[0] == right:
                    stop_motors() # clone from above
                    turn_right()
            stop_motors()
            if which_way == "left":
                turn_left()
            elif which_way == "right":
                turn_right() # MAKE A MORE SIMPLE TURN_RIGHT THAT DOES SAME AS TURN_LEFT
            elif which_way == "mid":
                turn_left()
                turn_left()
            if not paths: # still other options we haven't gone.
                if len(paths) == 1: # only one option to go
                    if paths == ["left"]:
                        turn_left()
                    elif paths == ["right"]:
                        turn_right()
                    elif paths == ["mid"]:
                        continue
                else: # two paths
                    #explore
                    pass

def main2():
    found = 0
    speedX = speedY = 70
    drive(speedX, speedY)
    while True:
        if is_can() and not found:
            found = 1 # This avoids repeatedly finding the can when we already have it.
            Sound.tone([(400, 1000, 200)])
            stop_motors()
            grab()
            turn_left(reset=False) # reset=False so we can turn accurately South
            turn_left()
        spin_results = sensor_turning()
        if len(spin_results) == 1:
            # Then go in that direction
            if spin_results[0] == mid:
                drive(*balance(speedX, speedY))
            elif spin_results[0] == left:
                stop_motors()
                turn_left()
            elif spin_results[0] == right:
                stop_motors() # clone from above
                turn_right()
        elif len(spin_results) >= 2:
            if mid in spin_results:
                # So it's either mid/left or mid/right
                if left in spin_results:
                    # Create a new node
                    new = Node(n_count, random.choice(["left", "mid"]), current_parent)
                    Node(current_parent)
                    current_parent = n_count
                    # Then turn left
                    stop_motors()
                    turn_left()
                elif right in spin_results:
                    # Create a new node
                    # Now turn right
                    stop_motors()
                    turn_right()
            else:
                # Left and right
                # Create new node, go left first
                stop_motors()
                turn_left()
        else: # dead end??
            stop_motors()
            turn_left()
            turn_left()