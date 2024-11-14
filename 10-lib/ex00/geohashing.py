import sys
import antigravity


def antigrav():
    # Check if we have at least 3 arguments (script name + 3 parameters)
    if len(sys.argv) != 4:
        print("Error: Invalid number of arguments")
        print("Usage: python3 geohashing.py <latitude> <longitude> <datedow>")
        sys.exit(1)
    
    try:
        # Convert latitude and longitude to float
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        datedow = sys.argv[3]
        
        # Validate latitude and longitude ranges
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")
        
        # Calculate and display geohash
        antigravity.geohash(latitude, longitude, datedow.encode())
        
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    antigrav()
