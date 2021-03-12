import gspread
import docx
import sys
from oauth2client.service_account import ServiceAccountCredentials
from exercise import *

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

#validating credentials and open the sheet with all the exercises
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(creds)
sheet = gc.open("exercises")

#listing all the categories existing in my trainings and so that I can iterate over
categories = ["Fastbreak", "Multipurpose", "Shooting", "Defense", "Offense", "Team-Offense", "Team-Defense", "Athletiktraining", "Ballhandling"]

#The header of the columns
header = sheet.sheet1.row_values(1)
header_length = len(header)

#returns the list of exercises of the category given by cmd line argument
#chosen category from the command line. Must be set to 1 if I pass the category
category = "ballhandling"#sys.argv[1]
max_intensity = 10 #int(sys.argv[2])
print(f"The max intensity is {max_intensity}")
def create_exercise_list(the_category):
	list_of_exercise = []
	worksheet = sheet.worksheet(the_category.capitalize())
	rows = worksheet.get_all_values()[1:]
	#iterate over every row in the worksheet and appends it to the list
	for row in rows:
		obj = Exercise(row[0], row[1], row[2], row[3])
		list_of_exercise.append(obj)
	return list_of_exercise

exercises_of_category = create_exercise_list(category)#sys.argv[1]

training_plan = Training_plan(category, max_intensity, exercises_of_category)
training_plan.create_plan(4)

training_plan.print_training_plan()



