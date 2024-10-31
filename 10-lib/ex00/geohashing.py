import sys


def print_precision_table():
    # Table of precision levels and the areas they represent
    table = """
    Precision | Geohash Length | Approximate Area Represented
    ---------------------------------------------------------
    1         | 1 character    | ±5,000 km
    2         | 2 characters   | ±1,250 km
    3         | 3 characters   | ±156 km
    4         | 4 characters   | ±40 km
    5         | 5 characters   | ±5 km
    6         | 6 characters   | ±1.2 km
    7         | 7 characters   | ±150 m
    8         | 8 characters   | ±19 m
    9         | 9 characters   | ±5 m
    10        | 10 characters  | ±0.6 m
    """
    return table


def encode_geohash(latitude, longitude, precision=5):

    BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    
    lat_min, lat_max = -90.0, 90.0
    lon_min, lon_max = -180.0, 180.0
    geohash = []
    bit = 0
    ch = 0
    even = True

    while len(geohash) < precision:
        if even:
            mid = (lon_min + lon_max) / 2
            if longitude > mid:
                ch |= 1 << (4 - bit)
                lon_min = mid
            else:
                lon_max = mid
        else:
            mid = (lat_min + lat_max) / 2
            if latitude > mid:
                ch |= 1 << (4 - bit)
                lat_min = mid
            else:
                lat_max = mid

        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash += BASE32[ch]
            bit = 0
            ch = 0

    return ''.join(geohash)


def main():
    if len(sys.argv) != 3:
        print("Usage: python geohashing.py <latitude> <longitude>")
        print("Example: python geohashing.py 37.421542 -122.085589")
        sys.exit(1)

    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        print(print_precision_table())
        precision = int(input("Introduce desired precision\n"))

        geohash_result = encode_geohash(latitude, longitude, precision)
        print("Geohash:", geohash_result)

    except ValueError:
        print("Error: Latitude and longitude must be valid numbers.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
