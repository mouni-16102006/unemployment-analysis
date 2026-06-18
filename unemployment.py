# ================================================
# UNEMPLOYMENT ANALYSIS - CodeAlpha Internship
# ================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. LOAD THE DATASET
# ─────────────────────────────────────────────
df = pd.read_csv('unemployment.csv')

print("=" * 55)
print("DATASET OVERVIEW")
print("=" * 55)
print(df.head(10))
print(f"\nShape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nMissing Values:\n{df.isnull().sum()}")

# ─────────────────────────────────────────────
# 2. CLEAN THE DATA
# ─────────────────────────────────────────────
df.columns = df.columns.str.strip()

df = df.rename(columns={
    'Region'                                 : 'State',
    'Date'                                   : 'Date',
    'Frequency'                              : 'Frequency',
    'Estimated Unemployment Rate (%)'        : 'Unemployment_Rate',
    'Estimated Employed'                     : 'Employed',
    'Estimated Labour Participation Rate (%)': 'Labour_Rate'
})

df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df['Month'] = df['Date'].dt.month
df['Year']  = df['Date'].dt.year
df = df.dropna()

print("\n✅ Data cleaned successfully!")
print(f"Total records: {len(df)}")

# ─────────────────────────────────────────────
# 3. BASIC STATISTICS
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("UNEMPLOYMENT STATISTICS")
print("=" * 55)
print(f"Average Unemployment Rate : {df['Unemployment_Rate'].mean():.2f}%")
print(f"Highest Unemployment Rate : {df['Unemployment_Rate'].max():.2f}%")
print(f"Lowest  Unemployment Rate : {df['Unemployment_Rate'].min():.2f}%")

# ─────────────────────────────────────────────
# 4. CHART 1 — Unemployment Rate Over Time
# ─────────────────────────────────────────────
plt.figure(figsize=(14, 6))
monthly = df.groupby('Date')['Unemployment_Rate'].mean().reset_index()
plt.plot(monthly['Date'], monthly['Unemployment_Rate'],
         color='crimson', linewidth=2.5, marker='o', markersize=4)
plt.axvspan(pd.Timestamp('2020-03-01'),
            pd.Timestamp('2020-08-01'),
            alpha=0.2, color='red', label='Covid-19 Lockdown')
plt.title('Unemployment Rate Over Time in India',
          fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('unemployment_over_time.png', dpi=150)
plt.show()
print("✅ Chart 1 saved: unemployment_over_time.png")

# ─────────────────────────────────────────────
# 5. CHART 2 — Top 10 States Highest Unemployment
# ─────────────────────────────────────────────
plt.figure(figsize=(12, 7))
state_avg = df.groupby('State')['Unemployment_Rate'].mean()\
              .sort_values(ascending=False).head(10)
colors = sns.color_palette('Reds_r', len(state_avg))
bars = plt.barh(state_avg.index, state_avg.values, color=colors)
plt.xlabel('Average Unemployment Rate (%)', fontsize=12)
plt.title('Top 10 States with Highest Unemployment Rate',
          fontsize=15, fontweight='bold')
for bar, val in zip(bars, state_avg.values):
    plt.text(bar.get_width() + 0.2,
             bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('top10_states.png', dpi=150)
plt.show()
print("✅ Chart 2 saved: top10_states.png")

# ─────────────────────────────────────────────
# 6. CHART 3 — Covid-19 Impact
# ─────────────────────────────────────────────
plt.figure(figsize=(10, 6))
before_covid = df[df['Date'] < '2020-03-01']['Unemployment_Rate'].mean()
during_covid = df[(df['Date'] >= '2020-03-01') &
                  (df['Date'] <= '2020-08-01')]['Unemployment_Rate'].mean()
after_covid  = df[df['Date'] > '2020-08-01']['Unemployment_Rate'].mean()

periods = ['Before Covid\n(< Mar 2020)',
           'During Covid\n(Mar–Aug 2020)',
           'After Covid\n(> Aug 2020)']
values  = [before_covid, during_covid, after_covid]
colors  = ['#2ecc71', '#e74c3c', '#3498db']

bars = plt.bar(periods, values, color=colors,
               width=0.5, edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.3,
             f'{val:.1f}%', ha='center',
             fontsize=13, fontweight='bold')
plt.title('Covid-19 Impact on Unemployment Rate',
          fontsize=15, fontweight='bold')
plt.ylabel('Average Unemployment Rate (%)')
plt.ylim(0, max(values) + 5)
plt.tight_layout()
plt.savefig('covid_impact.png', dpi=150)
plt.show()
print("✅ Chart 3 saved: covid_impact.png")

# ─────────────────────────────────────────────
# 7. CHART 4 — Heatmap by State and Month
# ─────────────────────────────────────────────
plt.figure(figsize=(14, 10))
pivot = df.pivot_table(values='Unemployment_Rate',
                       index='State',
                       columns='Month',
                       aggfunc='mean')
pivot.columns = ['Jan','Feb','Mar','Apr','May','Jun',
                 'Jul','Aug','Sep','Oct','Nov','Dec']
sns.heatmap(pivot, cmap='YlOrRd', annot=True,
            fmt='.1f', linewidths=0.5,
            cbar_kws={'label': 'Unemployment Rate (%)'})
plt.title('Unemployment Rate by State and Month',
          fontsize=15, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('State')
plt.tight_layout()
plt.savefig('heatmap_state_month.png', dpi=150)
plt.show()
print("✅ Chart 4 saved: heatmap_state_month.png")

# ─────────────────────────────────────────────
# 8. FINAL INSIGHTS
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("KEY INSIGHTS")
print("=" * 55)
print(f"📌 Average unemployment rate      : {df['Unemployment_Rate'].mean():.2f}%")
print(f"📌 Before Covid avg rate          : {before_covid:.2f}%")
print(f"📌 During Covid avg rate          : {during_covid:.2f}%")
print(f"📌 After  Covid avg rate          : {after_covid:.2f}%")
print(f"📌 Covid increased unemployment by: {during_covid - before_covid:.2f}%")
print(f"📌 Worst state : {state_avg.index[0]} ({state_avg.values[0]:.2f}%)")
print("\n✅ Analysis Complete!")