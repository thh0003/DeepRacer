from tboneDeepRacerUtils import calcDistanceFromCenter, getClosestWaypoints, getDistanceCenterLine,getCurLocation,inside_borders,speed,progress,direction_and_waypoint,follow_centerline

class RaceStep:
    def __init__(self, stepParams, params, stepNum, HISTORY):
        self.HISTORY = HISTORY
        if stepNum == 0:
            self.location = HISTORY.prev_location 
            self.closest_waypoints = HISTORY.prev_closest_waypoints if HISTORY.prev_closest_waypoints != None else (0,1)
            print("closest_waypoints: "+str(self.closest_waypoints))
            self.distance_from_center = HISTORY.prev_distance_centerline if HISTORY.prev_distance_centerline != None else 0.00
            print("distance_from_center: "+str(self.distance_from_center))
            self.onTrack = True if (params["track_width"]*.5)>self.distance_from_center else False
            self.stepReward = self.calcStepReward(stepParams, params) if self.onTrack else 0
            self.stepNumber = stepParams["stepNumber"]
        elif stepNum == 1:
            self.location = stepParams["location"]
            self.closest_waypoints = params["closest_waypoints"]
            print("closest_waypoints: "+str(self.closest_waypoints))
            self.distance_from_center = params["distance_from_center"]
            print("distance_from_center: "+str(self.distance_from_center))
            self.onTrack = True if (params["track_width"]*.5)>self.distance_from_center else False            
            self.stepReward = self.calcStepReward(stepParams, params) if self.onTrack else 0
            self.stepNumber = stepParams["stepNumber"]
        else:
            self.location = stepParams["location"]
            self.closest_waypoints = getClosestWaypoints(self.location, stepParams, params)
            print("closest_waypoints: "+str(self.closest_waypoints))
            self.distance_from_center = calcDistanceFromCenter(self.closest_waypoints,self.location,stepParams,params)
            print("distance_from_center: "+str(self.distance_from_center))
            self.onTrack = True if (params["track_width"]*.5)>self.distance_from_center else False
            self.stepReward = self.calcStepReward(stepParams, params) if self.onTrack else 0
            self.stepNumber = stepParams["stepNumber"]

    def calcStepReward(self, stepParams, params):
        rewardParams = params.copy()
        rewardParams["distance_from_center"] = self.distance_from_center
        rewardParams["closest_waypoints"]= self.closest_waypoints
        centerline_reward = follow_centerline(rewardParams)
        #inside_reward = inside_borders(rewardParams)
        #speed_reward = speed(rewardParams)
#        direction_reward = direction_and_waypoint(rewardParams)
#        curProg = progress(rewardParams)
        #print("CenterLine: "+str(centerline_reward)+" Direction Reward: "+str(direction_reward)+"Progress: "+str(curProg))
        #print("CenterLine: "+str(centerline_reward)+" Direction Reward: "+str(direction_reward)+" Speed: "+str(speed_reward))
        #print("CenterLine: "+str(centerline_reward))
#        return float(centerline_reward+direction_reward+curProg)
        return float(centerline_reward)