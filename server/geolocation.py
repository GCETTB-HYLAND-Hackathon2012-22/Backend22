# Resource -> https://www.geeksforgeeks.org/program-distance-two-points-earth/

from math import radians, cos, sin, asin, sqrt, inf

def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    '''Calculates approx. distance ( in K.M ) between 2 places on the Earth based on Latitude and Longitude'''

    # Degrees to Radians
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # Calculate the result
    return (c * r)


def distance_or_Inf(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    if lat1 is None or lat1 is None or lat1 is None or lat1 is None:
        return inf
    return distance(lat1, lon1, lat2, lon2)


# DEBUG
if __name__ == '__main__':
    lat1 = 53.32055555555556
    lat2 = 53.31861111111111
    lon1 = -1.7297222222222221
    lon2 = -1.6997222222222223
    print(distance(lat1, lon1, lat2, lon2), "K.M")