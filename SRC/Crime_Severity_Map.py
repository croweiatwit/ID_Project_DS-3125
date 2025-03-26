import pandas as pd
import folium

# Load the crime data CSV
data = pd.read_csv('csv_2017_2022.csv')

# Ensure the necessary columns are present
required_columns = ['Lat', 'Long', 'STREET']

# Clean data by dropping rows with missing coordinates or street names
data_clean = data.dropna(subset=['Lat', 'Long', 'STREET'])

# Aggregate data by street (count the number of crimes per street)
crime_counts = data_clean.groupby('STREET').size().reset_index(name='crime_count')

# Sort streets by crime count (most dangerous first)
top_streets = crime_counts.sort_values(by='crime_count', ascending=False).head(250)

# Initialize the map centered on Boston
boston_map = folium.Map(location=[42.3601, -71.0589], zoom_start=12)

# Add markers for top dangerous streets
for _, row in top_streets.iterrows():
    street_name = row['STREET']
    crime_count = row['crime_count']
    
    # Find the first record of the street to extract Lat/Long
    street_data = data_clean[data_clean['STREET'] == street_name].iloc[0]
    lat, long = street_data['Lat'], street_data['Long']
    
    
    # I need to get another csv file to relate the data by population.
    # Customize marker color based on crime count (using hex color codes)
    color = '#950606' if crime_count > 5000 else '#FF3333' if crime_count > 1200 else '#FFBF00' if crime_count > 800 else '#2ec939' if crime_count > 500 else '#167f4e' if crime_count > 300 else '#14452F' 
    
    # Add a CircleMarker for each street with the crime count in the popup
    folium.CircleMarker(
        location=[lat, long],
        radius=9,  
        color=color,  # Border color
        fill=True,  
        fill_color=color,  # Fill color (same as border)
        fill_opacity= .7, 
        popup=f"{street_name}: {crime_count} Crimes"
    ).add_to(boston_map)

# Create a legend for the map
legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 195px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px;">
        <h4 style="text-align: center; margin: 10px 0;">Crime Severity</h4>
        <ul style="list-style-type:none; padding-left: 10px;">
            <li><span style="background-color: #14452F; width: 20px; height: 20px; display: inline-block;"></span> <strong>Lower: 300 - 0 </strong></li>
            <li><span style="background-color: #167f4e; width: 20px; height: 20px; display: inline-block;"></span> <strong>Low: 500 - 300</strong></li>
            <li><span style="background-color: #2ec939; width: 20px; height: 20px; display: inline-block;"></span> <strong>Moderate: 800 - 500 </strong></li>
            <li><span style="background-color: #FFBF00; width: 20px; height: 20px; display: inline-block;"></span> <strong>Medium: 1200 - 800  </strong></li>
            <li><span style="background-color: #FF3333; width: 20px; height: 20px; display: inline-block;"></span> <strong>High: 5000 - 1200</strong></li>
            <li><span style="background-color: #950606; width: 20px; height: 20px; display: inline-block;"></span> <strong>Severe: 5000+</strong></li>
        </ul>
    </div>
'''

# Add the legend to the map
boston_map.get_root().html.add_child(folium.Element(legend_html))

# Save the interactive map to an HTML file
boston_map.save("dangerous_streets_map.html")

