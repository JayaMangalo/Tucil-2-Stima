import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from myConvexHull import *

data = datasets.load_iris()

#create a DataFrame
df = pd.DataFrame(data.data, columns=data.feature_names)

df['Target'] = pd.DataFrame(data.target)

print(df)

plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title('Petal Width vs Petal Length')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[0,1]].values
    hull = CONVEXHULL(bucket) #bagian ini diganti dengan hasil implementasi

    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[1])
    
    for j in range(0,len(hull),2):
        x_values = [hull[j][0], hull[j+1][0]]
        y_values = [hull[j][1], hull[j+1][1]]
        plt.plot(x_values, y_values, colors[i]) 
plt.legend()

plt.show()


