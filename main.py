from flask import Flask, redirect, url_for, render_template, request
from service import *
from exercise import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    #name = StringField("What is the name of the category?", validators=[DataRequired()])
    #level = IntegerField("Type in a Max in",default = 0,  validators=[DataRequired()])
    max_intensity = SelectField("Level of Intensity", choices = [(5,5),
                                                                 (6,6),
                                                                 (7,7),
                                                                 (8,8),
                                                                 (9,9),
                                                                 (10,10),
                                                                 (11,11),
                                                                 (12,12),
                                                                 (13,13),
                                                                 (14,14),
                                                                 (15,15)], validators=[DataRequired()])
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

@app.route("/test/<string:category>")
def test(category):
    exercises_of_category = create_exercise_list(category)
    training_plan = Training_plan(category, 10, exercises_of_category)
    training_plan.create_plan(4)
    #training_plan.print_training_plan()
    test = training_plan.training_plan[0].name
    return f"<h1>  </h1>"

@app.route("/training", methods=["GET", "POST"]) #/<string:category>/<int:intensity>")
def training():
    #name = None
    #level = None
    form = NameForm()
    if form.validate_on_submit():
        #name = form.name.data
        #level = form.level.data
        categories = form.categories.data
        max_intensity = form.max_intensity.data
        return redirect(f"/training-plan/{categories}/{max_intensity}")
#    exercises_list = create_exercise_list(category)
#    training_plan = Training_plan(category, intensity, exercises_list)
#    training_plan.create_plan(4)
#    test = training_plan.training_plan[0].name
    return render_template("training.html", form=form)#name=training_plan

#Its is the endpoint, when the user clicks on the submit button to  create a new training plan
@app.route("/training-plan/<string:category>/<int:intensity>", methods=["GET", "POST"])
def get_trainingplan(category, intensity):
    list_of_exercises = create_exercise_list(category)#fetches the entire list of exercises for this particular category
    training_plan = Training_plan(category, intensity, list_of_exercises)
    training_plan.create_plan(4)# Creates a Trainingplan with 4 exercises
    return render_template("training_plan.html", training_plan=training_plan )

@app.route("/profiles")
def profiles():
    return render_template("player_profiles.html")

if __name__ == "__main__":
    app.run(debug=True)
