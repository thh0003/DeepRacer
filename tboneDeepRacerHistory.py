class HISTORY:
    stepsPerSecond = 16
    lookAheadSteps = 5
    prev_speed=None
    prev_steering_angle=None
    prev_steps=None
    prev_distance_centerline=None
    prev_location=[0.00,0.00]
    step_duration = float(1 / stepsPerSecond)
    prev_total_reward = None
    prev_heading = None
    prev_closest_waypoints = None
