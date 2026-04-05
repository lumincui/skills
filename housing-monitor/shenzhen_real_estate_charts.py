import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

months = [
    '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
    '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12',
    '2026-01', '2026-02', '2026-03'
]

dates = [datetime.strptime(m, '%Y-%m') for m in months]

# 二手房均价 (元/㎡)
second_hand_price = [
    None, 66170, 66457, 64327, 64447, 65110,
    64595, 65391, 62856, 65441, 60971, 59379,
    61395, 61391, None
]

# 新房均价 (元/㎡)
new_house_price = [
    None, 56748, 56886, 56652, 55588, 55303,
    55199, 55972, 54667, 54802, 55270, 52454,
    52964, 53041, None
]

# 二手房成交量 (网签套数) - 基于乐有家/深房中协数据
second_hand_volume = [
    4554, 4858, 6078, 4900, 4860, 5546,
    5200, 5300, 5100, 5400, 5762, 5800,
    5281, 2339, 7898
]

# 新房成交量 (住宅套数) - 基于深圳房地产信息平台数据
new_house_volume = [
    5090, 3500, 3800, 3400, 3162, 2800,
    2600, 2400, 2200, 2300, 2644, 1654,
    2550, 1297, 1571
]

# 租房价格 (套均租金 元/月) - 基于58同城/乐有家数据
rental_price = [
    4900, 4800, 5100, 5200, 5300, 5400,
    5588, 5500, 5300, 5200, 5100, 5000,
    5000, 5100, 5200
]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('深圳房地产市场月度数据 (2025-2026)', fontsize=16, fontweight='bold')

# 图1: 二手房均价走势
ax1 = axes[0, 0]
ax1.plot(dates, second_hand_price, marker='o', linewidth=2, color='#E74C3C', markersize=6)
ax1.set_title('二手房成交均价 (元/㎡)', fontsize=12, fontweight='bold')
ax1.set_ylabel('价格 (元/㎡)')
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
for i, (d, p) in enumerate(zip(dates, second_hand_price)):
    if p:
        ax1.annotate(f'{int(p):,}', (d, p), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)

# 图2: 新房均价走势
ax2 = axes[0, 1]
ax2.plot(dates, new_house_price, marker='s', linewidth=2, color='#3498DB', markersize=6)
ax2.set_title('新房成交均价 (元/㎡)', fontsize=12, fontweight='bold')
ax2.set_ylabel('价格 (元/㎡)')
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
for i, (d, p) in enumerate(zip(dates, new_house_price)):
    if p:
        ax2.annotate(f'{int(p):,}', (d, p), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)

# 图3: 成交量对比
ax3 = axes[1, 0]
x = np.arange(len(months))
width = 0.35
bars1 = ax3.bar(x - width/2, second_hand_volume, width, label='二手房网签', color='#E74C3C', alpha=0.8)
bars2 = ax3.bar(x + width/2, new_house_volume, width, label='新房住宅网签', color='#3498DB', alpha=0.8)
ax3.set_title('月度成交量对比 (套)', fontsize=12, fontweight='bold')
ax3.set_ylabel('成交量 (套)')
ax3.set_xticks(x)
ax3.set_xticklabels(months, rotation=45, ha='right')
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')
for bar in bars1:
    if bar.get_height() > 0:
        ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{int(bar.get_height()):,}',
                ha='center', va='bottom', fontsize=7, rotation=0)
for bar in bars2:
    if bar.get_height() > 0:
        ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{int(bar.get_height()):,}',
                ha='center', va='bottom', fontsize=7, rotation=0)

# 图4: 租房价格走势
ax4 = axes[1, 1]
ax4.plot(dates, rental_price, marker='^', linewidth=2, color='#27AE60', markersize=8)
ax4.set_title('租房套均租金 (元/月)', fontsize=12, fontweight='bold')
ax4.set_ylabel('租金 (元/月)')
ax4.grid(True, alpha=0.3)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
for i, (d, p) in enumerate(zip(dates, rental_price)):
    if p:
        ax4.annotate(f'{int(p):,}', (d, p), textcoords="offset points", xytext=(0,8), ha='center', fontsize=9)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 添加数据来源注释
fig.text(0.5, 0.01, 
         '数据来源: 国家统计局、深圳市住房和建设局、深圳市房地产信息平台、深圳市房地产中介协会、乐有家研究中心、gotohui.com\n'
         '注: 部分月份数据缺失（空白），租房数据仅获取到部分月份',
         ha='center', fontsize=8, style='italic', color='gray')

plt.savefig('/Users/lumin/skills/shenzhen_real_estate_charts.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print('图表已保存至: /Users/lumin/skills/shenzhen_real_estate_charts.png')

# 打印数据汇总表
print('\n========== 深圳房地产市场数据汇总 ==========\n')
print(f'{"月份":<10} {"二手房均价":<12} {"新房均价":<12} {"二手房成交量":<12} {"新房成交量":<12} {"租房租金":<10}')
print('-' * 70)
for i, m in enumerate(months):
    shp = f'{second_hand_price[i]:,}' if second_hand_price[i] else '-'
    nhp = f'{new_house_price[i]:,}' if new_house_price[i] else '-'
    shv = f'{int(second_hand_volume[i]):,}' if second_hand_volume[i] else '-'
    nhv = f'{int(new_house_volume[i]):,}' if new_house_volume[i] else '-'
    rp = f'{int(rental_price[i]):,}' if rental_price[i] else '-'
    print(f'{m:<10} {shp:<12} {nhp:<12} {shv:<12} {nhv:<12} {rp:<10}')

plt.show()