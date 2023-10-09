# [Cristian's Algorithm](https://en.wikipedia.org/wiki/Cristian%27s_algorithm)

The goal of this work is to apply distributed algorithms.

## Problem Description

In this practical assignment, you are required to implement Cristian's algorithm for physical clocks.

The distributed system should always have a device with the exact time, updated through the NTP protocol. This computer will be responsible for updating the other devices.

Cristian's algorithm should use estimates of RTT (Round Trip Time) to update the other clocks.

The change in time should be made gradually.

The synchronization algorithm should run periodically.

The network should have a minimum of 3 devices.
