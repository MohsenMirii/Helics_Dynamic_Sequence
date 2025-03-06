# Helics_Dynamic_Sequence
Helics for Dynamic Sequence (Runtime Adjustment)
Below is an example of a co-simulation using HELICS (Hierarchical Engine for Large-scale Infrastructure Co-Simulation) to demonstrate Dynamic Sequence (Runtime Adjustment) with three federates: Charger, Battery, and Controller. Each federate is implemented in a separate Python file.

**Scenario:** The Controller dynamically adjusts the charging process based on Battery status.

# Steps:
  1- **Broker** advances time and notifies federates.

  2- **Charger** sends charging current/voltage to the Battery.

  3- **Battery** updates its state and sends status (e.g., state of charge, temperature) to the Controller.

  4- **Controller** analyzes the Battery status and sends control signals (e.g., increase/decrease charging rate) to the Charger.

  5- **Broker** synchronizes and advances to the next time step.

# Visualization:
**Time Step 1:**
![Helics_Dynamic_Sequence](https://github.com/user-attachments/assets/ce183929-b345-4ae5-ae5c-3916165f318d)

**Time Step 2:**
![Helics_Dynamic_Sequence](https://github.com/user-attachments/assets/ce183929-b345-4ae5-ae5c-3916165f318d)

# Non-Blocking Communication:
The Controller sends control signals to the Charger asynchronously, allowing the Charger to continue its operation without waiting.

# Explanation of Dynamic Sequence:

  1- The Controller dynamically adjusts the charging process based on the Battery's status.

  2- If the battery status exceeds a threshold (e.g., 80.0), the Controller sends a control signal to stop charging.

  3- This demonstrates runtime adjustment and non-blocking communication (the Charger continues operating while the Controller dynamically intervenes).

#  Explanation of Period and Offset:
In order to manage the sequence in timing for three federates, We have considerated the period and offset for them:

**Period:** The period defines the time interval between consecutive executions of a federate.  
  In this example, all federates have a period of 1.0, meaning they execute every 1.0 time unit.

**Offset:** The offset defines the initial delay before a federate starts executing.
  In this example:
  **Charger:** Offset = 0.0 (starts immediately).

  **Battery:** Offset = 0.5 (starts after 0.5 time units).

  **Controller:** Offset = 0.25 (starts after 0.25 time units).

For running the Co-Simulation with CMD:
At first we have to install HELICS with this command:
  **pip install helics**

Then in seperated CMD we have to run these command:
 **1- cls && python broker.py**
 **2- cls && python charger.py**
 **3- cls && python battery.py**
 **4- cls && python controller.py**

# Then we see these tables which show the Data Transfer Flow:

 **Charger :**


![charger](https://github.com/user-attachments/assets/fb549141-41bf-4b77-8739-2b28b1a61415)

As you can see, the charger is  publishing the random value until get the control_signal equal to zero from the controller.

  **Battery**

  ![battery](https://github.com/user-attachments/assets/d5986260-a242-498f-b7cc-b0255f090d7d)

Here, in the battery, it subscribes the published values from the charger, It adds all the received values ​​together and publishes them each iteration so that the controller can receive them.

**Controller**


![Controller](https://github.com/user-attachments/assets/e5df5c8d-0d1d-4cff-9851-03b27acce680)

The controller subscribe the SOC from the Battery, and check it, if its bigger than 80.0 then publish zero to stop charger, otherwise publishes 1 flage.




