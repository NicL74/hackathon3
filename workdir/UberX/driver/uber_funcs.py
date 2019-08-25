import numpy as np
import matplotlib.pyplot as plt
import time


def roads(*args):
    #
    # Usage: roads(block_map_array, block_size, lane_width, line_width, kerb_width,display_on)
    #
    # Can use with no paramters and defaults will be used, or just with block_map_array
    # Defaults are:
    #   block_size = 64
    #   lane_width = 12
    #   line_width = 2
    #   kerb_width = 3
    #
    # Define blocks, which are used to compose roads.
    # There are a small number of basic block types
    #
    # Define some parameters
    varargin = args
    nargin = len(varargin)
    #print('number of args into roads')
    #print(nargin)
    if(nargin==1): # assume default values
        block_map_array = args[0]
        block_size = 64
        lane_width = 12
        line_width = 2
        kerb_width = 3
        display_on = 1
    elif(nargin==0):
        # Default simple map
        block_map_array = np.array([(5, 4, 9, 6),\
                                    (3, 5, 2, 10),\
                                    (8, 10, 3, 3),\
                                    (1, 8, 11, 7)])
        block_size = 64
        lane_width = 12
        line_width = 2
        kerb_width = 3
        display_on = 0
        print('Default parameter values are being used')
    else:
        block_size = args[1]
        lane_width = args[2]
        line_width = args[3]
        kerb_width = args[4]
        display_on = args[5]

    display_on = 0 #hard code off for now

    #print(block_size)
    # Display the block map
    #print(block_map_array)
        
    blocks_y = np.size(block_map_array,0)
    blocks_x = np.size(block_map_array,1)

    # Define the block types in terms of how many lanes they have on each of
    # the N, E,S & W sides respectively
    
    block_types = ([ \
    (0, 0, 0, 0),\
    (2, 2, 2, 2),\
    (2, 0, 2, 0),\
    (0, 2, 0, 2),\
    (0, 2, 2, 0),\
    (0, 0, 2, 2),\
    (2, 0, 0, 2),\
    (2, 2, 0, 0),\
    (0, 2, 2, 2),\
    (2, 0, 2, 2),\
    (2, 2, 0, 2),\
    (2, 2, 2, 0)])

    num_block_types = np.size(block_types,0)
    # Define a 3-D space to store blocks
    # block_type_array = np.zeros(block_size,block_size,num_block_types)
    block_type_array_slice = np.zeros((block_size,block_size))

    # indexing with np.newaxis inserts a new 3rd dimension, which we then repeat the
    # array along, (you can achieve the same effect by indexing with None, see below)
    # Exmple: b = np.repeat(a[:, :, np.newaxis], 3, axis=2)
    block_type_array = np.repeat(block_type_array_slice[:, :, np.newaxis],num_block_types, axis=2)
    #print(np.shape(block_type_array))

    # Define some vertical heights for different surface components
    h_line = 2
    h_road = 3
    h_kerb = 1
    h_dirt = 0

    # Define some blocks
    # Start by defining a cross-section strip
    straight = np.zeros(block_size)
    road_width = kerb_width+lane_width+line_width+lane_width+kerb_width
    gap = np.round((block_size-road_width)/2)
    dirt = (h_dirt*np.ones((int(gap),1)))
    kerb = (h_kerb*np.ones((int(kerb_width),1)))
    road = (h_road*np.ones((int(lane_width),1)))
    line = (h_line*np.ones((int(line_width),1)))
    strip = np.vstack((dirt,kerb,road,line,road,kerb,dirt))
    #print(strip)
    #print(np.shape(strip))
    # Create a straight road block
    straight = np.kron(strip,np.ones((1,block_size)))
    #print(straight)
    block_type_array[:,:,3] = straight
    block_type_array[:,:,2] = np.transpose(straight)
    # Create an 4-way intersection block
    intersection = np.maximum(straight,np.transpose(straight))
    a = int(gap+kerb_width-line_width)
    b = int(block_size-gap-kerb_width+line_width)
    c = int(gap+kerb_width-line_width)
    d = int(block_size-gap-kerb_width+line_width)
    #print(a,b,c,d)
    e = int(gap+kerb_width)
    f = int(block_size-gap-kerb_width)
    g = int(gap+kerb_width)
    h = int(block_size-gap-kerb_width)
    #print(e,f,g,h)
    intersection[a:b,c:d] = h_line*np.ones((2*lane_width+3 * line_width))
    intersection[e:f,g:h] = h_road*np.ones((2*lane_width+line_width))
    block_type_array[:,:,1] = intersection
    # Create some corner blocks
    corner = np.zeros((block_size,block_size))
    inner_rad = 1+gap + kerb_width/2
    middle_rad = inner_rad + kerb_width/2 + lane_width + line_width/2
    outer_rad = middle_rad + line_width/2 + lane_width + line_width/2

    for i in range(0,block_size):
        for j in range(0,block_size):
            val = ((i+1)**2+(j+1)**2)**.5;
            if(val>(outer_rad+kerb_width/2)):
                corner[i,j] = h_dirt
            elif(np.abs(val-inner_rad)<kerb_width/2):
                corner[i,j] = h_kerb
            elif(np.abs(val-outer_rad)<kerb_width/2):
                corner[i,j] = h_kerb
            elif(np.abs(val-middle_rad)<line_width/2):
                corner[i,j] = h_line
            elif(val<(inner_rad+kerb_width/2)):
                corner[i,j] = h_dirt
            else:
                corner[i,j] = h_road

    block_type_array[:,:,6] = corner
    block_type_array[:,:,5] = np.flipud(corner)
    block_type_array[:,:,7] = np.fliplr(corner)
    block_type_array[:,:,4] = np.flipud(np.fliplr(corner))

    # Create some 3-way intersection blocks
    threeway = intersection
    threeway[0:int(gap+kerb_width+2*lane_width+line_width),:] = straight[0:int(gap+kerb_width+2*lane_width+line_width),:]
    block_type_array[:,:,8] = threeway
    block_type_array[:,:,9] = np.fliplr(np.transpose(threeway))
    block_type_array[:,:,10] = np.flipud(threeway)
    block_type_array[:,:,11] = np.transpose(threeway)    

    # Display all the block types
    if(display_on==1):
        fig = plt.figure()
        for xi in range(0,num_block_types):
            ax = fig.add_subplot(3,4,xi+1)
            plt.imshow(block_type_array[:,:,xi])
            plt.title('Block type: '+str(xi+1))

    # Assemble a map from the blocks
    mymap = np.zeros((block_size*blocks_y,block_size*blocks_x))  
    for i in range(1,blocks_x+1):
        for j in range(1,blocks_y+1):
            a = int(((j-1)*block_size))
            b = int(j*block_size)
            c = int(((i-1)*block_size))
            d = int(i*block_size)
            #print(i,j)
            e = int(block_map_array[j-1,i-1])-1
            mymap[a:b,c:d] = block_type_array[:,:,e];

    if(display_on==1):
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        plt.imshow(mymap)
        plt.title('Road map')
        plt.draw()

    roadmap = mymap;

    return (roadmap, block_types, block_size)


def satnav(*args):

    # Uses the roads function to create a map from input map_array
    #
    # Usage: (route_vector, distance, instructions, roadmap) = satnav(map_array,origin,destination,display_on)
    #
    # For a MxN block map array, we assume blocks are numbered from 1 to M*N in
    # left to right, top to bottom order
    #
    # The route vector is returned as a Px1 vector where each element represents 
    # a block according to the same numbering.
    # So the first element will be the origin and the last element will be the 
    # destination

    # Ref: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm 

    # Define some default parameters
    varargin = args
    nargin = len(varargin)
    #print(nargin)
    #print(args)
    if(nargin==0): # assume default values
        origin = 2
        destination = 8
        map_array = np.array([    \
            (5,4,4,4,6,5,4,6), \
            (8,6,5,6,8,10,1,3), \
            (5,7,3,3,5,7,5,10), \
            (8,4,10,3,3,5,10,3), \
            (5,6,3,12,2,2,10,3), \
            (3,12,11,7,3,3,12,10), \
            (3,3,5,4,2,2,7,3),  \
            (8,11,11,4,7,8,4,7)])
        display_on = 1
    elif(nargin==1): # map_array only passed
        map_array = args[0]
        origin = 2
        destination = 8
        display_on = 0
    elif(nargin==3): # map_array, origin and destination passed
        map_array = args[0]
        origin = args[1]
        destination = args[2]
        display_on = 0
    else:
        map_array = args[0]
        origin = args[1]
        destination = args[2]
        display_on = args[3]
        

    # Call the roads function to generate a roadmap
    #print(map_array)
    (roadmap,block_types,block_size) = roads(map_array)
    #print(roadmap)
    (y,x)=np.shape(map_array)
    (y_rm,x_rm) = np.shape(roadmap)
    # print(y,x,)
    #print(y_rm,x_rm)
    large_val = 2**16 # Used in distance array as a default large distance
    larger_val = large_val*2

    # May need to define and initialise some storage arrays (check later)
    route_vector = []
    instructions = {}
    distance_array = large_val * np.ones((y,x))
    
    # Define an array to store previously visited node
    previous_array = np.zeros((y,x))

    # Define an array to store status of whether node has been visited or not
    visited_array = np.zeros((y,x))
    
    # Identify the starting and ending blocks (using numbers starting at 0)
    # For origin = 8 and destination = 2 (and x=y=8), should yield:
    # y_orig = 0, x_orig = 7
    # y_dest = 0, x_dest = 1

    y_orig = np.ceil((origin/x))-1
    x_orig = ((origin-(x*(y_orig))))-1
    y_dest = np.ceil((destination/x))-1
    x_dest = ((destination-((x)*(y_dest))))-1
    # So these params are in python index space (0 to N)
    # print(y_orig,x_orig,y_dest,x_dest)
    
    # Set the distance to zero at start
    distance_array[int(y_orig),int(x_orig)] = 0

    x_curr = x_orig
    y_curr = y_orig
    current_node = ((y_curr)*x)+x_curr+1
    # print(current_node)

    last_direction=0
    change_in_direction=4 # Special value to denote start of journey

    # Run a loop until finished
    finished = 0;
    while(finished==0):

        # print(y_curr,x_curr)
        # print(current_node)
        # Starting at the origin, identify which neighbours are connected and update distances
        neighbour_array = np.zeros((3,3))
        my_dist = distance_array[int(y_curr),int(x_curr)]
        for i in range (0,3):
            for j in range (0,3):
                if(i==1 and j==1): # Itself, so not a neighbour
                    neighbour_array[j,i] = 0
                elif((x_curr+i<1) or (x_curr+i>x)): # i.e. at a vert boundary, so not valid neighbour
                    neighbour_array[j,i] = 0
                elif((y_curr+j<1) or (y_curr+j>y)): # i.e. at a horiz boundary, so not valid neighbour
                    neighbour_array[j,i] = 0
                else: # potentially valid neighbour
                    visited = visited_array[int(y_curr-1+j),int(x_curr-1+i)] # Check if visited
                    if(visited==0):
                        block_index = map_array[int(y_curr-1+j),int(x_curr-1+i)]
                        block_type = np.array((block_types[int(block_index-1)]))
                        # Check if has right kind of neighbour to create connection
                        if(( block_type[2]>0 and j==0 and i==1) or \
                            (block_type[0]>0 and j==2 and i==1) or \
                            (block_type[1]>0 and i==0 and j==1) or \
                            (block_type[3]>0 and i==2 and j==1)):
                            neighbour_array[j,i] = 1
                            current_dist = distance_array[int(y_curr-1+j),int(x_curr-1+i)]
                            if((my_dist+1)<current_dist):
                                distance_array[int(y_curr-1+j),int(x_curr-1+i)] = my_dist+1
                                previous_array[int(y_curr-1+j),int(x_curr-1+i)] = current_node
                    else:
                        neighbour_array[j,i] = 0

        # Mark that node as visited
        visited_array[int(y_orig),int(x_orig)] = 1

        # Choose next node to visit 

        # Calculate smallest tentative distance in set of unvisited nodes
        unvisited_distances = np.multiply(distance_array,(1-visited_array))
        # For visited nodes, leave them in but set distances to very large number so
        # not selected (dirty hack)
        unvisited_distances = unvisited_distances + visited_array*larger_val

        # Find the unvisited node with the smallest (or joint smallest) tentative distance
        # Matlab version: [Y,Iy] = min(unvisited_distances,[],1)
        Y = np.amin(unvisited_distances,axis=0)
        Iy = np.argmin(unvisited_distances,axis=0)

        # Matlab version: (min_dist,Ix) = min(Y,[],2)
        min_dist = np.amin(Y)
        Ix = np.argmin(Y)

        # Update the current x and y values
        x_curr = Ix
        y_curr = Iy[int(Ix)]

        # Update current_node to the new version
        current_node = ((y_curr)*x)+x_curr+1

        # Check if end condition reached
        if(((x_curr == x_dest) and (y_curr == y_dest)) or (min_dist==large_val)):
            finished = 1
            #print('Finished')
        else:
            finished = 0

        # Update visited_array
        visited_array[y_curr,x_curr]=1
        
        # Debug
        debug=0
        if(debug==1):
            print(distance_array)
            print(neighbour_array)
            print(visited_array)
            print(previous_array)

    #print('Hello')

    # Now route has been found, work back from the destination to describe the
    # route (using previous_array)
    route_vector = [destination]
    # print(route_vector)

    # Turn the array into a vector for ease of manipulation (left to right, then down)
    #temp = np.transpose(previous_array)
    previous_vect = np.concatenate(previous_array)
    # print(previous_vect)

    # Start at the destination and then work backwards to get the previous nodes
    index = destination-1
    prev = previous_vect[int(index)]
    if(prev==origin):
        route_vector = [[prev],[route_vector]]

    while(prev!=origin):
        prev = previous_vect[int(index)]
        route_vector = np.vstack((prev,route_vector)) #[[prev],[route_vector]]
        index = prev-1

    #print(route_vector)

    # Calculate the distance
    distance = distance_array[int(y_dest),int(x_dest)]
    #print('Distance = '+str(distance))

    # Describe the route
    route_block_vector = np.zeros((np.shape(route_vector)))

    # Display the route on the map
    highlight = 2;
    highlight_array = np.zeros((y_rm,x_rm))
    if(display_on):
        fig3 = plt.figure()
        ax3 = fig3.add_subplot(111)


    # Later we can insert the code for generating 'driver instructions' (from the Matlab original)
    # Calculate original 'direction of travel'
    directions = ['north','east','south','west','stop']

    for d in range (1,int(distance)+2): #2
        block = route_vector[d-1]
        #print('Block')
        #print('block = '+str(block))
        #print('x')
        #print(x)
        #print('d = ' +str(d))
        # Get location of block (in numbering starting at 1)
        block_y = np.ceil((block/x))
        block_x = block-(x*(block_y-1))
        # Get type of block
        #block_type = block_types[map_array[int(block_y),int(block_x)],:]
        block_type = np.array((block_types[int(block_index-1)]))
        # Look ahead one block to see what exit you need to take
        if(d<=distance):
            next_block = route_vector[d]; 
            #print('next_block ='+str(next_block))
            # Get location of next block
            next_block_y = np.ceil((next_block/x))
            next_block_x = next_block-(x*(next_block_y-1))
            if((next_block_y==block_y) and (next_block_x==(block_x+1))):
                direction = 2 # East (N, E, S, W = 1, 2, 3, 4)
            elif((next_block_y==block_y) and (next_block_x==(block_x-1))):
                direction = 4 # West
            elif((next_block_y==(block_y+1)) and (next_block_x==(block_x))):
                direction = 3 # South
            elif((next_block_y==(block_y-1)) and (next_block_x==(block_x))):
                direction = 1 # North
            else:
                direction = 5 # Stop
            #print('direction = '+str(direction))
            # Get change in direction
            if(d==1):
                change_in_direction=4 # Special value to denote start of journey
            else:
                change_in_direction = direction-last_direction

            # Values:
            # 0 = straight on
            # 1 = turn right
            # -1 = turn left
            # -3 = turn right
            # 3 = turn left
              
            # 2 = arrived at dest (special value)
            # 4 = starting off (special value)
                
            # Instructions for car
            # 10 = start
            # 11 = stop
            # 12 = continue (follow the road)
            # 13 = turn left
            # 14 = turn right
            # 15 = go straight over
              
        else:
            change_in_direction=2

        connections = np.sum((block_type>0))

        # switch connections (Matlab)
        if(connections==2):
            #case 2
            if(change_in_direction==2):
                message = ['You have arrived at your destination!']
                instructions = np.vstack((instructions, '11 direction'))
            elif(change_in_direction==4):
                message = ['Start off by driving '+str(directions[direction-1])]
                instructions = np.vstack((instructions, '10 direction'))
            else:
                message = ['Follow road ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '12 direction'))
            #case 3
        if(connections==3):
            if(change_in_direction==0):
                message = ['Follow road ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '12 direction'))
            elif((change_in_direction==1) or (change_in_direction==-3)):
                message = ['At the intersection, turn right to head ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '14 direction'))
            elif((change_in_direction==-1) or (change_in_direction==3)):
                message = ['At the intersection, turn left to head ' +str(directions[direction-1])]                
                instructions = np.vstack((instructions, '13 direction'))
            elif(change_in_direction==2):
                message = ['You have arrived at your destination!']
                instructions = np.vstack((instructions, '11 direction'))
            elif(change_in_direction==4):
                message = ['Start off by driving ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '10 direction'))
            else:
                print('Uh?')
                print('Change in direction =' + str(change_in_direction))
                print('connections = '+str(connections))
            #case 4
        if(connections==4):
            if(change_in_direction==0):
                message = ['At crossroads, continue straight ahead, going ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '15 direction'))
            elif((change_in_direction==1) or (change_in_direction==-3)):
                message = ['At the crossroads, turn right to head ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '14 direction'))
            elif((change_in_direction==-1) or (change_in_direction==3)):
                message = ['At the crossroads, turn left to head ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '13 direction'))
            elif(change_in_direction==2):
                message = ['You have arrived at your destination!']
                instructions = np.vstack((instructions, '11 direction'))
            elif(change_in_direction==4):
                message = ['Start off by driving ' +str(directions[direction-1])]
                instructions = np.vstack((instructions, '10 direction'))
            else:
                print('Uh?')
                print('Change in direction =' + str(change_in_direction))
                print('connections = '+str(connections))


        # Get coordinates of block
        #print(block_y,block_x)
        block_y_start = ((block_y-1)*block_size)
        block_y_end = block_y_start + block_size
        block_x_start = ((block_x-1)*block_size)
        block_x_end = block_x_start + block_size
        a = int(block_y_start)
        b = int(block_y_end)
        c = int(block_x_start)
        d = int(block_x_end)
        #print(a,b,c,d)
        highlight_array[a:b,c:d] = highlight_array[a:b,c:d] + highlight*np.ones((block_size))
        
        if(display_on==1):
            #fig3 = plt.figure()
            #ax3 = fig3.add_subplot(111)
            plt.imshow(roadmap+highlight_array)
            plt.draw()
            #plt.show()
            plt.pause(.01)
            

    return (route_vector, distance, instructions, roadmap)

def calc_distances(*args):
    # Usage (dist_list,block_locations,blocks_to_locs,bm_y,bm_x,num_valid_locs) =
    #   calc_distances(block_map_array,locations,route_locs)
    #
    # This function takes a road network map (defined by block_map_array)
    # and a set of locations (defined by locations) and generates a list
    # in format (loc,loc,dist) plus a dict of location_name:->block_number

    #an array,
    # called distance_array, filled with the distances between locations,
    # where x and y indices into the array represent locations
    #

    
    # Define some parameters
    varargin = args
    nargin = len(varargin)
    #print('nargin: '+str(nargin))
    if(nargin<2): # assume default values
        panic('Needs two arguments')
    elif(nargin==2):
        block_map_array = args[0]
        locations = args[1]
        num_locations = len(locations)
        route_locs = np.array((range(num_locations)))
        route_locs_set = 0
    else:
        block_map_array = args[0]
        locations = args[1]
        route_locs = args[2] # route_locs is list of location numbers relevant to this route
        route_locs_set = 1 # Create flag to say whether toute_loc has been specified

    #print(route_locs)
    num_locations = len(locations)
    #print(num_locations)
    #print(locations)

    # If route_locs_set, create ascending list of valid locs
    valid_locs=[]
    for loc in range(0,num_locations):
        found = (np.sum((route_locs == loc))>0)
        #print(str(loc)+' found? :'+str(found))
        if(found):
            valid_locs.append(1)
        else:
            valid_locs.append(0)
    # Convert to array
    valid_locs = np.array((valid_locs))
    num_valid_locs = np.sum(valid_locs)
    #print('valid_locs')
    #print(valid_locs)
    #print('num_valid_locs')
    #print(num_valid_locs)

    # Find the dimensions of block_map_array
    bm_y,bm_x = np.shape(block_map_array)
    #print('bm_y = '+str(bm_y))
    #print('bm_x = '+str(bm_x))

    # Create dict of:
    # location_name ("text") -> block_number (1 to bm_y*bm_x)
    # block_number (1 to bm_y*bm_x) -> location_number (0 to num_locations-1)
    block_locations={}
    blocks_to_locs={}
    for location in range(0,num_locations):
        block_x = int(locations[location][1])
        block_y = int(locations[location][2])
        block = ((block_y-1)*bm_x)+block_x
        block_locations.update({locations[location,0] : block})
        blocks_to_locs.update({block :location})
    #print(block_locations)
    #print(blocks_to_locs)


    # Convert  block number to x and y for each location
    #for location in range(0,num_locations):
        
    
    # Create the initial array
    dist_array = np.zeros((num_locations,num_locations))
    dist_list=[]

    # Populate the array with real distances, calculated using satnav
    # (only need to populate half the array due to symmetry)
    for i in range (0,num_locations):
        for j in range (i,num_locations):
            # origin is defined in terms of x,y, so need to convert from
            # block number to x,y
            origin_x = int(locations[i][1])
            origin_y = int(locations[i][2])
            #print(origin_x,origin_y)
            origin = ((origin_y-1)*bm_x)+origin_x
            #print(origin)
            destination_x = int(locations[j][1])
            destination_y = int(locations[j][2])
            #print(destination_x,destination_y)
            destination = ((destination_y-1)*bm_x)+destination_x
            #print(destination)
            #if(i!=j):
            # Only calculate for locations in route_locs 
            if((i!=j) and (valid_locs[i]==1 and valid_locs[j]==1)):  
                # satnav requires origin and destination to be defined in block numbers (not x,y)
                (route_vector, distance, instructions, roadmap) = satnav(block_map_array,origin,destination,0)
                dist_list.append([i,j,distance])
            else:
                distance = 0
            dist_array[j,i] = distance
            #print('Dist = ' +str(distance))

    #print(dist_list)
    
            
    
    return (dist_list,block_locations,blocks_to_locs,bm_y,bm_x,num_valid_locs)


