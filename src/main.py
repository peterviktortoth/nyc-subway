import requests
import gtfs_realtime_pb2
from datetime import datetime

def convert_timestamp_to_readable(time):
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def get_mta_data():
    url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"  # Replace with your API endpoint
    headers = {
        "x-api-key": "6NMqF78y3816yZVnLeRTH799paXqFpoLassNyAz3"  # Replace with your API key
    }

    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        for entity in feed.entity:
            if entity.HasField('trip_update'):
                for update in entity.trip_update.stop_time_update:
                    if update.stop_id == "R11S":
                        arrival_time = convert_timestamp_to_readable(update.arrival.time)
                        departure_time = convert_timestamp_to_readable(update.departure.time)

                        print(f"Trip ID: {entity.trip_update.trip.trip_id}")
                        print(f"Arrival Time: {arrival_time}")
                        print(f"Departure Time: {departure_time}")
                        print(f"Stop ID: {update.stop_id}")
                        print("----------")
    else:
        print("Failed to retrieve data")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    get_mta_data()
