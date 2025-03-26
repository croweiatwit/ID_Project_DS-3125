import pandas as pd
import webbrowser
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import os

file_path = r"C:\Users\icrow\Desktop\Data science ID project\csv_2017_2022.csv"
data = pd.read_csv(file_path, low_memory=False, encoding="utf-8",
                   dtype={'DISTRICT': str, 'OFFENSE_CODE': str, 'OFFENSE_DESCRIPTION': str, 'OCCURRED_ON_DATE': str,
                          'STREET': str})
"""
This is the graph that for Roxbury

"""
fenway = {'D4'}  # Select multiple districts

# Filter data for the selected districts
filtered_data = data[data['DISTRICT'].isin(fenway)]
 
# Replace district codes with full names
filtered_data['DISTRICT'] = filtered_data['DISTRICT'].replace({'D4': 'Roxbury'})

# Sort data
filtered_sorted_data = filtered_data.sort_values(by=['DISTRICT', 'OCCURRED_ON_DATE'], ascending=True)

# Drop unnecessary columns
filtered_sorted_data.drop(['SHOOTING', 'REPORTING_AREA', 'UCR_PART', 'INCIDENT_NUMBER', 'OFFENSE_CODE', 'DAY_OF_WEEK', 'HOUR'], axis=1, inplace=True)

# Sample every 3rd row
sampled_data = filtered_sorted_data.iloc[::3]

# Calculate offense counts and top offenses
offense_counts = sampled_data['OFFENSE_CODE_GROUP'].value_counts()
top5 = offense_counts[:20].copy()

# Create the pie chart
plt.figure(figsize=(15, 11))

def format_labels(label):
    if len(label) > 10:
        return '\n'.join(label.split())
    return label

percentages = top5 / top5.sum() * 100
labels = [format_labels(label) if percentage >= 3 else '' for label, percentage in zip(top5.index, percentages)]
filtered_top5 = top5[percentages < 3]


patches, texts, autotexts = plt.pie(
    top5,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    #labeldistance=1.2,
    pctdistance=0.85
)

# Update the legend to reflect the new filtered data
legend_patches = [patches[i] for i in range(len(patches)) if top5.index[i] in filtered_top5.index]
legend_labels = filtered_top5.index
#labels = [f'{l}, {s:0.1f}%' for l, s in zip(labels, sizes)]

plt.legend(

# need to put a section that says if lower then 3% then put in legend
# labels = [f'{l}, {s:0.1f}%' for l, s in zip(labels, sizes)]


    legend_patches,
    legend_labels,
    loc="best",
    fontsize=12,
    title="Offenses under 3%",
    bbox_to_anchor=(.9, .85)
)

plt.title('Top Offense Types and Other (Fenway)')

for text in texts + autotexts:
    text.set_fontsize(10)
    text.set_fontweight('bold')

#plt.show()
#plt.tight_layout()

plt.savefig('Fenway_pi.jpg', format='jpg')