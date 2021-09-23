#Processes a file and transforms it in a model that can be processed by the program
def process_file(file_name):

    file = open(file_name)

    piece_costs = {}
    piece_restrictions = {}
    
    for line in file:
        
        if line.split()[0] == "e":
            if line.split()[1] in piece_restrictions:
                piece_restrictions[line.split()[1]] = piece_restrictions[line.split()[1]] + [line.split()[2]]
            else:
                piece_restrictions[line.split()[1]] = [line.split()[2]]
        if line.split()[0] == "n":
            piece_costs[line.split()[1]] = line.split()[2]

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
    for x in result:
        file.write("" + x[0] + ", " + x[1] + "\n")
        
#Trivial solving algorithm. Puts every piece on a sepparate laundy session
def trivial_method(costs,restrictions):
    result = []
    for x in costs:
        result.append((x,x))
    return result

#Main program

costs, restrictions = process_file("primer_problema.txt")
output_file(evaluate_model(costs,restrictions,trivial_method))
