def add_trip_ids(points):
    trip_id = -1
    last_occupancy = -1
    converted_points = []

    for point in points:
        occupancy = point[5]

        if last_occupancy != occupancy:
            last_occupancy = occupancy
            trip_id += 1

        converted_point = point[:1] + (trip_id,) + point[1:]
        converted_points.append(converted_point)

    return converted_points
