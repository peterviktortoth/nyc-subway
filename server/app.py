from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
import gtfs_realtime_pb2 as gpb2
import nyct_subway_pb2 as nspb2


app = Flask(__name__)
CORS(app)

def convert_timestamp_to_readable(time):
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def parse_trip_id(trip_id):
    parts = trip_id.split('_')
    if len(parts) > 1:
        train_line = parts[1][0]
        
        # Find the index of '..' and get the next character
        dot_index = parts[1].find('..')
        if dot_index != -1:
            direction_code = parts[1][dot_index + 2]  # Get the character immediately after '..'
        else:
            direction_code = "Unknown"

        print("Direction Code:", direction_code)

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
            feed = gpb2.FeedMessage()
            feed.ParseFromString(response.content)

            feed_header = {
                'timestamp': feed.header.timestamp,
                'nyct_subway_version': feed.header.Extensions[nspb2.nyct_feed_header].nyct_subway_version if feed.header.HasExtension(nspb2.nyct_feed_header) else None
            }

            valid_stop_ids = get_valid_stop_ids()

            for entity in feed.entity:
                if entity.HasField('trip_update'):
                    trip_update = entity.trip_update
                    if trip_update.trip.HasExtension(nspb2.nyct_trip_descriptor):
                        nyct_trip_desc = trip_update.trip.Extensions[nspb2.nyct_trip_descriptor]

                        for update in trip_update.stop_time_update:
                            if update.stop_id in valid_stop_ids:
                                arrival_time_str = convert_timestamp_to_readable(update.arrival.time)
                                minutes_until_arrival = get_time_until_arrival(arrival_time_str)

                                trip_data = {
                                    'feed_header': feed_header,
                                    'trip_id': trip_update.trip.trip_id,
                                    'direction': nyct_trip_desc.direction if nyct_trip_desc.HasField('direction') else None,
                                    'train_id': nyct_trip_desc.train_id if nyct_trip_desc.HasField('train_id') else None,
                                    'is_assigned': nyct_trip_desc.is_assigned if nyct_trip_desc.HasField('is_assigned') else None,
                                    'minutes_until_arrival': minutes_until_arrival,

                                }

                                if entity.HasField('vehicle'):
                                    vehicle = entity.vehicle
                                    trip_data['vehicle'] = {
                                        'id': vehicle.vehicle.id,
                                        'latitude': vehicle.position.latitude,
                                        'longitude': vehicle.position.longitude,
                                        'congestion_level': vehicle.congestion_level,
                                        'occupancy_status': vehicle.occupancy_status
                                    }

                                data.append(trip_data)

                # Optionally, handle other entity types like VehiclePosition and Alert here

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
