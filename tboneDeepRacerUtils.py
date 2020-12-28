import math

def calcDistanceFromCenter(closest_waypoints,location,stepParams, params):
    waypoints = params["waypoints"]
    segGH = (location[1]-waypoints[closest_waypoints[0]][1]) if closest_waypoints[0] != -1 else (location[1]-waypoints[0][1])
    segOG = (location[0]-waypoints[closest_waypoints[0]][0]) if closest_waypoints[0] != -1 else (location[1]-waypoints[0][0])
    stepHeading = params["heading"]
    # print("Closest Waypoints: ")
    # print(str(closest_waypoints))
    wayPointY = waypoints[closest_waypoints[1]][1]-waypoints[closest_waypoints[0]][1]
    wayPointX = waypoints[closest_waypoints[1]][0]-waypoints[closest_waypoints[0]][0]
    wayPointZ = math.sqrt((wayPointX ** 2)+(wayPointY ** 2))
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(wayPointY, wayPointX) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    if track_direction > 90 and track_direction < 180:
        track_direction = 180 - stepHeading
    elif track_direction < -90 and track_direction > -180:
        track_direction = track_direction + 180

    if stepHeading > 90 and stepHeading < 180:
        stepHeading = 180 - stepHeading
    elif stepHeading < -90 and stepHeading > -180:
        stepHeading = stepHeading + 180
    if stepHeading != track_direction:
        segOH = segGH/math.sin(stepHeading-track_direction) if stepHeading > track_direction else segGH/math.sin(track_direction - stepHeading)
        segHZ = math.sin(stepHeading-track_direction) * segOH if stepHeading > track_direction else math.sin(track_direction-stepHeading) * segOH 
    else:
        segOH = 0
        segHZ = 0
    print("calcDistance: track_direction: "+str(track_direction)+", stepHeading: "+str(stepHeading)+", segOH: "+str(segOH)+", segHZ: "+str(segHZ))
    return segHZ

def isPOSHeading(currentHeading):
	return True if currentHeading < 90 or currentHeading > -90 else False

def getClosestWaypoints(location,stepParams, params):
    waypoints=params["waypoints"]
    startWaypoints = params["closest_waypoints"]
    # print("startWaypoints: ")
    # print(startWaypoints)
    curClosestWaypointIndex = startWaypoints[0]
    curClosestDistance = 100
    posHeading = True if params["heading"] < 90 or params["heading"] > -90 else False
    for num, waypoint in enumerate(params["waypoints"]):
#        print("index: "+str(num)+" waypoint: "+str(waypoint)+" location: "+str(location))
        xSQ = abs(waypoint[0]-location[0]) ** 2
        ySQ = abs(waypoint[1]-location[1]) ** 2
        z = math.sqrt((xSQ+ySQ))
#        print("waypoint distance: "+str(z))
        if z < curClosestDistance:
            curClosestDistance = z
            curClosestWaypointIndex = num
 #   print("curClosestWaypointIndex: "+str(curClosestWaypointIndex)+" location: "+str(location))
    if posHeading:
        if waypoints[curClosestWaypointIndex][0]>location[0]:
            return (curClosestWaypointIndex-1,curClosestWaypointIndex) # if curClosestWaypointIndex > 0 else (0,curClosestWaypointIndex)
        else:
            return (curClosestWaypointIndex,curClosestWaypointIndex+1)
    else:
        if waypoints[curClosestWaypointIndex][0]>location[0]:
            return (curClosestWaypointIndex,curClosestWaypointIndex-1) # if curClosestWaypointIndex > 0 else (curClosestWaypointIndex,0)
        else:
            return (curClosestWaypointIndex-1,curClosestWaypointIndex) # if curClosestWaypointIndex > 0 else (0,curClosestWaypointIndex)

def getDistanceCenterLine (track_width, distance_from_center):
    # Read input parameters
    delta = (track_width*.50)-distance_from_center
    return delta

def getCurLocation(stepDuration, params):
    stepHypo = stepDuration * params["speed"]
	futureHeading = params["heading"]
	if isPOSHeading(params["heading"]):
		futureHeading = params["heading"] + params["steering_angle"]
	else:
		futureHeading = params["heading"] - params["steering_angle"]

    stepOpp = math.sin(futureHeading) * stepHypo
    stepAdj = math.cos(futureHeading) * stepHypo
    x = stepAdj + params["x"]
    y = stepOpp + params["y"]
    print("step location: "+ str(x) + ", " + str(y))
    return [x,y]

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
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    # Set the speed threshold based your action space 
    SPEED_THRESHOLD = 4.00 

    if distance_from_center < (track_width * .10):
        return 1.00 * ((speed/SPEED_THRESHOLD) ** 3)
    else:
        return 0

def progress(params):
    prog = params["progress"]
    print("Progress: "+str(prog))
    return float(1.5 * ((prog/100)**3))

def follow_centerline(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    delta = (track_width*.50)-distance_from_center
#    print("Delta: "+str(delta)+", track width: "+str(track_width))
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center == 0:
        reward = 3.0
    else:
        reward = 3.0 * ((delta/(track_width*.50)) ** 3)
    
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
    reward = 3.0

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
    print("Heading: "+str(heading)+", Track Direction: "+str(track_direction))
    reward = float(reward * (((180-direction_diff)/180)**3))
    return reward