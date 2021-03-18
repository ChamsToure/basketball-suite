from flask import Flask, redirect, url_for, render_template, request
from service import *
from exercise import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    max_intensity = SelectField("Level of Intensity - Low(5-7) Medium(8-10) High(11-12)", choices = [(5,5),
                                                                 (6,6),
                                                                 (7,7),
                                                                 (8,8),
                                                                 (9,9),
                                                                 (10,10),
                                                                 (11,11),
                                                                 (12,12)], validators=[DataRequired()])
    categories = SelectField("Categories", choices= [("Ballhandling","Ballhandling"),
                                                  ("Shooting", "Shooting"),
                                                  ("Defense", "Defense")
                                                  ], validators=[DataRequired()])
    submit = SubmitField("Submit")

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "hard to guess string"

test_variable = "Hello Test"
exercises_of_category = create_exercise_list("ballhandling")

@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/training", methods=["GET", "POST"]) #/<string:category>/<int:intensity>")
def training():
    form = NameForm()
    history_sheet = sheet.worksheet("History")
    last_5 = history_sheet.get_all_values()[-5:]#fetches the 5 last items of the history
    last_5.sort(reverse=True) #So that the most recent plans are displayed at the top
    if form.validate_on_submit():
        categories = form.categories.data
        max_intensity = form.max_intensity.data
        return redirect(f"/training-plan/{categories}/{max_intensity}")
    return render_template("training.html", form=form, last_5=last_5)

#Its is the endpoint, when the user clicks on the submit button to  create a new training plan
@app.route("/training-plan/<string:category>/<int:intensity>", methods=["GET", "POST"])
def get_trainingplan(category, intensity):
    list_of_exercises = create_exercise_list(category)#fetches the entire list of exercises for this particular category
    training_plan = Training(category, intensity, list_of_exercises)
    training_plan.create_plan(4)# Creates a Trainingplan with 4 exercises
    training_plan.sort_plan()
    save_plan(training_plan)
    return render_template("training_plan.html", training_plan=training_plan )

@app.route("/profiles")
def profiles():
    return render_template("player_profiles.html")


if __name__ == "__main__":
    app.run(debug=True)
