# Battery_Test_Rig
Design documents and auxiliary scripts for battery cell testing rig

Battery Parameters that can be Modelled as Demonstrated Here
  OCV: As a function of SOC and temperature

  Coulombic Efficiency: As a function of temperature

  Hysteresis: Instantaneous and dynamic

  Static Series Resistance: R0 term

  Dynamic Series Resistance: R1 , R2 , C1 C2 terms

Generalized Description of Tests Performed to Generate Models

  OCV Tests:

    Soak cell at specified temperature and at fully charged voltage for 2 hours
    Discharge at C/30 until Vmin is reached at specified temp
    Soak at temp for 1 hour and check that cell is at Vmin
    If not at Vmin, charge or discharge at C/30 until Vmin is reached
    Repeat steps 2-4 except at C/30 charge and until Vmax is reached
  Coulombic Efficiency Tests:

    Comes from OCV Test data. Measures the amount of charge put into the battery vs. 
    what was taken out to determine overall efficiency see Math

`Hysteresis tests:

    Discharge at C/30 from 100 - 0
    Charge from 0 - 95
    Discharge from 95-5
    5-90, 90-10, 10-85... 55-50
    Data Can be analyzed to determine hysteresis characteristics of the cell when transitioning from charge to discharge and vice versa. See Data Analysis
  Static and Dynamic Series Resistance:

    From 100% to 0% at points along the discharge curve discharge at 1C and then let rest for an hour
    Repeat along charge curve from 0% to 100% with charge at 1C and then rest
    Static resistance can be determined by examining the instantaneous voltage change when charging / discharging starts
    See Data Analysis for determining dynamic components
