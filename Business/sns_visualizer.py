import numpy as np
import pandas as pd 
from scipy import stats, integrate  
import matplotlib.pyplot as plt 
import seaborn as sns 
import os
import math

os.chdir(os.path.dirname(__file__))
sns.set(color_codes=True)
excel_file = pd.ExcelFile('data.xlsx')
excel_sheet1 = excel_file.parse(excel_file.sheet_names[0])
exams = [excel_sheet1.iloc[:,0], excel_sheet1.iloc[:,1]]
confidence = float(input("Confidence score [%]: "))/100
for i in range(2):
    dist = exams[i]
    print("Currently reviewing dist " + str(i) + ": ")
    sample_size = (len(dist))
    mean = (np.mean(dist))
    standard_deviation = (np.std(dist))
    standard_error = standard_deviation / math.sqrt(sample_size)
    critical_number = stats.t.ppf(1-(1-confidence)/2, sample_size-1)
    margin_of_error = standard_error * critical_number

    print("Sample size: " + str(sample_size))
    print("Mean: " + str(mean))
    print("Standard deviation: " + str(standard_deviation))
    print("Confidence interval ({0}%): {1} ~{2}".format(confidence, mean, margin_of_error))


# x = []
# while True:
#     user_input = input("Enter new data point [# to stop]: ")
#     if (user_input == '#'):
#         break
#     try:
#         num = float(user_input)
#         x.append(num)
#     except:
#         pass 

# sns.distplot(x)
# sns.kdeplot(x, shade=True)
#plt.show()