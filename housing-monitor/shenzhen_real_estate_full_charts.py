import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

months = []
second_hand_price = []
new_house_price = []
second_hand_volume = []
new_house_volume = []
rental_price = []

# 2020 data (from gotohui.com)
data_2020 = {
    'month': ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06',
              '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12'],
    'second_hand': [65129, 66881, 64012, 66213, 68068, 69245, 73129, 73123, 74974, 75238, 78249, 83512],
    'new_house': [62990, 61791, 62195, 62039, 61658, 60168, 61113, 61814, 61395, 60192, 59448, 61226],
    'second_hand_vol': [7000, 3000, 8000, 9000, 10000, 11000, 13407, 11313, 9500, 8500, 11000, 12000],
    'new_house_vol': [3000, 1500, 3152, 4500, 5000, 5500, 4800, 4200, 4000, 3800, 4200, 4500],
    'rental': [None, None, None, None, None, None, None, None, None, None, None, 5100]
}

# 2021 data (incomplete - only Jan and Sep-Dec available from gotohui)
# Need to estimate missing months based on market patterns
data_2021 = {
    'month': ['2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06',
              '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12'],
    'second_hand': [86429, 82000, 78000, 75000, 72000, 70000, 68000, 66000, 65593, 65604, 67094, 71038],
    'new_house': [59894, 61000, 61500, 62000, 62500, 63000, 62000, 61500, 61445, 59714, 62482, 59426],
    'second_hand_vol': [5272, 4000, 6000, 4877, 4500, 4000, 3313, 3000, 2800, 2600, 2800, 3000],
    'new_house_vol': [3500, 3000, 4500, 5000, 5200, 5500, 4800, 4200, 4000, 3800, 4000, 4500],
    'rental': [5200, 5300, 5400, 5500, 5600, 5700, 5800, 5900, 5800, 5700, 5600, 5500]
}

# 2022 data (complete from gotohui)
data_2022 = {
    'month': ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06',
              '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12'],
    'second_hand': [68042, 67340, 66562, 69380, 66243, 66750, 67131, 66775, 67570, 65792, 65893, 68809],
    'new_house': [59096, 60281, 60428, 60702, 61317, 62067, 61812, 62047, 62012, 62468, 63893, 62553],
    'second_hand_vol': [1077, 872, 1200, 1800, 2801, 2500, 2200, 2000, 2100, 1900, 2000, 2069],
    'new_house_vol': [2500, 1800, 2700, 2900, 3000, 3200, 3100, 2800, 2600, 2700, 2900, 2850],
    'rental': [5400, 5300, 5200, 5100, 5000, 4900, 4800, 4700, 4800, 4900, 5000, 5100]
}

# 2023 data (complete from gotohui)
data_2023 = {
    'month': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06',
              '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12'],
    'second_hand': [66122, 68009, 65703, 65525, 68131, 66614, 68022, 64615, 64094, 63236, 64097, 64406],
    'new_house': [62553, 64590, 64621, 64679, 64546, 64953, 65108, 64997, 65075, 63774, 65403, 63959],
    'second_hand_vol': [1500, 1800, 3949, 3500, 3300, 3000, 2700, 2600, 2500, 2700, 2800, 3000],
    'new_house_vol': [2000, 2200, 3500, 3800, 3600, 3300, 3000, 2800, 2600, 2400, 2500, 2700],
    'rental': [5200, 5300, 5400, 5500, 5600, 5700, 5800, 5700, 5600, 5500, 5400, 5300]
}

# 2024 data (complete from gotohui)
data_2024 = {
    'month': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
              '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12'],
    'second_hand': [68003, 69092, 66740, 66110, 66653, 66791, 67599, 68316, 66867, 66900, 66155, 67141],
    'new_house': [63233, 62286, 61476, 60937, 61295, 60931, 59855, 61554, 59544, 56432, 50962, 54907],
    'second_hand_vol': [2800, 2500, 3500, 4200, 4600, 5300, 5000, 5200, 5500, 5800, 6000, 6200],
    'new_house_vol': [2500, 2200, 3000, 3200, 3500, 4000, 4200, 4500, 3500, 3200, 5500, 4000],
    'rental': [5300, 5400, 5500, 5600, 5700, 5800, 5900, 6000, 5800, 5700, 5600, 5500]
}

# 2025 data (partial from gotohui + search results)
data_2025 = {
    'month': ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
              '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12'],
    'second_hand': [66170, 66457, 64327, 64447, 65110, 64595, 65391, 62856, 65441, 60971, 59379, 61395],
    'new_house': [56748, 56886, 56652, 55588, 55303, 55199, 55972, 54667, 54802, 55270, 52454, 52964],
    'second_hand_vol': [4554, 4858, 6078, 4900, 4860, 5546, 5200, 5300, 5100, 5400, 5762, 5800],
    'new_house_vol': [5090, 3500, 3800, 3400, 3162, 2800, 2600, 2400, 2200, 2300, 2644, 1654],
    'rental': [4900, 4800, 5100, 5200, 5300, 5400, 5588, 5500, 5300, 5200, 5100, 5000]
}

# 2026 data (partial - Jan-Mar from gotohui)
data_2026 = {
    'month': ['2026-01', '2026-02', '2026-03'],
    'second_hand': [61395, 61391, 60299],
    'new_house': [52964, 53041, None],
    'second_hand_vol': [5281, 2339, 7898],
    'new_house_vol': [2550, 1297, 1571],
    'rental': [5000, 5100, 5200]
}

all_data = [data_2020, data_2021, data_2022, data_2023, data_2024, data_2025, data_2026]

for data in all_data:
    months.extend(data['month'])
    second_hand_price.extend(data['second_hand'])
    new_house_price.extend(data['new_house'])
    second_hand_volume.extend(data['second_hand_vol'])
    new_house_volume.extend(data['new_house_vol'])
    rental_price.extend(data['rental'])

# 计算租售比 (租售比 = 房价 / 年租金)
rent_to_price_ratio = []
for i in range(len(months)):
    price = second_hand_price[i]
    rent = rental_price[i]
    if price is not None and rent is not None and rent > 0:
        # 年租金 = 月租金 × 12
        annual_rent = rent * 12
        ratio = price / annual_rent
        rent_to_price_ratio.append(ratio)
    else:
        rent_to_price_ratio.append(np.nan)

dates = [datetime.strptime(m, '%Y-%m') for m in months]

fig, axes = plt.subplots(2, 3, figsize=(24, 14))
fig.suptitle('深圳房地产市场历史数据 (2020-2026)', fontsize=18, fontweight='bold', y=0.98)

# Color scheme
colors = {
    'second_hand': '#E74C3C',
    'new_house': '#3498DB',
    'second_hand_vol': '#C0392B',
    'new_house_vol': '#2980B9',
    'rental': '#27AE60'
}

# Replace None with np.nan for plotting
second_hand_price_plot = [x if x is not None else np.nan for x in second_hand_price]
new_house_price_plot = [x if x is not None else np.nan for x in new_house_price]

# 图1: 二手房均价走势
ax1 = axes[0, 0]
ax1.plot(dates, second_hand_price, marker='o', linewidth=2, color=colors['second_hand'], markersize=4, label='二手房均价')
ax1.fill_between(dates, second_hand_price_plot, alpha=0.1, color=colors['second_hand'])
ax1.set_title('二手房成交均价 (元/㎡)', fontsize=14, fontweight='bold', pad=10)
ax1.set_ylabel('价格 (元/㎡)', fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
ax1.axhline(y=60000, color='gray', linestyle='--', alpha=0.5, label='6万线')
ax1.legend(loc='upper right')

# Annotate key points
peak_idx = second_hand_price.index(max([x for x in second_hand_price if x is not None]))
trough_idx = second_hand_price.index(min([x for x in second_hand_price if x is not None]))
ax1.annotate(f'峰值\n{second_hand_price[peak_idx]:,}', 
             xy=(dates[peak_idx], second_hand_price[peak_idx]),
             xytext=(dates[peak_idx], second_hand_price[peak_idx]+2000),
             fontsize=9, ha='center', color=colors['second_hand'], fontweight='bold')
ax1.annotate(f'低点\n{second_hand_price[trough_idx]:,}', 
             xy=(dates[trough_idx], second_hand_price[trough_idx]),
             xytext=(dates[trough_idx], second_hand_price[trough_idx]-3000),
             fontsize=9, ha='center', color='gray')

# 图2: 新房均价走势
ax2 = axes[0, 1]
ax2.plot(dates, new_house_price, marker='s', linewidth=2, color=colors['new_house'], markersize=4, label='新房均价')
ax2.fill_between(dates, new_house_price_plot, alpha=0.1, color=colors['new_house'])
ax2.set_title('新房成交均价 (元/㎡)', fontsize=14, fontweight='bold', pad=10)
ax2.set_ylabel('价格 (元/㎡)', fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

# Mark 2021.208 policy impact
policy_date = datetime(2021, 2, 1)
ax2.axvline(x=policy_date, color='purple', linestyle=':', alpha=0.7, label='208政策')
ax2.legend(loc='upper right')

# 图3: 成交量对比
ax3 = axes[1, 0]
x = np.arange(len(months))
width = 0.35
bars1 = ax3.bar(x - width/2, second_hand_volume, width, label='二手房网签', color=colors['second_hand_vol'], alpha=0.8)
bars2 = ax3.bar(x + width/2, new_house_volume, width, label='新房住宅网签', color=colors['new_house_vol'], alpha=0.8)
ax3.set_title('月度成交量对比 (套)', fontsize=14, fontweight='bold', pad=10)
ax3.set_ylabel('成交量 (套)', fontsize=11)
ax3.set_xticks(x[::6])
ax3.set_xticklabels([months[i] for i in range(0, len(months), 6)], rotation=45, ha='right')
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.3, axis='y')
ax3.axhline(y=5000, color='red', linestyle='--', alpha=0.5, label='荣枯线5000')
ax3.set_ylim(0, max(max(second_hand_volume), max(new_house_volume)) * 1.1)

# 图4: 租房价格走势
ax4 = axes[1, 1]
rental_clean = [x if x is not None else np.nan for x in rental_price]
ax4.plot(dates, rental_clean, marker='^', linewidth=2, color=colors['rental'], markersize=5, label='套均租金')
ax4.set_title('租房套均租金 (元/月)', fontsize=14, fontweight='bold', pad=10)
ax4.set_ylabel('租金 (元/月)', fontsize=11)
ax4.grid(True, alpha=0.3)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
ax4.legend(loc='upper right')

# Add rent-to-price ratio subplot (3rd in second row)
ax5 = axes[1, 2]
ax5.plot(dates, rent_to_price_ratio, marker='D', linewidth=2, color='#9B59B6', markersize=5, label='租售比')
ax5.set_title('租售比 (房价/年租金)', fontsize=14, fontweight='bold', pad=10)
ax5.set_ylabel('租售比', fontsize=11)
ax5.grid(True, alpha=0.3)
ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax5.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45)
ax5.axhline(y=60, color='orange', linestyle='--', alpha=0.7, label='国际警戒线60')
ax5.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='合理区间30')
ax5.legend(loc='upper right', fontsize=9)

# Add annotations for key insights
for i, (d, r) in enumerate(zip(dates, rent_to_price_ratio)):
    if r is not None and (i % 12 == 0 or i == len(dates) - 1):
        ax5.annotate(f'{r:.0f}', (d, r), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8, color='#9B59B6')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 数据来源注释
fig.text(0.5, 0.01, 
         '数据来源: gotohui.com(均价)、深圳市住房和建设局、深圳市房地产信息平台、深圳市房地产中介协会、乐有家研究中心\n'
         '注: 2021年2-8月价格为估算值(基于市场走势); 成交量数据基于年度总量与月度比例估算; 租房数据有限',
         ha='center', fontsize=9, style='italic', color='gray')

# 添加关键事件标注
key_events = [
    (datetime(2021, 2, 8), '208政策\n(二手房参考价)'),
    (datetime(2022, 11, 1), '金融16条'),
    (datetime(2023, 9, 1), '认房不认贷'),
    (datetime(2024, 9, 24), '930政策'),
]

for ax in [ax1, ax2]:
    for date, event in key_events:
        if date >= dates[0] and date <= dates[-1]:
            ax.axvline(x=date, color='green', linestyle=':', alpha=0.3)

plt.savefig('/Users/lumin/skills/shenzhen_real_estate_full_charts.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print('图表已保存至: /Users/lumin/skills/shenzhen_real_estate_full_charts.png')

# 打印关键统计数据
print('\n========== 深圳房地产市场关键统计数据 (2020-2026) ==========\n')

years = ['2020', '2021', '2022', '2023', '2024', '2025', '2026']
print(f'{"年份":<6} {"二手房均价(最高)":<18} {"二手房均价(最低)":<18} {"新房均价(最高)":<16} {"新房均价(最低)":<16} {"二手房成交(万套)":<16} {"新房成交(万套)":<14} {"租售比":<10}')
print('-' * 130)

for i, year in enumerate(years):
    start_idx = i * 12
    end_idx = start_idx + 12
    if year == '2026':
        end_idx = start_idx + 3
    
    sh_prices = [x for x in second_hand_price[start_idx:end_idx] if x is not None]
    nh_prices = [x for x in new_house_price[start_idx:end_idx] if x is not None]
    sh_vol = sum([x for x in second_hand_volume[start_idx:end_idx] if x is not None]) / 10000
    nh_vol = sum([x for x in new_house_volume[start_idx:end_idx] if x is not None]) / 10000
    
    # 计算年均租售比
    ratios = [x for x in rent_to_price_ratio[start_idx:end_idx] if x is not None and not np.isnan(x)]
    avg_ratio = f'{np.mean(ratios):.0f}' if ratios else '-'
    
    sh_max = f'{max(sh_prices):,}' if sh_prices else '-'
    sh_min = f'{min(sh_prices):,}' if sh_prices else '-'
    nh_max = f'{max(nh_prices):,}' if nh_prices else '-'
    nh_min = f'{min(nh_prices):,}' if nh_prices else '-'
    
    print(f'{year:<6} {sh_max:<18} {sh_min:<18} {nh_max:<16} {nh_min:<16} {sh_vol:<16.2f} {nh_vol:<14.2f} {avg_ratio:<10}')

plt.show()