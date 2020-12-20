def inside_borders(params):
    '''
    Example of rewarding the agent to stay inside the two borders of the track
    '''
    
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    
    # Give a very low reward by default
    reward = -1

    # Give a high reward if no wheels go off the track and 
    # the car is somewhere in between the track borders 
    if all_wheels_on_track:
        reward = 0.50
    
    bonus_reward = ((0.5*track_width)-distance_from_center)/(0.5*track_width)
    if bonus_reward < 0:
        bonus_reward = 0
    elif bonus_reward > .75:
        bonus_reward = 1.25
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
    SPEED_THRESHOLD = 2.75 

    if speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward = 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward = 1.0

    return reward

def faster(params):
    #############################################################################
    '''
    Example of using steps and progress
    '''

    # Read input variable
    steps = params['steps']
    progress = params['progress']
    track_length = params['track_length']
    speed = 1
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = track_length/speed*15


    # Initialize the reward with typical value 
    reward = 0

    # Give additional reward if the car pass every 100 steps faster than expected 
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += 10.0

    return reward

def follow_centerline(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_3 = 0.3 * track_width
    marker_4 = 0.4 * track_width
    marker_5 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.5
    elif distance_from_center <= marker_2:
        reward = 0.8
    elif distance_from_center <= marker_3:
        reward = 0.6
    elif distance_from_center <= marker_4:
        reward = 0.4
    elif distance_from_center <= marker_5:
        reward = 0.2
    else:
        reward = -1  # likely crashed/ close to off track
    
    return float(reward)

def direction_and_waypoint(params):
    ###############################################################################
    '''
    Example of using waypoints and heading to make the car in the right direction
    '''

    import math

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
    # Set Reward Weights
    rewards = {
                'oncenter': {'center':.3,'inside':.3, 'speed':.4, 'direction':0},
                'semicenter': {'center':.2,'inside':.2, 'speed':.2, 'direction':.4},
                'offcenter': {'center':.1,'inside':.1, 'speed':0, 'direction':.8}
               }

    # Read input parameters
    centerline_reward = follow_centerline(params)
    inside_reward = inside_borders(params)
    speed_reward = speed(params)
    direction_reward = direction_and_waypoint(params)
    faster_reward = faster(params)

    return float(centerline_reward+inside_reward+direction_reward+faster_reward)

    # if centerline_reward > 0.6:
    #     return float(rewards['oncenter']['center']*centerline_reward+rewards['oncenter']['inside']*inside_reward+rewards['oncenter']['speed']*speed_reward+rewards['oncenter']['direction']*direction_reward)
    # elif centerline_reward >= 0.4:
    #     return float(rewards['semicenter']['center']*centerline_reward+rewards['semicenter']['inside']*inside_reward+rewards['semicenter']['speed']*speed_reward+rewards['semicenter']['direction']*direction_reward)
    # else:
    #     return float(rewards['offcenter']['center']*centerline_reward+rewards['offcenter']['inside']*inside_reward+rewards['offcenter']['speed']*speed_reward+rewards['offcenter']['direction']*direction_reward)