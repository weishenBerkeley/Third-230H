from __future__ import division
import numpy as np
import scipy as sp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
import pandas as pd

def cal_per(c, B =100000):
    Total_pen = sum([c* B*(1.02**i)*(1.015**(44-i)) for i in range(45)])
    Last_pay = 0.7*B*1.02**44
    for t in range(18):
        Total_pen = Total_pen * 1.015
        Total_pen = Total_pen - Last_pay*0.99**t
    return Total_pen


def simulate(c, TPL,  B = 80000):
    Total_pen = c * B
    for t in range(1, 45):
        z = np.random.normal()
        Total_pen = Total_pen * np.exp((0.015 - 0.5* 0.06**2) + 0.06 * z) + c * B * (1.02**t)
    #Only considering end of year, after payment
    Last_pay = 0.7 * B * 1.02 ** 44
    if Total_pen / TPL < 0.8:
        return 0
    for t in range(17):
        TPL = TPL - Last_pay*0.99**t
        z = np.random.normal()
        Total_pen = Total_pen * np.exp((0.015 - 0.5* 0.06**2) + 0.06 * z) - Last_pay*0.99**t
        if Total_pen / TPL < 0.8:
            return t+1
    return -1


def main():
    B = 80000
    np.random.seed(0)
    r = fsolve(cal_per,0.1)
    print "The percentage rate is:" + str(r[0])
    Last_pay = 0.7 * B * 1.02**44
    TPL = sum([Last_pay*0.99**t for t in range(18)])
    prob = []
    N = 1000
    for i in range(N):
        prob.append(simulate(r[0], TPL))
    s = [np.sum(np.equal(prob,i))/N for i in range(-1,18)]
    print pd.DataFrame(s, index= range(-1,18))

if __name__ == "__main__":
    main()