import pandas as pd
from prettytable import PrettyTable

data = pd.read_csv("courses.csv")


def okTimetable():
    '''
    Line 33 and 34 sort both the dictionary and the list of tuples that have been constructed before now
    they both sort their respective data sets
    '''
    data["start_time"] = data["start_time"].apply(lambda x: int(x.split(":")[0]))
    data["finish_time"] = data["finish_time"].apply(lambda x: int(x.split(":")[0]))
    
    data_table = PrettyTable(field_names=data.columns.tolist(), title="Unsorted data")
    for _,row in data.iterrows():
        data_table.add_row(row.values)
    sortedCourses = data.sort_values(by=['finish_time'], ignore_index=True)

    print(data_table)

    with_venues = []
    for i , row in sortedCourses.iterrows():
        if i == 0:
            for venue in list_of_venues:
                if venue['capacity'] >= row["no_of_students"]:
                    val = data.iloc[0].to_dict()
                    val["venue"] = venue['name']
                    with_venues.append(val)
                    break
        else:
            if (row["start_time"] >= with_venues[i-1]["finish_time"]):
                for venue in list_of_venues:
                    if venue["capacity"] >= row["no_of_students"]:
                        val = sortedCourses.iloc[i].to_dict()
                        val["venue"] = venue["name"]
                        with_venues.append(val)
                        break
            else:
                for venue in list_of_venues:
                    if (venue['capacity'] >= row["no_of_students"]) and (with_venues[i-1]["venue"] != venue["name"]):
                        val = sortedCourses.iloc[i].to_dict()
                        val["venue"] = venue["name"]
                        with_venues.append(val)
                        break
    
    table = PrettyTable(field_names=with_venues[0].keys(), title= "TimeTable with Venues in Sorted order")
    for row in with_venues:
        table.add_row(row.values())        
        
    print(table)
    
okTimetable()


#pending tasks 
