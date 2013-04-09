import random
import math

# Rounds
months = 100000

input_model = {}
# users_to_track (it means, calls against Topsy service)
input_model[0] = [50, 300, 175]
#events_number_per_month (eventes = number of projects deployed)
input_model[1] = [1, 4, 2]
#event_duration (duration per day of each project)
input_model[2] = [3, 11, 4]


def array_to_file(filename, dataset, header = None):
    """
    """
    # Prepare file descriptor
    f_out = open(filename, "w")
    
    # Write headers
    for head in header:
        f_out.write("%s\t" % head)
    f_out.write("\n")
    
    # Write dataset
    for data in dataset:
        for entity in data:
            f_out.write("%s\t" % entity)
        f_out.write("\n")
        
    # Close file descriptor
    f_out.close()


def simulation_per_month_model(input_model):
    """ 
        Model to solve the problem 
    """    
    # Static model data
    cold_start_initial_users = 400
    cost_per_request = 0.01
    request_per_user = 4
    
    # Model
    
    # Select randomly input parameters
    events = random.triangular(input_model[1][0], input_model[1][1], input_model[1][2])
    
    # Calculate the cost
    cost = 0
    
    # For each event in the month
    for event in range(0, round(events)):
        event_duration = random.triangular(input_model[2][0], input_model[2][1], input_model[2][2])
        
        # For each day of the event
        for day in range(0, round(event_duration)):
            
            # Get users to track
            users_to_track = random.triangular(input_model[0][0], input_model[0][1], input_model[0][2])
            cost += event_duration * users_to_track * request_per_user * cost_per_request
        cost += cold_start_initial_users * request_per_user * cost_per_request
    return cost
    
# Ds to save final values to get stats (mean and dev)
data = []
for i in range(1, months):
    value = round(simulation_per_month_model(input_model))
    data.append((i,value))
    
# Save data to file
array_to_file("data/histogram.tsv", data, ("index", "cost"))


# Calculated mean and standard deviation
# mean
n = len(data)
summarize = 0
for value in data:
    summarize += value[1]
mean = summarize / n 

# standard deviation
deviation = 0
for value in data:
    deviation += pow((value[1] - mean), 2)
print("Mean: %f\tDS:%f" % (mean, math.sqrt((deviation * (1 / n)))))


# Calulate accumulated probability
values = []
for value in data:
    values.append(value[1])
    
# DS to operate
data = []
uniques = {}

# Sort values to calculate accumulated probability
values.sort()
acumulated = 0
for value in values:
    if value not in uniques:
        value_frecuency = values.count(value)
        acumulated += value_frecuency / n
        data.append((value, acumulated))
        uniques[value] =  True
        
# Save data to file
array_to_file("data/accumulated.tsv", data, ("cost", "probability"))



