# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 10:48:15 2025

@author: Mohsen
"""

import helics as h
import matplotlib.pyplot as plt
import pandas as pd

period=1.0
offset=0.5


# Create Federate Info
fedinfo = h.helicsCreateFederateInfo()
h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")
#h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, 1.0)

h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_PERIOD, period)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_OFFSET, offset)

# Create Battery Federate
battery = h.helicsCreateCombinationFederate("Battery", fedinfo)

# Register Publications and Subscriptions
sub_charging = h.helicsFederateRegisterSubscription(battery, "charging", "")
pub_status = h.helicsFederateRegisterGlobalTypePublication(battery, "status", "double", "")

# Enter Execution Mode
h.helicsFederateEnterExecutingMode(battery)

# Data collection for plotting
requested_times = []  # To store requested times
granted_times = []  # To store granted times
subscribed_values = []
soc_values = []  # To store SOC values
status_value=0.0
charging_value=0.0
granted_time=0.00

# Simulation Loop
for t in range(0, 10):
    
    # Request time step    
    requested_time = round(granted_time,2) + period
    granted_time = h.helicsFederateRequestTime(battery, requested_time)
    
    # Get charging value from Charger    
    charging_value = 0.0
    if h.helicsInputIsUpdated(sub_charging):  # Check if a new value is available
       charging_value = h.helicsInputGetDouble(sub_charging)
    else:
       charging_value = 0.0  # Default to 0 if no update received       
    

    # Simulate battery status (e.g., state of charge)
    status_value = status_value + charging_value
    #status_value=charging_value
    h.helicsPublicationPublishDouble(pub_status, status_value)
    
    
    requested_times.append(requested_time)
    granted_times.append(granted_time)
    subscribed_values.append(charging_value)
    soc_values.append(status_value)

# Cleanup
h.helicsFederateDestroy(battery)

print(soc_values)
#Table

data = {
    "Request Time (s)": requested_times,
    "Grant Time (s)": granted_times,
    "Subscribed Value (kW)": subscribed_values,
    "SOC Value (kW)": soc_values,
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
plt.title("Battery Federate")


# Show the plots
plt.tight_layout()
plt.show()