import gspread
from datetime import date
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
#Change the list of categories to your needs. This is just an example.
categories = ["Fastbreak", "Multipurpose", "Shooting", "Defense", "Offense", "Team-Offense", "Team-Defense", "Athletiktraining", "Ballhandling"]

#The header of the columns
header = sheet.sheet1.row_values(1)
header_length = len(header)

#returns the list of exercises of the category given by cmd line argument
#chosen category from the command line. Must be set to 1 if I pass the category
category = "ballhandling"#sys.argv[1]
max_intensity = 10 #int(sys.argv[2])
def create_exercise_list(the_category):
	list_of_exercise = []
	worksheet = sheet.worksheet(the_category.capitalize())
	rows = worksheet.get_all_values()[1:]
	#iterate over every row in the worksheet and appends it to the list
	for row in rows:
		obj = Exercise(row[0], row[1], row[2], row[3])
		list_of_exercise.append(obj)
	return list_of_exercise

#Add generated training plan to the history
def save_plan(finished_plan):
    index = 1
    today = date.today().strftime("%d/%m/%y")
    exercise_list = [exercise.name for exercise in finished_plan.training_plan]
    worksheet = sheet.worksheet("History")
    items = len(worksheet.col_values(1)) #Gets all values from the first column
    next_entry = items+1
    #Writing to a cell have to be done manually, 
    #because there is no simple and readable way to map each info to its associated cell
    worksheet.update_cell(next_entry, 1, next_entry)
    worksheet.update_cell(next_entry, 2, finished_plan.category)
    worksheet.update_cell(next_entry, 3, exercise_list[0])
    worksheet.update_cell(next_entry, 4, exercise_list[1])
    worksheet.update_cell(next_entry, 5, exercise_list[2])
    worksheet.update_cell(next_entry, 6, exercise_list[3])
    worksheet.update_cell(next_entry, 7, finished_plan.intensity)
    worksheet.update_cell(next_entry, 8, today)
    worksheet.update_cell(next_entry, 9, "No Rating")


