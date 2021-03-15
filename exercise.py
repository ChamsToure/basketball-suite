import random

class Training:

    def __init__(self, category, intensity, exercise_list):
        self.category = category
        self.intensity = intensity
        self.exercise_list = exercise_list
        self.training_plan = []

        #fetching all the exercises of the category when we construct an object

    def print_training_plan(self):
        print("===========================Hello Chams, this is the Plan for today============================== \n")
        print("Here are some information about the plan for today\n")
        print(f"The category is: {self.category}")
        print(f"The Level of intensity is {self.intensity}")
        print(f"Here is the ist of exercises: \n")
        for i in self.training_plan:
            print(i.name)
            print(i.category)
            print(i.level)
            print(i.description)

    #Sorts the plan, so that the easiest exercise comes first
    def sort_plan(self):
        self.training_plan.sort(key=lambda exercise: exercise.level)

    def check_sum(self, current_training_plan):
        current_sum = 0
        for exercise in current_training_plan:
            current_sum += int(exercise.level)
        return current_sum

    def add_exercises(self, number_of_exercises):
        iteration = 0
        while iteration < number_of_exercises:
            self.training_plan.append(random.choice(self.exercise_list))
            iteration+=1


    def create_plan(self, number_of_exercises):
        correct = False
        while correct == False:
            self.add_exercises(number_of_exercises)
            if self.check_sum(self.training_plan) == self.intensity :
                correct == True
                return self.training_plan
            else:
                self.training_plan.clear()

class Exercise:

    def __init__(self, name, category, level, description):
        self.name = name
        self.category = category
        self.level = level
        self.description = description
