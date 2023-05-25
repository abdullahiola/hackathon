import pandas as pd

# Define a list of available venues with their capacities
venues = [
    {'name': 'KDLT', 'capacity': 100},
    {'name': 'CLT', 'capacity': 50},
    {'name': 'PGC', 'capacity': 150},
]

# Create an empty DataFrame to store the schedule
columns = ['Course', 'Start-Time', 'Finish-Time', 'Day', 'Capacity', 'Venue']
schedule_df = pd.DataFrame(columns=columns)

def allocate_venue(course, start_time, finish_time, day, capacity):
    # Find a venue that has enough capacity and is available at the scheduled time
    for venue in venues:
        if venue['capacity'] >= capacity:
            available = True
            for _, row in schedule_df.iterrows():
                if day == row['Day'] and venue['name'] == row['Venue'] and \
                   (start_time < row['Finish-Time'] or finish_time > row['Start-Time']):
                    available = False
                    break
            if available:
                venue_name = venue['name']
                schedule_df.loc[len(schedule_df)] = [course, start_time, finish_time, day, capacity, venue_name]
                return venue_name
    return None

while True:
    # Ask the user for input
    course = input("Enter the course: ")
    start_time = input("Enter the start time (HH:MM AM/PM): ")
    finish_time = input("Enter the finish time (HH:MM AM/PM): ")
    day = input("Enter the day: ")
    capacity = int(input("Enter the capacity of the students: "))
  
    # Allocate a venue for the input course
    venue = allocate_venue(course, start_time, finish_time, day, capacity)

    # Display the result
    if venue:
        print(f"The course {course} is scheduled at {venue} on {day} from {start_time} to {finish_time}.")
    else:
        print(f"No suitable venue found for {course} on {day} from {start_time} to {finish_time}.")
        
    another_course = input("Do you want to add another course? (Y/N): ")
    if another_course.lower() == "n":
        if not schedule_df.empty:
            print("\nSchedule Table:\n")
            print(schedule_df.to_string(index=False))
        else:
            print("\nNo courses scheduled.\n")
        break