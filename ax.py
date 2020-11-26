import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
import xlrd

rb = xlrd.open_workbook('energy_characteristic/v110-2.0 MW.xls',formatting_info=True)
sheet = rb.sheet_by_index(0)

x, y = [], []
for rownum in range(2, sheet.nrows):
  x.append(round(sheet.row_values(rownum)[0], 2))
  y.append(round(sheet.row_values(rownum)[1], 2))

#print(x)
#print(y)

x = x
y = y
f = interpolate.interp1d(x, y)


xnew = np.arange(x[0], x[-1], 0.01)
ynew = f(xnew)
plt.plot(x, y, 'o', xnew, ynew, '-')
plt.show()

print(xnew)
print(ynew)



#x, y = [], []
#with open("g1.txt") as file:
#  for row in file:
#    x.append(float(row.split()[0]))
#    y.append(float(row.split()[1]))
