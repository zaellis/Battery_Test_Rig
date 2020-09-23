'''
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
'''

import csv
import math
import matplotlib.pyplot as plt
import scipy as sci
from scipy import interpolate, optimize
import numpy as np
import warnings

def extract_OCV(data, start_d, end_d, start_c, end_c):
    """
    Takes in raw data and returns tuple of SOC vs. OCV for given test range

    :param data:
    :param start_d:
    :param end_d:
    :param start_c:
    :param end_c:
    :return: [SOCvOCV, q, coulomb_eff]
    """

    SOC_d = []
    OCV_d = []
    curr_d = []
    SOC_c = []
    OCV_c = []
    curr_c = []
    SOC = []
    OCV = []
    q = data['capacity'][end_d] - data['capacity'][start_d]        #determine capacity
    q_c = data['capacity'][end_c] - data['capacity'][start_c]      #determine charge capacity
    coulomb_eff = q / q_c                                          #coulombic efficiency where discharge efficiency is assumed to be 1
    static_100 = (data['voltage'][start_d] - data['voltage'][start_d + 1]) / (-1 * data['current'][start_d + 1]) #estimated static resistance at 100% SOC
    static_0 = (data['voltage'][start_c + 1] - data['voltage'][start_c]) / data['current'][start_c + 1]          #estimated static resistance at 0% SOC

    for i in range(start_d, end_d + 1): #gather discharge curve data
        SOC_d.append(((q - (data['capacity'][i] - data['capacity'][start_d])) / q) * 100)
        OCV_d.append(data['voltage'][i])
        curr_d.append(-1 * data['current'][i])

    for i in range(start_c, end_c + 1): #gather charge curve data
        SOC_c.append(((data['capacity'][i] - data['capacity'][start_c]) / q_c) * 100)
        OCV_c.append(data['voltage'][i])
        curr_c.append(data['current'][i])

    top_OCV = interpolate.interp1d(SOC_d, OCV_d) #interpolation function make it easier to normalize scale in terms of SOC
    top_current = interpolate.interp1d(SOC_d, curr_d)
    bottom_OCV = interpolate.interp1d(SOC_c, OCV_c)
    bottom_current = interpolate.interp1d(SOC_c, curr_c)
    OCV_50 = ((top_OCV(50) * bottom_current(50)) + (bottom_OCV(50) * top_current(50))) / (top_current(50) + bottom_current(50)) #calculate OCV at 50% SOC via averaging
    slope_d = (((OCV_50 - top_OCV(50)) / top_current(50)) - static_100)/ 50 #simplified cell outpur resistance chage slope discharge
    slope_c = (((bottom_OCV(50) - OCV_50) / bottom_current(50)) - static_0)/ 50 #simplified cell outpur resistance chage slope charge

    for i in range(0,500): #extract normalized SOC from 0-49.9% at 0.1% intervals
        SOC.append(i/ 10)
        OCV.append(bottom_OCV(i / 10) - (((slope_c * (i / 10)) + static_0) * bottom_current(i / 10)))

    for i in range(500,1001): #extract normalized SOC from 50-100% at 0.1% intervals
        SOC.append(i / 10)
        OCV.append(top_OCV(i/10) + (((slope_d * (100 - (i/10))) + static_100) * top_current(i/10)))

    '''    
    plt.plot(SOC, OCV, SOC_d, OCV_d, SOC_c, OCV_c) #sanity plot
    plt.show()
    '''

    return [(SOC,OCV), q, coulomb_eff]

    pass

def extract_resistances(data, starts, finishes, SOCvOCV):
    """
    Extracts dynamic components and static resistances from dataset

    :param data:
    :param starts:
    :param finishes:
    :param SOCvOCV:
    :return: (SOC,R1,C1,R2,C2,R3)
    """
    f = interpolate.interp1d(SOCvOCV[0], SOCvOCV[1])
    SOC = []
    R1 = []
    C1 = []
    R2 = []
    C2 = []
    R3 = []

    for i in range(0,len(starts)):
        R1.append((data['voltage'][starts[i] + 1] - data['voltage'][starts[i]]) / (-1 * data['current'][starts[i]])) #calculating static resistance
        SOC.append(f(data['voltage'][finishes[i]]))              #determining SOC that data is taken at
        y = data['voltage'][(starts[i] + 1):finishes[i]]         #setting up voltage vs time graph
        t = data['test_time'][(starts[i] + 1):finishes[i]]
        delta_v = y[-1] - y[0]                                   #calculating normalizing values: voltage delta
        R23 = delta_v / (-1 * data['current'][starts[i]])        #: total dynamic resistance
        y_init = y[0]                                            #: offset voltage
        t_init = t[0]                                            #: time offset
        for j in range(0,len(y)):                                #function normalization
            t[j] -= t_init                                       #set t(0) to 0
            y[j] -= y_init                                       #remove voltage offset
            y[j] /= delta_v                                      #scale voltage delta to 1
        '''
        plt.plot(t,y) #sanity plot
        plt.show()
        '''
        param, param_cov = optimize.curve_fit(dynamic_fit, t, y) #curve fitting to 'dynamic_fit' function
        R2.append(R23 * param[0])                                #organizing parameters
        R3.append(R23 * param[2])                                #R2 and C1 come in pairs as well as R3 and C2 but the pairs are interchangeable
        C1.append(1 / (R2[-1] * param[1]))
        C2.append(1 / (R3[-1] * param[3]))

    return(SOC,R1,C1,R2,C2,R3)

    pass

def dynamic_fit(x, a, b, c, d): #battery dynamic model (normalized to 1)
    warnings.filterwarnings("ignore")
    return 1 - (a * np.exp(-b * x)) - (c * np.exp(-d * x))

if __name__ == '__main__':
    batt_data_raw = dict()
    batt_data_raw['capacity'] = []
    batt_data_raw['voltage'] = []
    batt_data_raw['current'] = []
    batt_data_raw['test_time'] = []
    with open('VTC6 RPT.csv') as csvfile: #gathering data from battery testing file
        reader = csv.DictReader(csvfile)
        for row in reader:
            batt_data_raw['capacity'].append(float(row['capacity']))
            batt_data_raw['voltage'].append(float(row['voltage']) / 1000)
            batt_data_raw['current'].append(float(row['current']) / 1000)
            batt_data_raw['test_time'].append(float(row['test_time']))
    [SOCvOCV, q, coulomb_eff] = extract_OCV(batt_data_raw,15081,18367,2319,13917) #Extracting SOC vs OCV data, capacity, and coulombic efficiency
    print("Cell capacity {:.2f}mAh".format(q))
    dynamics = extract_resistances(batt_data_raw, [33638, 37043], [34359, 37764], SOCvOCV) #Extracting static and dynamic resistances