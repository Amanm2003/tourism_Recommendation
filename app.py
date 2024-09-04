from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans

app = Flask(__name__)

# Load and process data
df = pd.read_csv('/Users/aman/Desktop/tourismRecommendation/file/locations.csv', sep=',')
country = 'India'
city_names = df['location']

longitude = []
latitude = []
geolocator = Nominatim(user_agent="Trips")

for c in city_names.values:
    location = geolocator.geocode(c + ',' + country)
    latitude.append(location.latitude)
    longitude.append(location.longitude)

df['Latitude'] = latitude
df['Longitude'] = longitude

# Prepare data for clustering
l2 = df[['Latitude', 'Longitude']].values
kmeans = KMeans(5)
kmeans.fit(l2)
identified_clusters = kmeans.predict(l2)
df['loc_clusters'] = identified_clusters

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    input_city = request.form['city']
    cluster = df.loc[df['location'] == input_city, 'loc_clusters'].iloc[0]
    cities = df.loc[df['loc_clusters'] == cluster, 'location']

    similar_cities = []
    for city in cities:
        if city != input_city:
            similar_cities.append(city)
    
    return render_template('results.html', input_city=input_city, similar_cities=similar_cities)

if __name__ == '__main__':
    app.run(debug=True)

# access the application by http://127.0.0.1:5000/