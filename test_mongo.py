
from backend.mongo_manager import MongoConnector

def main():
    mongo = MongoConnector()

    try:
        print("Testing MongoDB connection...")

        if not mongo.connect():
            print("Connection failed. Check the error above.")
            return

        print("Connection successful!")

        telemetry = mongo.get_hourly_telemetry(hours=48)

        if telemetry.empty:
            print("Connected, but no telemetry results were returned.")
        else:
            print(f"Telemetry rows returned: {len(telemetry)}")
            print(telemetry.head(5).to_string(index=False))

    finally:
        mongo.close()

if __name__ == "__main__":
    main()
