## Tourist Guide to finding Low Risk Restuarants in Chicago to eat.

Being a food and hodophilee,or simply Epicurista! I’m always excited about visiting new places and enjoying great food and wine everywhere around the world.
Finding a low risk restaurants has always been important to me, due to food sensitivities and intolerances, as a result I have a  very sensitve stomach.
The aim of this project is to conduct an exploratory data analysis on the Food Inspectionn data set from the city of Chicago data portal.
This information is derived from inspections of restaurants and other food establishments in Chicago from January 1, 2010 to the present. Inspections are performed by staff from the Chicago Department of Public Health’s Food Protection Program using a standardized procedure.

## DATASET
- 17 coloumns

- Original dataset 278K rows,I am only using the first 1000 rows

- Each row-Food Inspection

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
