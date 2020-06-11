# !/usr/bin/python
# -*- coding:utf-8 -*-
# Author: henry
# Created Time: 2020/6/11 13:35
# !/usr/bin/python
from matplotlib import pyplot as plt
import matplotlib
from matplotlib import ticker as mtick
import numpy as np
import pandas as pd
import re


class GenerateChart(object):

    def __init__(self):
        pass

    # Retention report
    def generate_chart(self, file_path="./3A.xlsx"):

        file_data = pd.read_excel(file_path, encoding='utf8')

        floor, num1, num2, num3, num4 = [], [], [], [], []

        file_data = list(np.array(file_data))
        for row_index in range(0, len(file_data)):
            temp_data = list(file_data[row_index])
            if int(temp_data[0]) not in floor:
                floor.append(int(temp_data[0]))
            number = str(int(temp_data[1]))
            if number[-2:] == "01":
                num1.append(float(temp_data[2]))
            if number[-2:] == "02":
                num2.append(float(temp_data[2]))
            if number[-2:] == "03":
                num3.append(float(temp_data[2]))
            if number[-2:] == "04":
                num4.append(float(temp_data[2]))

        num1 += [40000 for i in range(len(floor) - len(num1))]
        num2 += [40000 for i in range(len(floor) - len(num2))]
        num3 += [40000 for i in range(len(floor) - len(num3))]
        num4 += [40000 for i in range(len(floor) - len(num4))]

        plt.figure(figsize=(13, 6))
        plt.plot(floor, num1, label='Num 1', linewidth=3, alpha=0.6,
                 color='#FF3D09', marker='o', markersize='6')
        plt.plot(floor, num2, label="Num 2", linewidth=3,
                 alpha=0.6, color="#E59D11", marker='o', markersize='6')
        plt.plot(floor, num3, label="Num 3", linewidth=3,
                 alpha=0.6, color="#A45E22", marker='o', markersize='6')
        plt.plot(floor, num4, label="Num 4", linewidth=3,
                 alpha=0.6, color="#456E33", marker='o', markersize='6')
        plt.yticks(np.arange(40000, 60000, 1000))
        plt.xticks(np.arange(1, 38, 1))

        plt.ylabel("price", fontsize=16, color="BLack")
        plt.grid(True, which='major', axis='y', linestyle='--')
        plt.title("Block A")
        plt.legend()
        #
        # save report
        plt.savefig("./Chart.png")
        plt.show()


if __name__ == "__main__":
    obj = GenerateChart()
    obj.generate_chart()
