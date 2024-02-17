"""
This Python script demonstrates the growth of the congration window size
of a dynamically chosen TCP and TCP in independent networks.
"""

import matplotlib.pyplot as plt
import numpy as np
import tcp_congestion_control_algos as tcp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', type=str, required=True, help='choose a type of TCP: HSTCP, ScalableTCP, or CUBIC')

args = parser.parse_args()

if str(args.type).lower() == 'hstcp':
    othertcp = tcp.HSTCP()
elif str(args.type).lower() == 'scalabletcp' or str(args.type).lower() == 'scalable':
    othertcp = tcp.ScalableTCP()
elif str(args.type).lower() == 'cubic':
    othertcp = tcp.CUBIC()
else:
    raise ValueError("Please choose a type of TCP from: HSTCP, ScalableTCP, or CUBIC!")

ITERATESMAX = 500
Capcity = 200

otherwin_values = np.zeros(ITERATESMAX)
regwin_values = np.zeros(ITERATESMAX)

othertcp = tcp.HSTCP()
regtcp = tcp.TCP()

for i in range(1, ITERATESMAX):
    # Another TCP Algo
    if otherwin_values[i - 1] < Capcity:
        # Additive increase phase
        otherwin_values[i] = othertcp.additiveIncrease()
    else:
        # Multiplicative decrease phase
        otherwin_values[i] = othertcp.multiplicativeDecrease()

    # TCP
    if regwin_values[i - 1] < Capcity:
        # Additive increase phase
        regwin_values[i] = regtcp.additiveIncrease()
    else:
        # Multiplicative decrease phase
        regwin_values[i] = regtcp.multiplicativeDecrease()


plt.plot(range(ITERATESMAX), otherwin_values, label=f'{args.type}_Window')
plt.plot(range(ITERATESMAX), regwin_values, label='Standard_TCP_Window')

# plot guiding line
plt.plot(range(ITERATESMAX), [Capcity for i in range(ITERATESMAX)], linestyle='--', label='Capacity')
plt.plot(range(ITERATESMAX), [Capcity / 2 for i in range(ITERATESMAX)], linestyle='--', label='Half capacity')

plt.xlabel('RTT')
plt.ylabel('Window Size')
plt.title('Window Size over RTT')
plt.legend()
plt.show()
