import pandas as pd
from prettytable import PrettyTable

courses = pd.read_csv("courses.csv")
list_of_venues = pd.read_csv("list_of_venues.csv").to_dict("records")

# sorting the venues by capacity
list_of_venues.sort(key = lambda venue: venue["capacity"])

#split the time using colon and returns it as an integer
def split_data_and_return_time(time_str):
    hour = int(time_str.split(":")[0])
    return hour

#checks if the capacity of the venue is greater than the number of students
def check_capacity(venue, no_of_students):
    if venue["capacity"] >= no_of_students:
        return True
    return False

def check_time_clash(i,row,venue_result_list):
    if row["start_time"] >= venue_result_list[i-1]["finish_time"]:
        return True
    return False

def append_to_venue_result_list(val,venue,venue_result_list):
    val["venue"] = venue['name']
    val["venue_capacity"] = venue['capacity']
    venue_result_list.append(val)
    return 

def no_suitable_venue(val, venue_result_list):
    val["venue"] = "No suitable venue"
    val["venue_capacity"] = "null"
    venue_result_list.append(val)
    return
    

def timetable():

    courses["start_time"] = courses["start_time"].apply(split_data_and_return_time)
    courses["finish_time"] = courses["finish_time"].apply(split_data_and_return_time)
    
    # sorting by both finish time and number of students
    sorted_courses = courses.sort_values(by=["finish_time", "no_of_students"], ascending=[True, False], ignore_index=True)

    # creating a copy of the list of venues so we don't mess up the original
    venues_list = [dic.copy() for dic in list_of_venues]

    venue_result_list = []
    for i,row in sorted_courses.iterrows():
        if i == 0:
            for venue in venues_list:
                if check_capacity(venue, row["no_of_students"]) == True:
                    # giving each venue a 'timestamp' which is the finish time of the course currently being written there
                    venue["timestamp"] = row["finish_time"]
                    val = row.to_dict()
                    append_to_venue_result_list(val,venue,venue_result_list)
                    break
        else:
            if check_time_clash(i,row,venue_result_list) == True:
                for venue in venues_list:
                    if check_capacity(venue, row["no_of_students"])== True:
                        val = row.to_dict()
                        append_to_venue_result_list(val,venue,venue_result_list)
                        break
            else:
                for venue in venues_list:
                    if check_capacity(venue, row["no_of_students"]):
                        # if the venue doesn't have a timestamp, it hasn't been used for any course, so use it and assign a timestamp to it
                        if venue.get("timestamp", 0) == 0:
                            venue["timestamp"] = row["finish_time"]
                            val = row.to_dict()
                            append_to_venue_result_list(val,venue,venue_result_list)
                            break
                        # if the venue has a timestamp, check if the start time of the course is less or equal to the time stamp
                        # if it is, assign the course to it, and update the timestamp
                        else:
                            if venue["timestamp"] <= row["start_time"]:
                                val = row.to_dict()
                                append_to_venue_result_list(val,venue,venue_result_list)
                                venue["timestamp"] = row["finish_time"]
                                break
                else:
                    val = row.to_dict()
                    no_suitable_venue(val, venue_result_list)
    
    table = PrettyTable(field_names=venue_result_list[0].keys(), title= "TimeTable with Venues in Sorted order")
    for row in venue_result_list:
        table.add_row(row.values())        
        
    print(table)

    #covert the table to excel format
    df = pd.DataFrame.from_dict(venue_result_list)
    df.to_excel('timetable.xlsx')
   
timetable()


#pending tasks 
