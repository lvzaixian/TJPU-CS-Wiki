import matplotlib
matplotlib.use('TkAgg')
import pylab as plt
import xlrd
data= xlrd.open_workbook("data.xls")
sh = data.sheet_by_name("Sheet1")
x=sh.col_values(0)
y=sh.col_values(1)
plt.plot(x, y, '.')
plt.show()
