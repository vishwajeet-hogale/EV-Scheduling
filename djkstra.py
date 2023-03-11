from all_details import *
from datetime import datetime,timedelta
stations_map = {}
def convert_time_to_datetime_obj(time):
    try:
        return datetime.strptime(time, '%I:%M%p')
    except:
        return time
def dischargeRate (batteryCapacity, dischargeTime):
    dis_rate = batteryCapacity/ dischargeTime
    return dis_rate
def new_battery_capacity(batteryCapacity, dis_rate):
    # new_capacity = (batteryCapacity([i] - dis_rate for [i] in batteryCapacity))
    new_capacity = batteryCapacity - dis_rate
    return new_capacity
def driveTime (currentDistanceSinceLastCharge, Avg_speed) :
    dr_time = (currentDistanceSinceLastCharge / Avg_speed)
    return dr_time
def arrival_time(startTime, dr_time):
    arrivalTime = startTime + dr_time
    return arrivalTime
def departure_time (arrivalTime, parkingTime):
    departureTime = arrivalTime + parkingTime
    return departureTime
def selectCurrentVertex(vis,dis):
    new_list = []
    for i,j in enumerate(zip(vis,dis)):
        if j[0] == 0:
            new_list.append([j[0],j[1],i])
    new_list = sorted(new_list,key = lambda x: (x[0],x[1]))
    return int(new_list[0][2])
def charge_left_after_reaching_station(curr_charge,totalBatteryLife,distanceTravelled,distanceTravelledToStation):
    battery_left = totalBatteryLife - curr_charge
    constant = distanceTravelled/curr_charge
    charge_consumed = curr_charge + distanceTravelledToStation/constant
    return charge_consumed
def distance_to_empty(curr_charge,totalBatteryLife,distanceTravelled):
    battery_left = totalBatteryLife - curr_charge
    constant = distanceTravelled/curr_charge
    return constant*battery_left
def djkstra(graph,n,dis,vis,parent):
    for i in range(n):
        curr = selectCurrentVertex(vis,dis)
        vis[curr] = 1
        for child in range(n):
            if graph[curr][child] != 0 and child != curr and not vis[child] and dis[curr] != 10000:
                if (dis[curr] + graph[curr][child]) < dis[child]:
                    parent[child] = curr
                    dis[child] = dis[curr] + graph[curr][child]
    return [parent,dis]
def get_all_charging_station_from_source(startingPosition,chargingStations,distanceToEmpty):
    distanceFromLocationToChargingStation = {}
    vis = [0 for i in range(n)]
    dis = [10000 for i in range(n)]
    parent = [-1 for i in range(n)]
    dis[startingPosition] = 0
    parent,distance = djkstra(graph,n,dis,vis,parent)
    for i in chargingStations:
        if distance[i] < distanceToEmpty:
            distanceFromLocationToChargingStation[i] = distance[i]
    return distanceFromLocationToChargingStation
def get_closest_station(all_possible_stations,station_details,n):
    temp = {}
    for i in range(n):
        try:
            if(station_details[i]["demand"] != station_details[i]["current_demand"] and station_details[i]["station_no"] in all_possible_stations):
                temp[station_details[i]["station_no"]] = all_possible_stations[station_details[i]["station_no"]]
        except:
            return [[-1,0]],None
    distances = [[i,j] for i,j in temp.items()]
    distances = sorted(distances,key=lambda x:x[1])

    if (len(distances) == 0):
        return [[-1,0]],None
    drive_time = distances[0][1]/60
    return distances,drive_time

def preprocess_all_EVs(ev,distancetostation):
    ev["start_time"] = convert_time_to_datetime_obj(ev["start_time"])
    travel_time_hour = distancetostation//60
    travel_time_mins = distancetostation%60
    arrival_time = ev["start_time"] + timedelta(hours=travel_time_hour) + timedelta(minutes=travel_time_mins)
    ev["arrival_time"] = arrival_time
    charge_left_at_station = charge_left_after_reaching_station(i["usedCapacity"],ev["new_capacity"],i["currentDistanceSinceLastCharge"],distancetostation)
    time_to_charge_hours = (5 * charge_left_at_station )//60
    time_to_charge_mins = (5 * charge_left_at_station )%60
    ev["dept_time"] = ev["arrival_time"] + timedelta(hours=time_to_charge_hours) + timedelta(minutes=time_to_charge_mins + 5)
    return ev
def time_slot_conversion(time_slot):
    option1 = time_slot[0].strftime('%I:%M%p')
    option2 = time_slot[1].strftime('%I:%M%p')
    return [option1,option2]

if __name__ == "__main__":
    # Input matrix is in the form of adjacency matrix
    graph = [
        [0,18,0,9,0],
        [18,0,13,15,7],
        [0,13,0,6,11],
        [9,15,6,0,0],
        [0,7,11,0,0]
        # []
        ]
    n = len(graph)
    """
        Stores all the parent and distances from every location
    """
    no_assigned_station_evs = []
    demand_full_evs = []
    for i in enumerate(Stations):
        stations_map[i[1]["station_no"]] = i[0]
    # Scheduling Evs based on distance : Stations
    for val,i in enumerate(EVs):

        dis_rate = float(dischargeRate(i["batteryCapacity"],i["dischargeTime"]))
        i["dis_rate"] = dis_rate
        new_capacity = float(new_battery_capacity(i["batteryCapacity"],dis_rate))
        i["new_capacity"] = new_capacity
        distanceToEmpty = distance_to_empty(i["usedCapacity"],new_capacity,i["currentDistanceSinceLastCharge"])
        i["distanceToEmpty"] = distanceToEmpty
        all_possible_stations = get_all_charging_station_from_source(i["currentNodeLocation"],[1,3,2],distanceToEmpty)
        if len(all_possible_stations) == 0:
            print("EV ",i["ID"]," No charging stations nearby : Not enough charge")
            i["station_assigned"] = -1
            no_assigned_station_evs.append(i["ID"])
            # continue
        else:
            # print(get_closest_station(all_possible_stations,Stations,3))
            station_distance_assigned,drive_time = get_closest_station(all_possible_stations,Stations,3)#1
            i["distances"] = station_distance_assigned
            station_assigned = station_distance_assigned[0][0]
            EVs[val] = preprocess_all_EVs(i,station_distance_assigned[0][1])
            i["station_assigned"] = station_assigned
            # station_assigned = 
            if station_assigned == -1:
                print("EV ",i["ID"]," No charging stations are available")
                
                i["station_assigned"] = -1
                no_assigned_station_evs.append(i["ID"])
                demand_full_evs.append(i)
                EVs[val] = i
                continue
            # print("EV ",i["ID"]," : ",station_assigned)
            EVs[val] = i
            Stations[stations_map[station_assigned]]["current_demand"] += 1

    # Assign timeslots at each station
    """
    departure_time = driveTime + amount of time taken to charge the ev completely,

    arrival_time = initial_time + drive time 

    Time slot : [arrival_time,departure_time]

    Case : Greedy sort by arrival time to get right time slots
        CaSE I : WHEN IN BETWEEN 
            Case 2 : I should go to the next ev station provided I have charge in my ev? distances[1] < distanceToEmpty : [new_arrival_time,new_dept_time], update the all_details dicts
                Case 2i : I come in between arr and dept : I should wait ? [prev_dept+20secs,dept_time]
        case II : if arrival time greater than prev_dept time 
            Oh peace! I can schedule it here it self.

    Step 1 : Fill out arrival_time,drive_time,dept_time based on charge left
    Step 2 : Sort all ev dicts in ascending order of arrival time 
    Step 3 : if dept < prev_dept :  Perform CaSE I
    Step 4 : else : Case II [arrival_time,dept_time]
    """
    print("############################")
    EVs = [i for i in EVs if i["ID"] not in no_assigned_station_evs]
    EVs = sorted(EVs,key = lambda x:(x["station_assigned"],x["arrival_time"]))
    Stations[stations_map[i["station_assigned"]]]["prev_dept"] = -1
    for val,i in enumerate(EVs):
        # print(i["arrival_time"])
        if Stations[stations_map[i["station_assigned"]]]["prev_dept"] == -1:
            i["time_slot"] = [i["arrival_time"],i["dept_time"]]
            Stations[stations_map[i["station_assigned"]]]["prev_dept"] = i["dept_time"]
            
        elif i["arrival_time"] < Stations[stations_map[i["station_assigned"]]]["prev_dept"] :
            if len(i["distances"]) > 1 :
                option_2_station_distance = i["distances"][1][1]
                time_to_drive_to_option_2 = (option_2_station_distance//60)*60 + option_2_station_distance%60 
                wait_minutes = abs((Stations[stations_map[i["station_assigned"]]]["prev_dept"]-i["arrival_time"]).total_seconds())/60
                if (i["arrival_time"]-i["start_time"]).total_seconds()/60 + wait_minutes > time_to_drive_to_option_2:
                    EVs[val] = preprocess_all_EVs(i,option_2_station_distance)
                    station_assigned = i["distances"][1][0]
                    Stations[stations_map[i["station_assigned"]]]["current_demand"] -= 1
                    i["station_assigned"] = station_assigned
                    i["time_slot"] = [Stations[stations_map[i["station_assigned"]]]["prev_dept"]+timedelta(minutes=5),i["dept_time"]]
                    EVs[val] = i
            i["time_slot"] = [Stations[stations_map[i["station_assigned"]]]["prev_dept"],i["dept_time"]]
        else:
            i["time_slot"] = [i["arrival_time"],i["dept_time"]]
        Stations[stations_map[i["station_assigned"]]]["prev_dept"] = i["dept_time"]
        print("EV ",i["ID"]," ",i["station_assigned"],"-> ",time_slot_conversion(i["time_slot"]))
    demand = 0
    for val,i in enumerate(demand_full_evs):
        demand += 1
        all_possible_stations = get_all_charging_station_from_source(i["currentNodeLocation"],[1,3,2],i["distanceToEmpty"])
        all_poss = sorted([[i,j] for i,j in all_possible_stations.items()],key=lambda x:x[1])
        i["station_assigned"] = all_poss[0][0]

        Stations[stations_map[i["station_assigned"]]]["demand"] += 1
        station_distance_assigned,drive_time = get_closest_station(all_possible_stations,Stations,3)#1
        Stations[stations_map[i["station_assigned"]]]["current_demand"] += 1
        # print("EV ",i["ID"]," : ",station_assigned)
        EVs[val] = i
        if Stations[stations_map[i["station_assigned"]]]["prev_dept"] == -1:
            i["time_slot"] = [i["arrival_time"],i["dept_time"]]
            Stations[stations_map[i["station_assigned"]]]["prev_dept"] = i["dept_time"]
            
        elif i["arrival_time"] < Stations[stations_map[i["station_assigned"]]]["prev_dept"] :
            if len(i["distances"]) > 1 :
                option_2_station_distance = i["distances"][1][1]
                time_to_drive_to_option_2 = (option_2_station_distance//60)*60 + option_2_station_distance%60 
                wait_minutes = abs((Stations[stations_map[i["station_assigned"]]]["prev_dept"]-i["arrival_time"]).total_seconds())/60
                if (i["arrival_time"]-i["start_time"]).total_seconds()/60 + wait_minutes > time_to_drive_to_option_2:
                    EVs[val] = preprocess_all_EVs(i,option_2_station_distance)
                    station_assigned = i["distances"][1][0]
                    Stations[stations_map[i["station_assigned"]]]["current_demand"] -= 1
                    i["station_assigned"] = station_assigned
                    i["time_slot"] = [Stations[stations_map[i["station_assigned"]]]["prev_dept"]+timedelta(minutes=5),i["dept_time"]]
                    EVs[val] = i
            i["time_slot"] = [Stations[stations_map[i["station_assigned"]]]["prev_dept"],i["dept_time"]]
        else:
            i["time_slot"] = [i["arrival_time"],i["dept_time"]]
        EVs[val] = i
        Stations[stations_map[i["station_assigned"]]]["prev_dept"] = i["dept_time"]
        print("EV ",i["ID"]," ",i["station_assigned"],"-> ",time_slot_conversion(i["time_slot"]))   
    
    penalty = 0
    for val,i in enumerate(Stations):
        i["penalty"] = abs(i["current_demand"] - i["demand"])*5 + demand*10
        print(i)   









    



    













     


