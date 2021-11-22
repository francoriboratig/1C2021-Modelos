import operator
import random
import time

#Processes a file and transforms it in a model that can be processed by the program
def process_file(file_name):

    file = open(file_name)

    piece_costs = {}
    piece_restrictions = {}
    
    for line in file:
        
        if line.split()[0] == "e":

            left_number = int(line.split()[1])
            right_number = int(line.split()[2])
            
            if left_number in piece_restrictions:
                if right_number not in piece_restrictions[left_number]: 
                    piece_restrictions[left_number] = piece_restrictions[left_number] + [right_number]
            else:
                piece_restrictions[left_number] = [right_number]

            if right_number in piece_restrictions:
                if left_number not in piece_restrictions[right_number]: 
                    piece_restrictions[right_number] = piece_restrictions[right_number] + [left_number]
            else:
                piece_restrictions[right_number] = [left_number]

        if line.split()[0] == "n":
            piece_costs[int(line.split()[1])] = int(line.split()[2])

    #If no restrictions were given for a piece, fill the restrictions with empty list

    for i in range(max(piece_costs.keys())):
        if i+1 not in piece_restrictions:
            piece_restrictions[i+1] = {}

    print("/////////////////////")
    print("File processor says: -Hey, I got this!")
    print("Costs")
    print(piece_costs)
    print("Restrictions")
    print(piece_restrictions)
    return piece_costs, piece_restrictions

#Processes the model generated and returns the solution using the method function provided
def evaluate_model(costs,restrictions,method):
    return method(costs,restrictions)

#Prints the solution to a .txt file with the propper 
def output_file(result):
    file = open("solution.txt", "w")

    returnable = []

    for i in range(len(result)):
        for j in result[i]:
            returnable.append([j,i+1])

    for x in returnable:
        file.write("" + str(x[0]) + " " + str(x[1]) + "\n")

#Rate the proposed solution for the problem
#It is assumed that the proposed solution is valid
def rate_solution(solution, costs):
    cost = 0

    for i in solution:
        bag_costs = []
        for j in i:
            bag_costs = bag_costs + [costs[j]]
        cost = cost + max(bag_costs)

    return cost

#All my algorythms are dependant on some randomness that I apply, since they rely on which piece of clothe they begin the bags with.
#So multiple attempts are necessary for searching the best solution.
#Timeout variable units is [seconds]
def multi_try_evaluation(costs,restrictions,method,timeout):
    best_cost = 99999999
    best_solution = []
    
    start_time = time.time()

    while time.time() < start_time + timeout:
        challenger_solution = evaluate_model(costs,restrictions,method)
        if rate_solution(challenger_solution,costs) < best_cost:
            best_cost = rate_solution(challenger_solution,costs)
            best_solution = challenger_solution
            output_file(challenger_solution)

    return best_solution

    
#/////////////Solvers////////////////////


        
#Trivial solving algorithm. Puts every piece on a sepparate laundy session
def trivial_method(costs,restrictions):
    result = []
    for x in costs:
        result.append((x,x))
    return result

#The idea of this method is to, grab the biggest cost cloth, and try to put all the other same cost clothes on the same wash.
#Then, it will try to get all the n-1 cost clothes in the same wash as the n cost clothe, being n the cost of the first cloth picked.
#Repeat until you can't get any more clothes in the same wash
def greedy_method(costs,restrictions,randomize=True):

    def shirt_fits_in_bag(shirt,bag,restrictions):
        result = True

        if len(set(bag).intersection(set(restrictions[shirt]))) != 0:
               result = False

        return result

    costs_list_sorted = list(costs.items())

    #Add some variance to the deterministic nature of this algorithm
    if randomize: random.shuffle(costs_list_sorted)
    
    costs_list_sorted.sort(key = lambda x: -x[1])
    print("///////////////////")
    print("Sorted clothes by cost")
    print(costs_list_sorted)
    #I have my clothes sorted decreasingly by wash cost

    result = []
    while len(costs_list_sorted) != 0:
        #I make a bag of clothes that are permitted together, since the list of clothes is sorted by cost, this is the most expensive bag
        bag = []
        for shirt in costs_list_sorted:
            #I check if I can put this clothing (shirt for short) in the same washing bag, if so, it goes in the bag.
            if shirt_fits_in_bag(shirt[0],bag,restrictions):
                bag.append(shirt[0])

        #Now I remove all clothes in clothes list that I already put in the bag
        costs_list_sorted = [i for i in costs_list_sorted if i[0] not in bag]
        result.append(bag)
    print("///////////////////")
    print("Greedy Algorithm says:")
    print("-Hey, I think this is the best option")
    print(result)

#    returnable = []

#    for i in range(len(result)):
#        for j in result[i]:
#            returnable.append([j,i+1])
    
    return result
    
#///////////////////////////////////////

#Main program
costs, restrictions = process_file("segundo_problema.txt")
solution = multi_try_evaluation(costs,restrictions,greedy_method,500)
print(rate_solution(solution,costs))
