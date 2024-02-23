import tcp_congestion_control_algos as tcp
import numpy as np
import matplotlib.pyplot as plt
import random



###################
# two-user scenario
###################
ITERATESMAX = 100
Capacity = 100
user_1 = tcp.TCP(10) # init window size = 10, alpha = 1, beta = 0.5
user_2 = tcp.TCP(30, alpha=1.2, beta=0.6) # init window size = 30, alpha = 1.2, beta = 0.6

window_size_values = np.zeros((2, ITERATESMAX))
window_size_values[0, 0] = 10
window_size_values[1, 0] = 30

for i in range(1, ITERATESMAX):
    # additive increase phase
    if sum(window_size_values[:, i - 1]) < Capacity:
        window_size_values[0, i] = user_1.additiveIncrease()
        window_size_values[1, i] = user_2.additiveIncrease()
    else: # multiplicative decrease phase
        window_size_values[0, i] = user_1.multiplicativeDecrease()
        window_size_values[1, i] = user_2.multiplicativeDecrease()

    
plt.plot(window_size_values[0], window_size_values[1], label='AIMD Iterates')
print(f"window size of user {1}: {window_size_values[0][-10:-1]}")
print(f"window size of user {2}: {window_size_values[1][-10:-1]}")

# plot fairness line
x_f = [i for i in range(Capacity + 1)]
y_f = [i for i in range(Capacity + 1)]
plt.plot(x_f, y_f, '--', label='fairness line')

# plot capcity line
x_c = [i for i in range(Capacity + 1)]
y_c = [Capacity - i for i in range(Capacity + 1)]
plt.plot(x_c, y_c, color='red', label='capcity line')

# plot converge line
x_e = [i for i in range(50)]
y_e = [1.5 * i for i in range(50)]
plt.plot(x_e, y_e, '--', label='converge line')

plt.legend()

plt.xlabel("User 1")
plt.ylabel("User 2")
plt.show()

###################
# five-user scenario
###################
ITERATESMAX = 100
Capacity = 100
user_number = 5 # change the following values according to the number of users
init_window_size = [30, 12, 6, 8, 15]
alphas = [1, 3, 2, 0.5, 6]
betas = [0.5, 0.5, 0.6, 0.5, 0.4]
users = []

window_size_values = np.zeros((user_number, ITERATESMAX))

for i in range(user_number):
    window_size_values[i, 0] = init_window_size[i]
    users.append(tcp.TCP(init_window=init_window_size[i], alpha=alphas[i], beta=betas[i]))

for i in range(1, ITERATESMAX):
    # additive increase phase
    if sum(window_size_values[:, i - 1]) < Capacity:
        for user_idx in range(user_number):
            window_size_values[user_idx, i] = users[user_idx].additiveIncrease()
    else: # multiplicative decrease phase
        for user_idx in range(user_number):
            window_size_values[user_idx, i] = users[user_idx].multiplicativeDecrease()

colors = plt.cm.turbo(np.linspace(0.1, 0.9, user_number)) # generating a gradient of colors for plotting
for user_idx in range(user_number):
    plt.plot(range(ITERATESMAX), window_size_values[user_idx], label=f'user {user_idx + 1}', color=colors[user_idx])
    # print final window sizes
    print(f"window size of user {user_idx+1}: {window_size_values[user_idx]}")


plt.legend()

plt.xlabel("time")
plt.ylabel("window size")
plt.show()

###################
# hundred-user scenario
###################
ITERATESMAX = 120
Capacity = 1000
user_number = 100 # change the following values according to the number of users
init_window_size = [random.randint(1, 20) for _ in range(user_number)]
alphas = []
betas = []
users = []
window_size_values = np.zeros((user_number, ITERATESMAX))

for i in range(user_number):
    beta = round(random.uniform(0.3, 0.7), 1)
    alpha = 2 * (1 - beta)
    alphas.append(alpha)
    betas.append(beta)

    window_size_values[i, 0] = init_window_size[i]
    users.append(tcp.TCP(init_window=init_window_size[i], alpha=alpha, beta=beta))

for i in range(1, ITERATESMAX):
    # additive increase phase
    if sum(window_size_values[:, i - 1]) < Capacity:
        for user_idx in range(user_number):
            window_size_values[user_idx, i] = users[user_idx].additiveIncrease()
    else: # multiplicative decrease phase
        for user_idx in range(user_number):
            window_size_values[user_idx, i] = users[user_idx].multiplicativeDecrease()

colors = plt.cm.turbo(np.linspace(0.1, 0.9, user_number))  # generating a gradient of colors for plotting
for user_idx in range(user_number):
    plt.plot(range(ITERATESMAX), window_size_values[user_idx], label=f'user {user_idx + 1}', color=colors[user_idx])
    # print final window sizes
    print(f"window size of user {user_idx+1}: {window_size_values[user_idx][-1]}")

plt.xlabel("time")
plt.ylabel("window size")
plt.show()