#! python3.9.6 64-bit
from pylab import *
from tqdm import tqdm  # 进度条模块

import data
from Arknights_simulation import simulation

print('警告:这将非常消耗内存!')
input()

results = []
for i in tqdm(range(1000)):  # 模拟 N次连抽 N次
    obj = simulation(data.chars, data.star6_p_up, data.star5_p_up)
    for j in range(i):
        obj.simulate()
    results.append(obj.times_of_star6)
    del obj


# 绘制图表
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文

x_axis_data = [i for i in range(len(results))]
y_axis_data = results
y_axis_data2 = [results[-1] / len(results) * 50] * len(results)  # 50抽可以获得6星的个数

# plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
plt.plot(x_axis_data, y_axis_data, y_axis_data2, 'ro-', color='#1e90ff',
         alpha=0.8, linewidth=1, label='增长变化')

# 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
plt.legend(loc="upper right")
plt.xlabel('寻访次数')
plt.ylabel('六星个数')

plt.show()
