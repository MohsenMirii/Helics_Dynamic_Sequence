import helics as h
import random
import matplotlib.pyplot as plt
import pandas as pd


period=1.0
offset=0.0

# Create Federate Info
fedinfo = h.helicsCreateFederateInfo()
h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")
#h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, 1.0)

h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_PERIOD, period)
h.helicsFederateInfoSetTimeProperty(fedinfo, h.HELICS_PROPERTY_TIME_OFFSET, offset)

# Create Charger Federate
charger = h.helicsCreateCombinationFederate("Charger", fedinfo)

# Register Publications and Subscriptions
pub_charging = h.helicsFederateRegisterGlobalTypePublication(charger, "charging", "double", "")
sub_control = h.helicsFederateRegisterSubscription(charger, "control", "")

# Enter Execution Mode
h.helicsFederateEnterExecutingMode(charger)

# Data collection for plotting
requested_times = []  # To store requested times
granted_times = []  # To store granted times
published_values = []
subscribed_values = []
granted_time=0.00

# Simulation Loop
for t in range(0, 10):
    
    # Request time step
    requested_time = round(granted_time,2) + period
    granted_time = h.helicsFederateRequestTime(charger, requested_time)
    
    # Get control signal from Controller
    
    control_signal = 1.0
    if h.helicsInputIsValid(sub_control):  # Check if a new value is available
       control_signal = h.helicsInputGetDouble(sub_control)
    else:
       control_signal = 1.0  # Default to 0 if no update received       
    
    

    # Check control signal to decide whether to charge or not
    charging_value = random.uniform(10.0, 20.0)  # Random charging value
    if control_signal == 1.0:  # Continue charging
        h.helicsPublicationPublishDouble(pub_charging, charging_value)
    else:  # Stop charging
        charging_value = 0.0  # No charging
        h.helicsPublicationPublishDouble(pub_charging, charging_value)
    
    
    requested_times.append(requested_time)
    granted_times.append(granted_time)
    published_values.append(charging_value)
    subscribed_values.append(control_signal)
    


# Cleanup
h.helicsFederateDestroy(charger)

data = {
    "Request Time (s)": requested_times,
    "Grant Time (s)": granted_times,
    "Subscribed Value from Controller": subscribed_values,
    "Published Value (kW)": published_values,
    

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
plt.title("Charger Federate")


# Show the plots
plt.tight_layout()
plt.show()
