# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import pandas as pd   
import numpy as np 
import gspread
import csv
import openpyxl
import random
import matplotlib.pyplot as plt
import seaborn as sns

from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('FoodInspections')

foodInspection1 = SHEET.worksheet('foodInspection1')

data = foodInspection1.get_all_values()

print(data)

dataframe = pd.DataFrame(foodInspection1.get_all_records())
print(dataframe)
type(dataframe)
dataframe.head()
dataframe.columns
dataframe.shape
dataframe1 = dataframe.drop('Latitude',axis = 1)
dataframe2 = dataframe1.drop('Longitude',axis =1)
sum(dataframe2['DBA Name'].isnull())  #check the number of nulls / NaNs in the dataset
sum(dataframe2['AKA Name'].isnull())  #check the number of nulls / NaNs in the column.
dataframe2 = dataframe2.rename(columns={'DBA Name': 'DBA_name', 'AKA Name': 'AKA_name'}) #change names of the first two columns,some functions wont work because of the white space between the names
dataframe2.DBA_name.unique().ravel()
dataframe2.AKA_name = dataframe2.AKA_name.fillna(value= dataframe2.DBA_name) # where you have an  empty string in AKAName replace with DBA Name.
sum(dataframe2['AKA_name'].isnull())#checking to see if there are any more empty strings in AKA_name column #
dataframe2['AKA_name'].isnull()
print(dataframe2) 
dataframe2.replace(['MC DONALD'], ["MCDONALD'S"])#Correct spelling 
dataframe3 = dataframe2.replace(['MCDONALDS'], ["MCDONALD'S"])
dataframe4=dataframe3.replace(['KFC'], ['KENTURKY FRIED CHICKEN'])
dataframe5=dataframe4.replace(['MC DONALD restaurant','STARBUCKS COFFEE'], ["MCDONALD'S",'STARBUCKS'])
dataframe6=dataframe5.replace('7/11', '7 ELEVEN')
dataframe7=dataframe6.replace('KFC', 'KENTURKY FRIED CHICKEN')
dataframe8=dataframe7.replace(['SUBWAY SANDWICH'], ['SUBWAY'])
M_restaurant=dataframe8['DBA_name'].where(dataframe5['DBA_name'] =='MC DONALD restaurant')#checking to see if code worked.
sum(M_restaurant.isnull())# checking to see if update worked
seven =dataframe8['AKA_name'].where(dataframe6['AKA_name'] == '7/11')
sum(seven.isnull())# checking to see if update worked

#dataframe8.to_csv('Food_InspectionsClean.csv') # save the cleaned dataframe to csv
#foodInspection1 = SHEET.worksheet('foodInspectionClean')

from openpyxl.workbook import Workbook

FoodInspectionCl=dataframe8.to_excel("foodInspectionCl.xlsx")

def update_worksheet(data, worksheet):
    
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

    update_worksheet(dataframe8, foodInspectionClean)

    
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = dataframe8.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()
    plotPerColumnDistribution(dataframe8, 10, 5)
    dataframe8 = dataframe8.rename(columns={'Facility Type': 'Facility_Type', 'Inspection Date': 'Inspection Date',}) #Renaming columns because some functions wont work because of the white space between the names
    dataframe9 = dataframe8[['DBA_name', 'Results', 'Zip']]# Pull out specific columns

    #Next, I’ll explore how many of the recent inspections were Pass and how many were Fail. I’ve considered Pass w/ Conditions as good and No Entry and Not Ready as bad.
UniqueResults=dataframe8.Results.unique()#Retrieve unique values from Results column
CountResults=dataframe8['Results'].value_counts()#count values
CountResults1=CountResults.to_frame()# convert the result which is a series to dataframe
#Result was not what I was expecting, cant plot with this, it's a dictionary like object.I have to create a dataframe manually from the above result.

v={'Unique':['Pass','Fail','Pass w/Conditions','Out of Business','No entry','Not Ready','Business Not Located'],
  'CountResults':['79811','26283','12595','12538','3282','527','56']}
dfv=pd.DataFrame(v,columns = ['Unique','CountResults'])
labels = dfv['Unique']
sizes = dfv['CountResults']
colors = ['turquoise', 'seagreen', 'mediumslateblue', 'palegreen', 'coral']
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
plt.axis('equal')
#I have to create another dataframe,removing the last row, to avoid overlap in visualization and also add a sixth colour
v={'Unique':['Pass','Fail','Pass w/Conditions','Out of Business','No entry'],
  'CountResults':['79811','26283','12595','12538','3282',]}
dfv1=pd.DataFrame(v,columns = ['Unique','CountResults'])
#New dataframe without the last 2 rows.
#Alternatively, the last two rows can be grouped together.
labels = dfv1['Unique']
sizes = dfv1['CountResults']
colors = ['turquoise', 'seagreen', 'mediumslateblue', 'palegreen', 'coral','purple']
plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
plt.axis('equal')
