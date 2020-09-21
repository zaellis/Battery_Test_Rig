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
from scipy import interpolate
import numpy as np

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
    q = data['capacity'][end_d] - data['capacity'][start_d]
    q_c = data['capacity'][end_c] - data['capacity'][start_c]
    coulomb_eff = q / q_c
    static_100 = (data['voltage'][start_d] - data['voltage'][start_d + 1]) / (-1 * data['current'][start_d + 1])
    static_0 = (data['voltage'][start_c] - data['voltage'][start_c + 1]) / data['current'][start_c + 1]

    for i in range(start_d, end_d + 1):
        SOC_d.append(((q - (data['capacity'][i] - data['capacity'][start_d])) / q) * 100)
        OCV_d.append(data['voltage'][i])
        curr_d.append(-1 * data['current'][i])

    for i in range(start_c, end_c + 1):
        SOC_c.append(((data['capacity'][i] - data['capacity'][start_c]) / q_c) * 100)
        OCV_c.append(data['voltage'][i])
        curr_c.append(data['current'][i])

    top_OCV = interpolate.interp1d(SOC_d, OCV_d)
    top_current = interpolate.interp1d(SOC_d, curr_d)
    bottom_OCV = interpolate.interp1d(SOC_c, OCV_c)
    bottom_current = interpolate.interp1d(SOC_c, curr_c)
    OCV_50 = ((top_OCV(50) * bottom_current(50)) + (bottom_OCV(50) * top_current(50))) / (top_current(50) + bottom_current(50))
    slope_d = (((OCV_50 - top_OCV(50)) / top_current(50)) - static_100)/ 50
    slope_c = (((bottom_OCV(50) - OCV_50) / bottom_current(50)) - static_0)/ 50

    for i in range(0,500):
        SOC.append(i/ 10)
        OCV.append(bottom_OCV(i / 10) - (((slope_c * (i / 10)) + static_0) * bottom_current(i / 10)))

    for i in range(500,1001):
        SOC.append(i / 10)
        OCV.append(top_OCV(i/10) + (((slope_d * (100 - (i/10))) + static_100) * top_current(i/10)))

    '''
    plt.plot(SOC, OCV)
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

    for x in starts, finishes:
        

    pass

if __name__ == '__main__':
    batt_data_raw = dict()
    batt_data_raw['capacity'] = []
    batt_data_raw['voltage'] = []
    batt_data_raw['current'] = []
    with open('VTC6 RPT.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            batt_data_raw['capacity'].append(float(row['capacity']))
            batt_data_raw['voltage'].append(float(row['voltage']) / 1000)
            batt_data_raw['current'].append(float(row['current']) / 1000)
    [SOCvOCV, q, coulomb_eff] = extract_OCV(batt_data_raw,15081,18367,2319,13917)
    print("Cell capacity {:.2f}mAh".format(q))
    print(SOCvOCV[1][1000])