# model name: tbone-015
# 
import math
from tboneDeepRacerUtils import calcDistanceFromCenter, getClosestWaypoints, getDistanceCenterLine,getCurLocation,inside_borders,speed,progress,direction_and_waypoint,follow_centerline
from tboneDeepRacerHistory import HISTORY
from tboneDeepRacerRaceStep import RaceStep
import csv

def reward_function(params):
    '''
    Use the weighted reward matrix to generate a reward
    
    '''
    stepRewardsCSV = open ("stepRewards.csv", "a+", newline='')
    stepLocationsCSV = open ("stepLocations.csv", "a+", newline='')

    stepRewardsWriter = csv.writer(stepRewardsCSV)
    stepLocationsWriter = csv.writer(stepLocationsCSV)
    if HISTORY.prev_heading == None:
        with open('trackWaypoints.csv', 'w', newline='') as csvfile:
            csvWriter = csv.writer(csvfile)
            for waypoint in params["waypoints"]:
                csvWriter.writerow(waypoint)

    # Create Steps to Evaluate
    steps = []
    stepLocations = []
    stepRewards = []
    curStep=2
    rewardTotal=0
    stepLocations.append(HISTORY.prev_location)
    steps.append(RaceStep({
        "location": HISTORY.prev_location,
        "speed": HISTORY.prev_speed,
        "distance_centerline": HISTORY.prev_distance_centerline,
        "heading": HISTORY.prev_heading,
        "stepNumber":0
    }, params,0,HISTORY))
    rewardTotal += steps[0].stepReward
    stepRewards.append(steps[0].stepReward)

    stepLocations.append([params["x"],params["y"]])
    steps.append(RaceStep({
        "location": [params["x"],params["y"]],
        "speed": params["speed"],
        "distance_centerline": params["distance_from_center"],
        "heading": params["heading"],
        "stepNumber":1
    }, params,1,HISTORY))
    rewardTotal += steps[1].stepReward
    stepRewards.append(steps[1].stepReward)

    stillOnTrack = True
    
    while curStep < HISTORY.lookAheadSteps+1:
        stepLocation = getCurLocation((HISTORY.step_duration * curStep),params)
        stepLocations.append(stepLocation)
        steps.append(RaceStep({
            "location": stepLocation,
            "speed": params["speed"],
            "distance_centerline": None,
            "heading": params["heading"],
            "stepNumber":curStep            
        }, params,curStep,HISTORY))
        if steps[curStep].onTrack and stillOnTrack:
            rewardTotal += steps[curStep].stepReward
            stepRewards.append(steps[curStep].stepReward)
        else:
            stillOnTrack = False
            rewardTotal += 0
            stepRewards.append(0)
        print("LookAhead Step: "+ str(curStep) +" Award: "+str(rewardTotal))
        curStep+=1
    print("stepLocations: ")
    print(str(stepLocations))
    stepLocationsWriter.writerow(stepLocations)
    print("stepRewards: ")
    print(str(stepRewards))
    stepRewardsWriter.writerow(stepRewards)

    HISTORY.prev_location = [params["x"],params["y"]]
    HISTORY.prev_speed=params["speed"]
    HISTORY.prev_steering_angle=params["steering_angle"]
    HISTORY.prev_steps=params["steps"]
    HISTORY.prev_distance_centerline=params["distance_from_center"]
    HISTORY.prev_heading = params["heading"]
    HISTORY.prev_total_reward = rewardTotal    
    stepRewardsCSV.close()
    stepLocationsCSV.close()

    return float(rewardTotal)

