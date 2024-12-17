import numpy as np
import shapely

def get_lat_long_firemap(polygon, lat_lon_array):
    """
    Gets a numpy array based on a polygon
    Arguments:
        polygon: polygon to construct array from
        lat_lon_array: numpy array showing lat lon coordinates of points in array
    """
    arr = np.zeros(lat_lon_array.shape[:2], dtype=np.int32)
    for i in range(lat_lon_array.shape[0]):
        for j in range(lat_lon_array.shape[1]):
            point = lat_lon_array[i, j]
            arr[i, j] = polygon.contains(shapely.Point(point[1], point[0]))
    return arr

def get_historical_firemap(fire_map, polygon, lat_lon_array, prev):
    """
    constructs 3 outputs
        simulator burned map
        historical burned map
        historical mitigations
    Arguments:
        fire_map: simulator fire map
        polygon: polygon showing historical burned area
        lat_lon_array: array mapping firemap location to lat lon coordinate
        prev: previous historical fire_map
    """
    hist_fire_map = get_lat_long_firemap(polygon, lat_lon_array)
    hist_fire_map = (hist_fire_map != 0)
    hist_fire_map = np.logical_or(hist_fire_map, prev)

    sim_damaged_map = fire_map != 0
    sim_mitigated_map = fire_map >= 3
    sim_burned_map = np.logical_and(sim_damaged_map, (1-sim_mitigated_map))
    return sim_burned_map, hist_fire_map, sim_mitigated_map

def get_historical_error(sim, historical_layer, metrics, fire_name="", get_fire_map=lambda x: x.fire_map):
    """
    logs historical metrics and produces visualization of historical/simulated fire
    Arguments:
        sim: simulator to use
        historical_layer: historical layer of config
        metrics: metrics object to use for logging
    """
    sim.reset()
    # Array to store images for animation
    # 3 channels:
        # simulated burn map
        # historical burn map
        # historical mitigations
    diff_arr = np.zeros((len(historical_layer.polygons_df["DateTime"]), *sim.fire_map.shape, 3), dtype=np.uint8)
    polygons_df = historical_layer.polygons_df.sort_values(by="DateTime", ascending=True)
    current_time = historical_layer.convert_to_datetime(historical_layer.start_time)
    prev = np.zeros(sim.fire_map.shape, dtype=np.int32)
    for i, (next_time, polygon) in enumerate(zip(polygons_df.DateTime, polygons_df.geometry)):
        # loop through each time/polygon and construct resulting firemaps, run simulator for time diff
        time_diff = next_time - current_time
        mitigation_points = historical_layer.get_mitigations_by_time(
            current_time,
            current_time + time_diff,
        )
        # update historical mitigations in simulator
        sim.update_mitigation(mitigation_points)
        # run simulator for delta t
        sim.run(int(time_diff.total_seconds() / 60))
        fire_map, hist_fire_map, mitigations = get_historical_firemap(
            get_fire_map(sim),
            polygon,
            historical_layer.lat_lon_array,
            prev,
        )
        diff_arr[i] = np.stack([fire_map, hist_fire_map, mitigations], axis=-1)
        prev = hist_fire_map

        # diff is area where burn maps don't match
        neq_fire_map = fire_map != hist_fire_map
        union_fire_map = np.logical_or(fire_map, hist_fire_map)
        intersect_fire_map = np.logical_and(fire_map, hist_fire_map)
        diff_fire_map = fire_map != intersect_fire_map
        total_area = fire_map.shape[0] * fire_map.shape[1]


        metrics.log_metrics(
                total_error=np.sum(neq_fire_map)/total_area,
                normalized_error=np.sum(neq_fire_map) / np.sum(union_fire_map),
                false_positive_error=np.sum(diff_fire_map) / np.sum(fire_map),
                false_negative_error=np.sum(intersect_fire_map) / np.sum(hist_fire_map),
                time=next_time,
                fire_name=fire_name,
        )
        current_time = next_time
    return diff_arr
