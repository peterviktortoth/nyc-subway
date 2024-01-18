from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import gtfs_realtime_pb2

app = Flask(__name__)
CORS(app)

def convert_timestamp_to_readable(time):
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def parse_trip_id(trip_id):
    parts = trip_id.split('_')
    if len(parts) > 1:
        train_line = parts[1][0]
        direction_code = parts[1].split('..')[-1]
        direction = "Downtown" if direction_code == "S" else "Uptown"
        return train_line, direction
    else:
        return "Unknown", "Unknown"

def get_time_until_arrival(arrival_time_str):
    arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()
    time_delta = arrival_time - current_time
    return round(time_delta.total_seconds() / 60)

def get_valid_stop_ids():
    # This function could fetch stop_ids from a database or a configuration file
    # For demonstration, returning a hardcoded list
    return ["R11S", "R11N", "R11", "629N", "629S"]


def get_mta_data():
    urls = [
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs",
        "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"
    ]

    headers = {"x-api-key": "6NMqF78y3816yZVnLeRTH799paXqFpoLassNyAz3"}
    data = []

    for url in urls:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)

            valid_stop_ids = get_valid_stop_ids()

            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    for update in entity.trip_update.stop_time_update:
                        if update.stop_id in valid_stop_ids:
                            arrival_time_str = convert_timestamp_to_readable(update.arrival.time)
                            train_line, direction = parse_trip_id(entity.trip_update.trip.trip_id)
                            minutes_until_arrival = get_time_until_arrival(arrival_time_str)

                            data.append({
                                'message': f"{direction} {train_line} train arriving in {minutes_until_arrival} minutes",
                                'minutes_until_arrival': minutes_until_arrival
                            })
        else:
            print("Failed to retrieve data from", url)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    # Sort the data by ascending arrival time
    sorted_data = sorted(data, key=lambda x: x['minutes_until_arrival'])
    return sorted_data


@app.route('/refresh')
def refresh():
    transit_data = get_mta_data()
    return jsonify(transit_data)

if __name__ == '__main__':
    app.run(debug=True)
