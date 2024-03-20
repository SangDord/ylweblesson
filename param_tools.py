def get_spn(toponym):
    envpe = toponym["boundedBy"]['Envelope']
    coords_left = list(map(float, envpe['lowerCorner'].split()))
    coords_up = list(map(float, envpe['upperCorner'].split()))
    scope_lst = [abs(coords_left[0] - coords_up[0])] + [abs(coords_left[1] - coords_up[1])]
    return ','.join(map(str, scope_lst))