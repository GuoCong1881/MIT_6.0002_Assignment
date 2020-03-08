###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    inFile = open(filename, 'r')
    data = {}
    for line in inFile:
        linedata = line.split(",")
        data[linedata[0]] = int(linedata[1].replace('\n',''))
    return data       
    inFile.close
allCows = load_cows('ps1_cow_data_2.txt')

# Problem 2  
def each_trip (cows, limit = 10):    
    #for each trip, select the cow with max weight based on the available limit
    #return: a tuple, first is a list of names of cows in one trip, the second is the list of cows left
    totalWeight = 0
    datacopy = cows.copy()
    translist = []
    leftlist = []
    while totalWeight <= limit and len(datacopy) > 0 :
        heavist = max(datacopy, key = datacopy.get)
        if datacopy[heavist] <= limit - totalWeight:
            translist.append(heavist)
            totalWeight += datacopy[heavist]
        else:
            leftlist.append(heavist)
        del datacopy[heavist]
        
    return (translist, leftlist)    

def tripPrint (i, trip, left):
    #to print the members of each trip and members left behind
    if i == 1:
        if len(trip) == 1:
            print ("cow in the 1 st trip is", trip)
        else:
            print ("cows in the 1 st trip are", trip)
    else:
        if len(trip) == 1:
            print ("cow in the", i, "th trip is: ", trip)
        else:
            print ("cows in the", i, "th trip are: ", trip)
    if len(left) > 0:
        print ("cows left are: ", left)
    else: 
        print ("All cows are transported")

def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    copydict = cows.copy()
    alltrip = []
    i = 0
    while len(copydict) > 0:
        trip, left = each_trip(copydict, limit)
        alltrip.append(trip)
        for cow in trip:
            del copydict[cow]
        i += 1
#        tripPrint(i, trip, copydict)
    return alltrip


    

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    leastTrip = len(cows)
    for partition in get_partitions(cows):
#        print(partition)
        if len(partition) <= leastTrip:
            point = 0
            for eachtrip in partition:
                tripWeight = 0
                for eachcow in eachtrip:
                    tripWeight += cows[eachcow]
    #            print ("the weight for this trip is", tripWeight)
                if tripWeight <= limit:
                    point += 1
                else:
    #                print("this trip is overweighted")
    #                print("the point is", point)
                    break
            if point == len(partition):
                leastTrip = point
                bestTrip = partition
        else:
            break
    return bestTrip



# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    startG = time.time()
    resultG = greedy_cow_transport(allCows)   
    endG = time.time()
    time_Greedy = endG-startG
    
    startBF = time.time()
    resultBF = brute_force_cow_transport(allCows)
    endBF = time.time()
    time_bruteforce = endBF-startBF 
    print(resultG)
    print(resultBF)
    return(time_Greedy, time_bruteforce)
#    return time_Greedy
compresult = compare_cow_transport_algorithms()
print(compresult)
