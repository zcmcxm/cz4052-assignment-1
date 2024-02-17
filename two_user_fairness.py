import numpy as np
import matplotlib.pyplot as plt
import tcp_congestion_control_algos as tcp
import argparse

##########################
# customizable parameters
##########################

num_users = 2
initial_values = [10, 30] # initial values for each user
ITERATESMAX = 200
C = 100 # Capacity of the network

##########################
# end of customizable parameters
##########################

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', type=str, required=True, help='choose a type of TCP: HSTCP, ScalableTCP, or CUBIC')

args = parser.parse_args()

if str(args.type).lower() == 'hstcp':
    othertcp = tcp.HSTCP
elif str(args.type).lower() == 'scalabletcp' or str(args.type).lower() == 'scalable':
    othertcp = tcp.ScalableTCP
elif str(args.type).lower() == 'cubic':
    othertcp = tcp.CUBIC
else:
    raise ValueError("Please choose a type of TCP from: HSTCP, ScalableTCP, or CUBIC!")

x_values = np.zeros((num_users, ITERATESMAX))
users = []

for user_idx in range(num_users):
    x_values[user_idx, 0] = initial_values[user_idx]
    users.append(othertcp(initial_values[user_idx]))

for i in range(1, ITERATESMAX):
    if (np.sum(x_values[:, i - 1]) <= C):
        # additive increase phase
        for user_idx in range(num_users):
            if isinstance(users[user_idx], tcp.CUBIC):
                x_values[user_idx, i] = users[user_idx].additiveIncrease(i)
            else:
                x_values[user_idx, i] = users[user_idx].additiveIncrease()
    else:
        # multiplicative decrease phase
        for user_idx in range(num_users):
            if isinstance(users[user_idx], tcp.CUBIC):
                x_values[user_idx, i] = users[user_idx].multiplicativeDecrease(x_values[user_idx, i-1], i)
            else:
                x_values[user_idx, i] = users[user_idx].multiplicativeDecrease()
    
plt.plot(x_values[0], x_values[1], label='AIMD Iterates')

# plot fairness line
x_f = [i for i in range(C + 1)]
y_f = [i for i in range(C + 1)]
plt.plot(x_f, y_f, '--', label='fairness line')

# plot capcity line
x_c = [i for i in range(C + 1)]
y_c = [C - i for i in range(C + 1)]
plt.plot(x_c, y_c, color='red', label='capcity line')

plt.legend()

plt.xlabel("x1")
plt.ylabel("x2")
plt.show()