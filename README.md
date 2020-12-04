# Battery_Test_Rig
Design documents and Auxiliary Scripts for Battery Cell Testing Rig.  
analysis.py can be used to derive some battery model components from test data but will is currently without a guide for use 
and is otherwise incomplete. However it can be useful to examine for how math is used to derive certain model componets and how to implement 
some of this math in code.  
MATLAB Corpses is a folder of legacy MATLAB code I have written as a precursor to this python version. It is even more poorly documented and unusable 
without modification but shows some of how MATLAB can be used to these purposes if you choose to decipher it.  

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

Comes from OCV Test data. Measures the amount of charge put into the battery vs. what was taken out to determine overall efficiency see [Math](#determination-of-coulombic-efficiency-and-derivation-of-equations)

### Hysteresis tests

1. Discharge at C/30 from 100 - 0
2. Charge from 0 - 95
3. Discharge from 95-5
4. 5-90, 90-10, 10-85... 55-50
Data Can be analyzed to determine hysteresis characteristics of the cell when transitioning from charge to discharge and vice versa. See [Data Analysis](#battery-hysteresis)

### Static and Dynamic Series Resistance

1. From 100% to 0% at points along the discharge curve discharge at 1C until voltage levels out and then let rest for an hour
2. Repeat along charge curve from 0% to 100% with charge at 1C and then rest  

Static resistance can be determined by examining the instantaneous voltage change when charging / discharging starts  
See [Data Analysis](#determining-static-and-dynamic-components-from-data) for determining dynamic components

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
![equation](https://latex.codecogs.com/gif.latex?%28%5Cfrac%7BDischarged_%7BTotal%7D%7D%7BCharged_%7BTestTemp%7D%7D%20-%20%28CoulombEff_%7BRoomTemp%7D*%5Cfrac%7BCharged_%7BRoomTemp%7D%7D%7BCharged_%7BTestTemp%7D%7D%29%29*100)  
Where the offsets created by needing to normalize at room temp can be eliminated.
### Creating a Mathematical Model of a Battery Cell from the Measured Parameters
WORK IN PROGRESS  
See slides by Prof. Gregory Plett for a more thorough explanation of this topic:  
[Battery Modeling Course Webpage](http://mocha-java.uccs.edu/ECE5710/index.html) [Slides on Equivalent Circuit Model](http://mocha-java.uccs.edu/ECE5710/ECE5710-Notes02.pdf)
## Data Analysis
### Determining Static and Dynamic Components from Data
Assuming an understanding of the ECM discussed (or at least linked to) in the prior section, we can now see how arbitrary inputs to that system
can help us in system identification. Ignoring the static series resistance and focusing on the RC branches, you can use the step response of the system to 
characterize its time constant or 1 / (R * C). The way this is done is by applying an arbitrary current step say at 1C until the voltage output of the cell mostly levels out. 
once the voltage is leveled out you can stop the load and watch as the voltage rises again (assuming the load was discharging the cell to begin with) back to some 
settling point. If you plot the voltage from the time the load is released to the settled time you will see a the characteristic response of the RC circuit. 
getting the time constant from this data can be done 1 of 2 ways: Simply by measuring the time it takes to settle and then dividing by 4 or 5 (it takes approximately 4-5 time
constants to charge or discharge a capacitor in an RC circuit) or use some sort of curve fitting tool to derive the time constant mathematically. Once the time constant is derived it needs to be 
split into the R and C components. This can be done Via Ohms law. Keeping track of the voltage right after the load is released V_load_release (not the settled value under load because the 
static resistance plays a part in this) and the voltage once the cell has settled V_no_load_settle, the resistance of the RC branch is (V_no_load_settle - V_load_release) 
/ Load_current where Load_current was the current you used for the step response. To find the static resistance a similar method is used except the voltage 
delta used is between V_load_settle (the voltage that the cell settles to under load) and V_load_release. Some good graphics for this can also be found on Dr. 
Gregory Plett's presentation on this same topic. [Presentation](http://mocha-java.uccs.edu/ECE5710/ECE5710-Notes02.pdf)
###Battery hysteresis
WORK IN PROGRESS: Trying to find the best way to automatically detect hysteresis of cells in code.  
  
A brief description of hysteresis band in Battery Cells: When examining SOC vs. OCV curves for cells measured at very low load, one might notice that there is 
a difference in the characteristic curve that the OCV follows based on whether the cell is charging or discharging. The gap between these two SOC vs. OCV curves 
is known as the hysteresis band. This band is important for battery modelling purposes because examining the very shallow region of SOC vs. OCV slope in the 
middle of the cell's SOC range, and the width of this band, encountering a cell for the first time and measuring a voltage of 
around nominal without knowing whether the cell was last in a charging or discharging state creates a large uncertainty in what the SOC actually is 
around these nominal values there can be on the order of 10s of percent uncertainty in what cell state of charge actually is. VISUAL COMING SOON BUT REVIEW ATTACHED 
PRESENTATION FOR AN INTRODUCTION TO THIS CONCEPT [Presentation](http://mocha-java.uccs.edu/ECE5710/ECE5710-Notes02.pdf). 
Keeping track of hysteresis dynamics helps a battery management system better estimate the cell SOC even after long periods of non-use and remove some 
of the uncertainty created by the combination of this band and the flat nature of the SOC vs. OCV curve at nominal values.

##Helpful References

Dr. Gregory Plett's courses on [Battery Modelling](http://mocha-java.uccs.edu/ECE5710/index.html) and [Battery Management](http://mocha-java.uccs.edu/ECE5720/index.html)  
[Battery University](https://batteryuniversity.com/)  
  
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
