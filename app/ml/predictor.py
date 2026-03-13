import joblib
import requests
import numpy as np

model = joblib.load("app/ml/model.pkl")


def get_coordinates(location):

    api_key = "0b5f1c161935d39a4bd7dcfaa506791e"

    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"

    response = requests.get(geo_url)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data:
        return None

    return data[0]["lat"], data[0]["lon"]


def get_climate_data(lat, lon):

    power_url = (
        f"https://power.larc.nasa.gov/api/temporal/climatology/point?"
        f"parameters=T2M,PRECTOTCORR,RH2M&community=ag"
        f"&longitude={lon}&latitude={lat}&start=1981&end=2010&format=JSON"
    )

    response = requests.get(power_url)

    if response.status_code != 200:
        return None

    data = response.json()

    temperature = data['properties']['parameter']['T2M']['ANN']
    humidity = data['properties']['parameter']['RH2M']['ANN']
    rainfall = data['properties']['parameter']['PRECTOTCORR']['ANN']

    return temperature, humidity, rainfall


def predict_crop(N, P, K, ph, location):

    coords = get_coordinates(location)
    print("Coordinates:", coords)

    if not coords:
        return None

    lat, lon = coords

    climate = get_climate_data(lat, lon)
    print("Climate:", climate)

    if not climate:
        return None

    temp, humidity, rainfall = climate

    input_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
    print("Input Data:", input_data)

    prediction = model.predict(input_data)
    print("Raw Prediction:", prediction)

    crop_labels = [
        'rice','maize','chickpea','kidneybeans','pigeonpeas',
        'mothbeans','mungbean','blackgram','lentil','pomegranate',
        'banana','mango','grapes','watermelon','muskmelon',
        'apple','orange','papaya','coconut','cotton','jute','coffee'
    ]

    predicted_crop = crop_labels[int(prediction[0])]
    print("Predicted Crop:", predicted_crop)

    return predicted_crop