# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 10:48:36 2025

@author: Mohsen
"""

import helics as h
import matplotlib.pyplot as plt
import pandas as pd


waitForCurrentTimeUpdate=True
period=1.0
offset=0.25

# Create Federate Info
fedinfo = h.helicsCreateFederateInfo()
h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")
h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, 1.0)
h.helicsFederateInfoSetFlagOption(fedinfo, h.helics_flag_wait_for_current_time_update, waitForCurrentTimeUpdate)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_PERIOD, period)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_OFFSET, offset)

# Create Controller Federate
controller = h.helicsCreateCombinationFederate("Controller", fedinfo)

# Register Publications and Subscriptions
sub_status = h.helicsFederateRegisterSubscription(controller, "status", "")
pub_control = h.helicsFederateRegisterGlobalTypePublication(controller, "control", "double", "")

# Enter Execution Mode
h.helicsFederateEnterExecutingMode(controller)

granted_time=0.00
requested_times = []  # To store requested times
granted_times = []  # To store granted times
published_values = []

# Simulation Loop
for t in range(0, 10):
    
    # Request time step
    requested_time = round(granted_time,2) + period
    granted_time = h.helicsFederateRequestTime(controller, requested_time)
    
    # Get battery status from Battery    
    status_value = 0.0
    if h.helicsInputIsUpdated(sub_status):  # Check if a new value is available
       status_value = h.helicsInputGetDouble(sub_status)
    else:
       status_value = 0.0  # Default to 0 if no update received       

    # Dynamic adjustment based on status
    if status_value > 80.0:  # Example condition
        control_signal = 0.0  # Stop charging
    else:
        control_signal = 1.0  # Continue charging

    # Send control signal to Charger
    h.helicsPublicationPublishDouble(pub_control, control_signal)
    
    requested_times.append(requested_time)
    granted_times.append(granted_time)
    published_values.append(control_signal)
    

# Cleanup
h.helicsFederateDestroy(controller)



data = {
    "Request Time (s)": requested_times,
    "Grant Time (s)": granted_times,
    "Subscribed Value (kW)": published_values,

}
df = pd.DataFrame(data)

# Plot the table using matplotlib
fig, ax = plt.subplots(figsize=(8, 4))  # Create a figure and axis
ax.axis('tight')  # Disable axis
ax.axis('off')  # Hide axes
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')  # Create the table

# Adjust table style
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Scale the table

# Show the table
plt.title("Controller Federate")


# Show the plots
plt.tight_layout()
plt.show()