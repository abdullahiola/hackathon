import pandas as pd
from prettytable import PrettyTable

welcome_text = """
\t\tGroup 2 Hackathon Project
Would you like to:
1.) Proceed to use this program with our csv files
2.) Provide your own courses
3.) Provide your own venues
4.) Provide both courses and venues

Answer with one of the numbers specified above: 
"""

mode = int(input(welcome_text))
if mode == 1:
    pass

if mode == 2 or mode == 4:
    N = int(input("How many courses do you want to enter?: "))
    data = []
    for i in range(N):
        name = input(f"What is the name of course {i+1}: ")
        start = input(f"What is the start time of {name} (24 hour format e.g 14:30): ")
        end = input(f"What is the finish time of {name} (24 hour format e.g 15:30): ")
        students = int(input(f"How many students offer {name} (a plain number e.g 10): "))
        data.append({
            "Course": name,
            "start_time": start,
            "finish_time": end,
            "no_of_students": students
        })
        
    courses_df = pd.DataFrame(data)
    courses_df.to_csv("user_courses.csv", index=False)

if mode == 3 or mode == 4:
    N = int(input("How many venues do you want to enter: "))
    venue_data = []
    for i in range(N):
        name = input(f"What is the name of venue {i+1}: ")
        capacity = int(input(f"What is the capacity of {name} (a plain number e.g 40): "))
        venue_data.append({
            "name": name,
            "capacity": capacity
        })
        
    venues_df = pd.DataFrame(venue_data)
    venues_df.to_csv("user_venues.csv", index=False)

if mode == 2 or mode == 4:
    courses = pd.read_csv("user_courses.csv")
if mode == 3 or mode == 4:
    list_of_venues = pd.read_csv("user_venues.csv").to_dict("records")
elif mode == 1:
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
    val["venue_capacity"] = 0
    venue_result_list.append(val)
    return
    

def timetable():

    courses["start_time"] = courses["start_time"].apply(split_data_and_return_time)
    courses["finish_time"] = courses["finish_time"].apply(split_data_and_return_time)
    
    # sorting by both finish time and number of students
    sorted_courses = courses.sort_values(by=["finish_time", "no_of_students"], ascending=[True, True], ignore_index=True)

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
    if mode != 1:
        df.to_excel('user_timetable.xlsx')
    else:
        df.to_excel('timetable.xlsx')
   
timetable()