import pandas as pd
from prettytable import PrettyTable


courses = pd.read_csv("courses.csv")
list_of_venues = pd.read_csv("list_of_venues.csv").to_dict("records")
#yes
#print(list_of_venues)



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

def append_to_venue_result_list(val,courses,venue,venue_result_list):
    val["venue"] = venue['name']
    val["venue_capacity"] = venue['capacity']
    venue_result_list.append(val)
    return 

def timetable():

    courses["start_time"] = courses["start_time"].apply(split_data_and_return_time)
    courses["finish_time"] = courses["finish_time"].apply(split_data_and_return_time)
    sorted_courses = courses.sort_values(by=['finish_time'], ignore_index=True)

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

    #covert the table to excel format
    df = pd.DataFrame.from_dict(venue_result_list)
    print(df)
    df.to_excel('timetable.xlsx')
# to add new course and venue when starting the app 
venue_prompt = input('do you want to add more venue yes or no')
venue_prompt = venue_prompt.lower()
if venue_prompt=='yes':
    venlist={}
    venueid= input('enter venue name').upper()
    venuecap= int(input('enter venue capacity'))
    venlist.update({'name':venueid},)
    venlist.update({'capacity':venuecap})
    list_of_venues.append(venlist)
    print(list_of_venues)
    course_prompt = input('do you want to add more courses yes or no')
    course_prompt = venue_prompt.lower()
    if course_prompt=='yes':
        courselist=[]
        course_code= input('enter course code').upper()
        startt= (input('enter start time'))
        finisht= (input('enter start time'))
        size = int(input('enter class size'))
        courselist.extend([course_code,startt,finisht,size])
        courses.loc[len(list_of_venues)] = courselist
        timetable() 
    elif course_prompt =='no':
        timetable()

elif venue_prompt=='no':
    course_prompt = input('do you want to add more courses yes or no').lower()
    if course_prompt=='yes':
        courselist=[]
        course_code= input('enter course code').upper()
        startt= (input('enter start time'))
        finisht= (input('enter start time'))
        size = int(input('enter class size'))
        courselist.extend([course_code,startt,finisht,size])
        courses.loc[len(list_of_venues)] = courselist
        timetable() 
    elif course_prompt =='no':
        timetable()
