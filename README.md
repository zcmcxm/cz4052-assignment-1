# CZ4052 Assignment 1

## Purpose of each file

`images`: store all the images in the report.<br>
`congestion_window_growth_comparison.py`: it belongs to Section 1 and compares the growth of window size of a TCP congestion control procedure with that of the standard TCP.<br>
`tcp_congestion_control_algos.py`: it stores the classes of all the TCP congestion control procedure explored (i.e. TCP, HSTCP, Scalable TCP, and CUBIC).<br>
`tcp_multiuser.py`: it belongs to Section 2 and simulates multi-user scenarios with TCP.<br>
`two_user_fairness.py`: it belongs to Section 1 and illustrates the fairness of a TCP congestion control procedure by simulating 2-user scenario.<br>

## Section 1 - Tuning AIMD Parameters

```
# test the fairness of a TCP congestion control procedure
# select a control procedure by specifying -t HSTCP/Scalable/CUBIC/TCP (case-insensitive)
python two_user_fairness.py -t scalable
```

```
# compare the growth of a TCP congestion control procedure with the standard TCP
# select a control procedure by specifying -t HSTCP/Scalable/CUBIC (case-insensitive)
python congestion_window_growth_comparison.py -t scalable
```

## Section 2 - Multi-user Experiments

```
# simulate multi-user scenario with the standard TCP
python tcp_multiuser.py
```
