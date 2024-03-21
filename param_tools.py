import math


def get_spn(toponym):
    envpe = toponym["boundedBy"]['Envelope']
    coords_left = list(map(float, envpe['lowerCorner'].split()))
    coords_up = list(map(float, envpe['upperCorner'].split()))
    scope_lst = [abs(coords_left[0] - coords_up[0])] + [abs(coords_left[1] - coords_up[1])]
    return ','.join(map(str, scope_lst))


def get_spn_tp(p1, p2):
    spn = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** .5
    return [spn, spn]


def get_mid_ll(p1, p2):
    llx = (p1[0] + p2[0]) / 2
    lly = (p1[1] + p2[1]) / 2
    return [llx, lly]


def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)

    return distance