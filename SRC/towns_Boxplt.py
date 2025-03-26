import pandas as pd
#import webbrowser
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import os


file_path = r"C:\Users\icrow\Desktop\Data science ID project\csv_2017_2022.csv"
data = pd.read_csv(file_path, low_memory=False, encoding="utf-8",
                   dtype={'DISTRICT': str, 'OFFENSE_CODE': str, 'OFFENSE_DESCRIPTION': str, 'OCCURRED_ON_DATE': str,
                          'STREET': str})

# Clean up and filter valid districts
valid_districts = {'A1', 'A15', 'A7', 'B2', 'B3', 'C6', 'C11', 'D4', 'D14', 'E5', 'E13', 'E18'}
data = data.dropna(subset=['DISTRICT'])  # Remove NaN values
data['DISTRICT'] = data['DISTRICT'].astype(str).str.strip()  # Remove extra spaces
data = data[data['DISTRICT'].isin(valid_districts)]  # Filter valid districts

# Sort data
sorted_data = data.sort_values(by=['DISTRICT', 'OCCURRED_ON_DATE'], ascending=True)

# Replace district names with full names
sorted_data['DISTRICT'] = sorted_data['DISTRICT'].replace({
    'A1': 'Downtown Boston', 'A7': 'East Boston',
    'A15': 'Charlestown', 'B2': 'Roxbury', 'B3': 'Mattapan',
    'C6': 'South Boston', 'C11': 'Dorchester', 'D4': 'Fenway, Lower Roxbury',
    'D14': 'Allston & Brighton', 'E5': 'West Roxbury & Roslindale',
    'E13': 'Jamaica Plain', 'E18': 'Hyde Park'
})

# Drop unnecessary columns
sorted_data.drop(['SHOOTING', 'Lat', 'Long', 'REPORTING_AREA', 'UCR_PART', 'INCIDENT_NUMBER', 'OFFENSE_CODE',
                  'DAY_OF_WEEK', 'HOUR'], axis=1, inplace=True)

# Sample every 3rd row
sampled_data = sorted_data.iloc[::3]

# Count incidents per district

district_counts = sorted_data['DISTRICT'].value_counts().reset_index()
district_counts.columns = ['DISTRICT', 'COUNT']
district_counts = district_counts.sort_values(by="COUNT", ascending=False)  # Sort

cmap = plt.get_cmap('RdYlGn_r')
# Reverse the colormap
#cmap = mcolors.ListedColormap(cmap(np.linspace(0, 0., 128))) # stops the colors halfway through.
# Choose the colormap you want
norm = mcolors.Normalize(vmin=district_counts['COUNT'].min(), vmax=district_counts['COUNT'].max())  # Normalize based on the COUNT values

# Plot the data
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='DISTRICT', y='COUNT', data=district_counts, palette=cmap(norm(district_counts['COUNT'])))




for p in ax.patches:
    p.set_facecolor(cmap(norm(p.get_height())))

for p in ax.patches:
    # Get the height of each bar (crime count)
    height = p.get_height()

    # Place the text on top of each bar
    ax.text(p.get_x() + p.get_width() / 2, height, f'{int(height)}',
            ha="center", va="bottom", fontsize=12, color="black")

plt.xlabel('DISTRICT', fontsize=14)
plt.ylabel('Number of Incidents', fontsize=14)
plt.title('Crime Incidents per District (Div by 3)', fontsize=16)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

#plt.show()
plt.tight_layout()


plt.savefig('Towns_Boston_Boxplt.jpg', format='jpg')