import pandas as pd
from prettytable import PrettyTable


courses = pd.read_csv("courses.csv")
list_of_venues = pd.read_csv("list_of_venues.csv").to_dict("records")

#split the using colon and returns it as an integer
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

def append_to_venue_result_list(val,courses,venue,venue_result_list):
    val["venue"] = venue['name']
    venue_result_list.append(val)
    return 

def timetable():

    courses["start_time"] = courses["start_time"].apply(split_data_and_return_time)
    courses["finish_time"] = courses["finish_time"].apply(split_data_and_return_time)
    
    unsorted_time_table = PrettyTable(field_names=courses.columns.tolist(), title="Unsorted Table")
    for _,row in courses.iterrows():
        unsorted_time_table.add_row(row.values)
    sorted_courses = courses.sort_values(by=['finish_time'], ignore_index=True)

    print(unsorted_time_table)

    venue_result_list = []

    for i,row in sorted_courses.iterrows():
        if i == 0:
            for venue in list_of_venues:
                if check_capacity(venue, row["no_of_students"]) == True:
                    val = row.to_dict()
                    append_to_venue_result_list(val,courses,venue,venue_result_list)
                    break
        else:
            if check_time_clash(i,row,venue_result_list) == True:
                for venue in list_of_venues:
                    if check_capacity(venue, row["no_of_students"])== True:
                        val = row.to_dict()
                        append_to_venue_result_list(val,courses,venue,venue_result_list)
                        break
            else:
                for venue in list_of_venues:
                    if check_capacity(venue,row["no_of_students"]) == True and (venue_result_list[i-1]["venue"] != venue["name"]):
                        val = row.to_dict()
                        append_to_venue_result_list(val,courses,venue,venue_result_list)
                        break
                    
    
    table = PrettyTable(field_names=venue_result_list[0].keys(), title= "TimeTable with Venues in Sorted order")
    for row in venue_result_list:
        table.add_row(row.values())        
        
    print(table)
    
timetable()


#pending tasks 
