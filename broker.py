# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# broker.py
import helics as h
print("broker is runing")
broker = h.helicsCreateBroker("zmq", "broker", "--federates=3")
while h.helicsBrokerIsConnected(broker):
    
    pass  # Keep broker running

print("broker is stoped")
h.helicsBrokerFree(broker)
h.helicsCloseLibrary()
