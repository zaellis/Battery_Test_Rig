# Battery_Test_Rig
Design documents and Auxiliary Scripts for Battery Cell Testing Rig

## Battery Parameters that can be Modelled as Demonstrated Here
- OCV: As a function of SOC and temperature
- Coulombic Efficiency: As a function of temperature
- Hysteresis: Instantaneous and dynamic
- Static Series Resistance: R0 term
- Dynamic Series Resistance: R1 , R2 , C1 C2 terms
## Generalized Description of Tests Performed to Generate Models
### OCV Tests:

1. Soak cell at specified temperature and at fully charged voltage for 2 hours
2. Discharge at C/30 until Vmin is reached at specified temp
3. Soak at temp for 1 hour and check that cell is at Vmin
4. If not at Vmin, charge or discharge at C/30 until Vmin is reached
5. Repeat steps 2-4 except at C/30 charge and until Vmax is reached
### Coulombic Efficiency Tests:

Comes from OCV Test data. Measures the amount of charge put into the battery vs. what was taken out to determine overall efficiency see [Math](#math)

### Hysteresis tests:

1. Discharge at C/30 from 100 - 0
2. Charge from 0 - 95
3. Discharge from 95-5
4. 5-90, 90-10, 10-85... 55-50
Data Can be analyzed to determine hysteresis characteristics of the cell when transitioning from charge to discharge and vice versa. See [Data Analysis](#data-analysis)

### Static and Dynamic Series Resistance:

1. From 100% to 0% disat points along the discharge curve discharge at 1C and then let rest for an hour
2. Repeat along charge curve from 0% to 100% with charge at 1C and then rest  

Static resistance can be determined by examining the instantaneous voltage change when charging / discharging starts  
See [Data Analysis](#data-analysis) for determining dynamic components
