# model name: tbone-014
# 
import math

def inside_borders(params):
    '''
    Example of rewarding the agent to stay inside the two borders of the track
    '''
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # Give a very low reward by default
    reward = 0

    # Give a high reward if no wheels go off the track and 
    # the car is somewhere in between the track borders 
    if all_wheels_on_track:
        reward = 0.50
    
    bonus_reward = ((0.5*track_width)-distance_from_center)/(0.5*track_width)
    if bonus_reward > 0.80:
        bonus_reward = bonus_reward * 3.00
    reward += bonus_reward
    # Always return a float value
    return reward

def speed(params):
#############################################################################
    '''
    speed
    '''

    # Read input variables
    speed = params['speed']

    # Set the speed threshold based your action space 
    SPEED_THRESHOLD = 2.00 

    # if speed < SPEED_THRESHOLD:
    #     # Penalize if the car goes too slow
    #     reward = 0.00
    # else:
    #     # High reward if the car stays on track and goes fast
    #     reward = 1.0

    return 1.00 * speed/SPEED_THRESHOLD

def follow_centerline(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center < (track_width * .20):
        reward = 3.0 * (distance_from_center/(track_width*.50))
    else:
        reward = 0  # likely crashed/ close to off track
    
    return float(reward)

def direction_and_waypoint(params):
    ###############################################################################
    '''
    Example of using waypoints and heading to make the car in the right direction
    '''



    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize the reward with typical value 
    reward = 1.0

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    WTF_DIRECTION = 20.0
    UHOH_DIRECTION = 15.0
    CHECKENGINE_DIRECTION = 10.0
    if direction_diff > WTF_DIRECTION:
        reward *= 0.05
    elif direction_diff > UHOH_DIRECTION:
        reward *= 0.25
    elif direction_diff > CHECKENGINE_DIRECTION:
        reward *= 0.50
    elif direction_diff < 2.5:
        reward *= 1.50

    return reward


def reward_function(params):
    '''
    Use the weighted reward matrix to generate a reward
    '''
    # Read input parameters
    centerline_reward = follow_centerline(params)
    #inside_reward = inside_borders(params)
    speed_reward = speed(params)
#    direction_reward = direction_and_waypoint(params)

    return float(centerline_reward+speed_reward)