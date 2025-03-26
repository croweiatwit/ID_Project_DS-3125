import pandas as pd
import webbrowser
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import os

file_path = r"C:\Users\icrow\PycharmProjects\PythonDataScience\csv_2017_2022.csv"
data = pd.read_csv(file_path, low_memory=False, encoding="utf-8",
                   dtype={'DISTRICT': str, 'OFFENSE_CODE': str, 'OFFENSE_DESCRIPTION': str, 'OCCURRED_ON_DATE': str,
                          'STREET': str})
"""
This is the graph that for Roxbury

"""
roxbury = {'B2'}

roxbury_sorted_data = data.sort_values(by=['DISTRICT', 'OCCURRED_ON_DATE'], ascending=True)

# Replace district names with full names
roxbury_sorted_data['DISTRICT'] = roxbury_sorted_data['DISTRICT'].replace({'B2': 'Roxbury'})

# Drop unnecessary columns
roxbury_sorted_data.drop(['SHOOTING', 'Lat', 'Long', 'REPORTING_AREA', 'UCR_PART', 'INCIDENT_NUMBER', 'OFFENSE_CODE',
                  'DAY_OF_WEEK', 'HOUR'], axis=1, inplace=True)

# Sample every 3rd row
sampled_data = roxbury_sorted_data.iloc[::3]

offense_counts = sampled_data['OFFENSE_CODE_GROUP'].value_counts()

# Get the top 5 offense categories
top5 = offense_counts[:20].copy()


# Add the "Other" category to the top5 using pd.concat() instead of append
#other_series = pd.Series({'Other': other_sum})
#top5 = pd.concat([top5, other_series])

# Create a pie chart
plt.figure(figsize=(15, 11))

def format_labels(label):
    # Here we add a line break after the first word if it's too long
    if len(label) > 10:  # Adjust this number based on how long your offense names are
        return '\n'.join(label.split())
    return label


percentages = top5 / top5.sum() * 100

labels = [format_labels(label) if percentage >= 3 else '' for label, percentage in zip(top5.index, percentages)]

filtered_top5 = top5[percentages < 3]
filtered_percentages = percentages[percentages < 3]


patches, texts, autotexts = plt.pie(
    top5,
    labels=labels,   # Add line breaks for long names
    autopct='%1.1f%%',  # Display percentage
    startangle=90,  # Start angle for the pie chart
    labeldistance=1.2,  # Increase distance between pie and labels
    pctdistance=0.85  # Adjust distance of percentages from the center
)


legend_patches = [patches[i] for i in range(len(patches)) if top5.index[i] in filtered_top5.index]
legend_labels = filtered_top5.index

plt.legend(
    legend_patches,  # The patches that represent the segments in the legend
    legend_labels,   # Labels for each segment
    loc="best",      # Automatically chooses the best location
    fontsize=12,      # Font size for the legend text
    title="Offenses under 3%",  # Optional: Title for the legend
    bbox_to_anchor=(.9, .85)  # Optional: Places the legend outside of the chart area
)



plt.title('Top Offense Types and Other (Roxbury District)')

for text in texts + autotexts:
    text.set_fontsize(10)

    text.set_fontweight('bold')


#plt.show()
plt.savefig('Roxbury.jpg', format='jpg')





