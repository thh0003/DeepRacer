# model name: tbone-015
# 
import math

class HISTORY:
    stepsPerSecond = 15
    lookAheadSteps = 3
    prev_speed=None
    prev_steering_angle=None
    prev_steps=None
    prev_direction_diff=None
    prev_distance_centerline=None
    prev_location=[0.00,0.00]
    step_duration = float(1 / stepsPerSecond)
    prev_total_reward = None
    prev_heading = None
    prev_closest_waypoints = None

class RaceStep:
    def __init__(self, stepParams, params):
        self.location = stepParams["location"]
        self.closest_waypoints = getClosestWaypoints(self.location, stepParams, params)
        self.distance_from_center = calcDistanceFromCenter(self.closest_waypoints,self.location,stepParams,params)
        self.stepReward = self.calcStepReward(stepParams, params)
        self.stepNumber = stepParams["stepNumber"]

    def calcStepReward(self, stepParams, params):


def calcDistanceFromCenter(closest_waypoints,location,stepParams, params):
    waypoints = params["waypoints"]
    segGH = (location[1]-closest_waypoints[0][1])
    segOG = (location[0]-closest_waypoints[0][0])
    stepHeading = params["heading"]
    wayPointY = waypoints[1][1]-waypoints[0][1]
    wayPointX = waypoints[1][0]-waypoints[0][0]
    wayPointZ = math.sqrt((wayPointX ** 2)+(wayPointY ** 2))
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(wayPointY, wayPointX) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    if track_direction > 90 and < 180:
        track_direction = 180 - stepHeading
    elif track_direction > 180 and < 270:
        track_direction = track_direction - 180
    elif track_direction > 270 and < 360:
        track_direction = 360 - track_direction

    if stepHeading > 90 and < 180:
        stepHeading = 180 - stepHeading
    elif stepHeading > 180 and < 270:
        stepHeading = stepHeading - 180
    elif stepHeading > 270 and < 360:
        stepHeading = 360 - stepHeading

    segOH = segGH/math.sin(stepHeading-track_direction) if stepHeading > track_direction else segGH/math.sin(track_direction - stepHeading)
    segHZ = math.sin(stepHeading-track_direction) * segOH if stepHeading > track_direction else math.sin(track_direction-stepHeading-) * segOH
    print("calcDistance: track_direction: "+str(track_direction+", stepHeading: "+str(stepHeading+", segOH: "+str(segOH)+", segHZ: "+str(segHZ))
    return segHZ

def getClosestWaypoints(location,stepParams, params):
    waypoints=params["waypoints"]
    startWaypoints = params["closest_waypoints"]
    curClosestWaypointIndex = startWaypoints[0]
    curClosestDistance = 100
    posHeading = True if params["heading"] < 90 or params["heading"] > 270 else False
    for num, waypoint in enumerate(params["waypoints"], start=curClosestWaypointIndex):
        xSQ = abs(waypoint[0]-location[0]) ** 2
        ySQ = abs(waypoint[1]-location[1]) ** 2
        z = math.sqrt((xSQ+ySQ))
        curClosestDistance = z if z < curClosestDistance else curClosestDistance
        curClosestWaypointIndex = num if z < curClosestDistance else curClosestWaypointIndex

    if posHeading:
        if waypoints[curClosestWaypointIndex][0]>location[0]:
            return (curClosestWaypointIndex-1,curClosestWaypointIndex)
        else:
            return (curClosestWaypointIndex,curClosestWaypointIndex+1)
    else:
        if waypoints[curClosestWaypointIndex][0]>location[0]:
            return (curClosestWaypointIndex,curClosestWaypointIndex-1)
        else:
            return (curClosestWaypointIndex-1,curClosestWaypointIndex)

def getDistanceCenterLine (track_width, distance_from_center):
    # Read input parameters
    delta = (track_width*.50)-distance_from_center
    return delta

def reward_function(params):
    '''
    Use the weighted reward matrix to generate a reward
    
    '''
    # Create Steps to Evaluate
    steps = []
    curStep=2
    steps[0] = RaceStep({
        "location": HISTORY.prev_location,
        "speed": HISTORY.prev_speed,
        "distance_centerline": HISTORY.prev_distance_centerline,
        "direction_diff": HISTORY.prev_direction_diff,
        "heading": HISTORY.prev_heading,
        "stepNumber":0
        "waypointIndex":
    }, params)
        
    steps[1] = RaceStep({
        "location": (params["x"],params["y"]),
        "speed": params["speed"],
        "distance_centerline": params["distance_from_center"]
        "direction_diff": getDirectionDiff(params),
        "heading": params["heading"],
        "stepNumber":1
    }, params)

    HISTORY.prev_location = steps[1].location
    HISTORY.prev_speed=params["speed"]
    HISTORY.prev_steering_angle=params["steering_angle"]
    HISTORY.prev_steps=params["steps"]
    HISTORY.prev_direction_diff=steps[1].direction_diff
    HISTORY.prev_distance_centerline=params["distance_from_center"]
    HISTORY.prev_total_reward = steps[1].total_reward
    HISTORY.prev_heading = params["heading"]

    while curStep < HISTORY.lookAheadSteps+1:
        stepLocation = getCurLocation((HISTORY.step_duration * curStep),params)
        steps[curStep] = RaceStep({
            "location": stepLocation,
            "speed": params["speed"],
            "distance_centerline": None
            "direction_diff": None,
            "heading": params["heading"],
            "stepNumber":curStep            
        })
        curStep+=1

    centerline_reward = follow_centerline(params)
    #inside_reward = inside_borders(params)
    speed_reward = speed(params)
    direction_reward = direction_and_waypoint(params)
    curProg = progress(params)
    print("CenterLine: "+str(centerline_reward)+" Direction Reward: "+str(direction_reward)+"Progress: "+str(curProg)+" Speed: "+str(speed_reward))
    return float(centerline_reward+speed_reward+direction_reward+curProg+speed_reward)
    #return float(centerline_reward)

def getCurLocation(stepDuration, params):
    stepHypo = stepDuration * params["speed"]
    stepOpp = math.sin(params["Heading"]) * stepHypo
    stepAdj = math.cos(params["Heading"]) * stepHypo
    x = stepAdj + params["x"]
    y = stepOpp + params["y"]
    print("step location: "+ str(x) + ", " + str(y))
    return (x,y)

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
    SPEED_THRESHOLD = 2.00 

    # if speed < SPEED_THRESHOLD:
    #     # Penalize if the car goes too slow
    #     reward = 0.00
    # else:
    #     # High reward if the car stays on track and goes fast
    # 
    #     reward = 1.0
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
    #elif: distance_from_center < (track_width * .50):
    else:
        reward = 3.0 * ((delta/(track_width*.50)) ** 3)
    # else:
    #     reward = 0  # likely crashed/ close to off track
    
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
    # WTF_DIRECTION = 20.0
    # UHOH_DIRECTION = 15.0
    # CHECKENGINE_DIRECTION = 10.0
    # if direction_diff > WTF_DIRECTION:
    #     reward *= 0.05
    # elif direction_diff > UHOH_DIRECTION:
    #     reward *= 0.25
    # elif direction_diff > CHECKENGINE_DIRECTION:
    #     reward *= 0.50
    # elif direction_diff < 2.5:
    #     reward *= 1.50
    print("Heading: "+str(heading)+", Track Direction: "+str(track_direction))
    reward = float(reward * (((180-direction_diff)/180)**3))
    return reward


def reward_function(params):
    '''
    Use the weighted reward matrix to generate a reward
    '''
    #print(params)
    # Read input parameters
    centerline_reward = follow_centerline(params)
    #inside_reward = inside_borders(params)
    speed_reward = speed(params)
    direction_reward = direction_and_waypoint(params)
    curProg = progress(params)
    print("CenterLine: "+str(centerline_reward)+" Direction Reward: "+str(direction_reward)+"Progress: "+str(curProg)+" Speed: "+str(speed_reward))
    return float(centerline_reward+speed_reward+direction_reward+curProg+speed_reward)
    #return float(centerline_reward)