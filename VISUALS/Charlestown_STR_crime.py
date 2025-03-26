
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = r"C:\Users\icrow\Desktop\Data science ID project\csv_2017_2022.csv"
data = pd.read_csv(file_path, low_memory=False, encoding="utf-8",
                   dtype={'DISTRICT': str, 'OFFENSE_CODE': str, 'OFFENSE_DESCRIPTION': str, 'OCCURRED_ON_DATE': str,
                          'STREET': str})

# Clean and prepare the data
data['STREET'] = data['STREET'].astype(str).str.strip()  # Remove leading/trailing whitespace from street
data = data.dropna(subset=['STREET', 'DISTRICT'])  # Remove rows with missing district or street


lat_min = 42.3700  # Minimum latitude (can adjust as needed for which part of Roxbury)
lat_max =  42.3785 
long_min = -71.0675
long_max = -71.0590



"""
42.3790,-71.0570

42.3680, -71.0630
Navy Yard

Maximum Latitude: 42.3790° N
Minimum Latitude: 42.3680° N
Maximum Longitude: -71.0570° W
Minimum Longitude: -71.0630° W


Main Street/Charlestown's

Maximum Latitude: 42.3785° N
Minimum Latitude: 42.3700° N
Maximum Longitude: -71.0590° W
Minimum Longitude: -71.0675° W


Bunker Hill 

Maximum Latitude: 42.3750° N
Minimum Latitude: 42.3690° N
Maximum Longitude: -71.0620° W
Minimum Longitude: -71.0700° W
"""


#change int boolean expression to make it true and false:


filtered_data = data[(data['Lat'] >= lat_min) & (data['Lat'] <= lat_max) &
                     (data['Long'] >= long_min) & (data['Long'] <= long_max)]

# Now you can proceed with your existing code to count crimes by street
filtered_data['DISTRICT'] = filtered_data['DISTRICT'].replace({'B2': 'Roxbury'})
filtered_data.drop(['SHOOTING', 'Lat', 'Long', 'REPORTING_AREA', 'UCR_PART', 'INCIDENT_NUMBER', 'OFFENSE_CODE',
                    'DAY_OF_WEEK', 'HOUR'], axis=1, inplace=True)

# Group by 'STREET' to count crimes per street
street_crime = filtered_data['STREET'].value_counts().reset_index()
street_crime.columns = ['STREET', 'COUNT']


# Sort streets by the count of crimes
street_crime = street_crime.sort_values(by='COUNT', ascending=False)

top_streets = street_crime.head(40) # need to make with street that have greater than 1000


# Plot the data with the default Seaborn palette
plt.figure(figsize=(20, 10))
ax = sns.barplot(x='STREET', y='COUNT', data=top_streets, palette='RdYlGn')


# Add the crime counts as labels on the bars
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2, height, f'{int(height)}', ha="center", va="bottom", fontsize=8, color="black")

# Set plot labels and title
plt.xlabel('STREET', fontsize=8)
plt.ylabel('Number of Incidents', fontsize=14)
plt.title('Crime Incidents Top 40 Street in Main Street/Charlestowns', fontsize=16)
plt.xticks(rotation=90)  # Rotate street names for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)


# Show the plot
plt.tight_layout()  # Ensure labels are not cut off
plt.show()

#plt.savefig('Main Street_STR_crime.jpg', format='jpg')

