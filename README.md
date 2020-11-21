# Battery_Test_Rig
Design documents and Auxiliary Scripts for Battery Cell Testing Rig

## Battery Parameters that can be Modelled as Demonstrated Here
- OCV: As a function of SOC and temperature
- Coulombic Efficiency: As a function of temperature
- Hysteresis: Instantaneous and dynamic
- Static Series Resistance: R0 term
- Dynamic Series Resistance: R1, R2, C1, C2 ... terms
## Generalized Description of Tests Performed to Generate Models
### OCV Tests

1. Soak cell at specified temperature and at fully charged voltage for 2 hours
2. Discharge at C/30 until Vmin is reached at specified temp
3. Soak at temp for 1 hour and check that cell is at Vmin
4. If not at Vmin, charge or discharge at C/30 until Vmin is reached
5. Repeat steps 2-4 except at C/30 charge and until Vmax is reached
### Coulombic Efficiency Tests

Comes from OCV Test data. Measures the amount of charge put into the battery vs. what was taken out to determine overall efficiency see [Math -> Determination of Coulombic Efficiency and Derivation of Equations](#determination-of-coulombic-efficiency-and-derivation-of-equations)

### Hysteresis tests

1. Discharge at C/30 from 100 - 0
2. Charge from 0 - 95
3. Discharge from 95-5
4. 5-90, 90-10, 10-85... 55-50
Data Can be analyzed to determine hysteresis characteristics of the cell when transitioning from charge to discharge and vice versa. See [Data Analysis](#data-analysis)

### Static and Dynamic Series Resistance

1. From 100% to 0% at points along the discharge curve discharge at 1C until voltage levels out and then let rest for an hour
2. Repeat along charge curve from 0% to 100% with charge at 1C and then rest  

Static resistance can be determined by examining the instantaneous voltage change when charging / discharging starts  
See [Data Analysis](#data-analysis) for determining dynamic components

## Math
### Determination of Coulombic Efficiency and Derivation of Equations

Coulombic efficiency is at its core a ratio between how much energy is put into a battery cell (charge), and how much can
be taken out (discharge). So at it's simplest the equation for coulombic efficiency is  
![equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7BEnergyDischarged%7D%7BEnergyCharged%7D*100%3DCoulombicEfficiency%28%25%29)  
What's important to consider however, is that measuring input and output energy is not always very easy. It is not the
measuring itself that is hard but knowing when to start and stop. In a battery cell there is a difference between total 
energy and total (usable) energy. For conventional lithium chemistries, there will be a minimum and maximum voltage operating range 
defined by the manufacturer (or you if you are the manufacturer) which outlines the optimal range of voltages to operate the battery cell 
at which result in an acceptable amount of degradation of the electrode materials over time. Technically there is still energy being stored in a cell 
in order to physically attain the minimum voltage potential and technically trying to cram more energy into a cell by overcharging is also possible. 
So, in its simplest form this equation holds true given that charge / discharge activity starts and stops at the correct points (times) 
defined by the manufacturer or defined by your use case which may be different. For example if you want to try to preserve the life of the cell 
even more by narrowing the charge / discharge window then energy measurements should be done in this window as well so your battery model best reflects 
its actual use. Something else to consider which is very important on its own, but otherwise related to the prior point, is the effects of temperature 
on your cell. Coulombic efficiency changes with temperature and so does the scaling between SOC and OCV, so in order to determine stopping points 
for fully charged / discharged in order to get coulombic efficiency at different temperatures, you need to set yourself up first at the temperature 
where these boundaries are defined (typically room temp 25 degrees C). The measurement sequence will usually follow these sequences.  
For Discharge:  
1. Get battery to predefined 100% SOC state at datasheet defined temp  
2. Soak cell at test temp knowing that it is at 100% SOC  
3. Discharge until predicted 0% SOC (voltage for 0% at predefined temp is usually a good guess) and take note of energy usage up to this point  
4. Bring back to predefined temp  
5. Finally charge / discharge to adjust to known 0% SOC at predefined temp and keep track of this energy usage separately  
  
For Charge:  
1. Get battery to predefined 0% SOC state at datasheet defined temp  
2. Soak cell at test temp knowing that it is at 0% SOC  
3. Charge until predicted 100% SOC (voltage for 100% at predefined temp is usually a good guess) and take note of energy usage up to this point  
4. Bring back to predefined temp  
5. Finally charge / discharge to adjust to known 100% SOC at predefined temp and keep track of this energy usage separately  
  
Having kept track of four different energies at this point a new equation can be used to find coulombic efficiency at any temp while only knowing the 
charge / discharge batteries for one predefined temp.  
![equation](https://latex.codecogs.com/gif.latex?%28%5Cfrac%7BEnergyDischargedTotal%7D%7BEnergyChargedTestTemp%7D%20-%20%28CoulombicEfficiencyRoomTemp%28decimal%29*%5Cfrac%7BEnergyChargedRoomTemp%7D%7BEnergyChargedTestTemp%7D%29%29*100%3DCoulombicEfficiency%28%25%29)  
Where the offsets created by needing to normalize at room temp can be eliminated.
### Creating a Mathematical Model of a Battery Cell from the Measured Parameters
DOCUMENTATION WORK IN PROGRESS
## Data Analysis
DOCUMENTATION WORK IN PROGRESS  
  
---------------------------------------------------------------------------------------------------------------------
Copyright 2020 Zachary Ellis

Licensed under the Apache License, Version 2.0 (the "License");  
you may not use this file except in compliance with the License.  
You may obtain a copy of the License at  
  
   http://www.apache.org/licenses/LICENSE-2.0  
  
Unless required by applicable law or agreed to in writing, software  
distributed under the License is distributed on an "AS IS" BASIS,  
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and  
limitations under the License.  
