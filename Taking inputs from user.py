import csv
import pandas as pd

# Allow users to input Venues and store them as a CSV file.
def add_venue():
    venues = [] # List to add venue
    while True:
        venue_name = input("Enter the name of the venue (or 'a' to quit): ")
        if venue_name == 'a':
            break
        capacity = input("Enter the venue's capacity: ")

        # Store Venue and capacity as a dictionary
        Venue = {
            'Venue name': venue_name,
            'Capacity': capacity
        }

        # Open the CSV file in append mode and store the venue information
        with open('list_of_venues.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=Venue.keys())

            # Check if the file is empty and write the header if needed
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(Venue)

        print("Venue and capacity stored successfully!")

# Allow users to enter Courses and store them as a CSV file
def add_courses():
    courses = [] # List to store courses
    while True:  
        course = input("Enter the course name (or 'a' to quit): ")
        if course == 'a':
            break

        # Store courses as a dictionary
        course_dict = {
            'courses': course
        }

        # Open the CSV file in append mode and store the course information
        with open("courses.csv", 'a', newline="") as file:
            writer = csv.DictWriter(file, fieldnames=course_dict.keys())

            writer.writerow(course_dict)

        print("Courses stored successfully!")

# Call the functions to execute the code
add_venue()
add_courses()


