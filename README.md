**Project Title: Autogidas.lt Car Listings Analysis**

**Project Objective:** Collect data about car listings from the website www.autogidas.lt, analyze and visualize the information. Learn to work with real-world data, apply data cleaning and analysis methods, and present insights through various visualizations.

**Project Workflow:**
For the project, we utilized the website www.autogidas.lt, which is freely accessible, and users can access its data. We selected the following data fields: Name, Made, Fuel Type, Mileage, Gearbox, Engine, Power, Location, and Price. Using the BeautifulSoup 4 (bs4) library, we extracted data from the website based on these categories.
- The project file was named autogidas.py, where we performed data loading and transformation.

- At the beginning of the project, we imported the necessary libraries:
 ```
 from bs4 import BeautifulSoup
 import pandas as pd
 import requests
 ```
- Using the requests library, we sent HTTP requests to the website www.autogidas.lt to retrieve the HTML content of the pages.

- The BeautifulSoup library was employed to parse and navigate the HTML content, making it easier to extract specific data from the webpage.

- We utilized the pandas library to organize and manipulate the data in tabular format, creating a DataFrame for further data cleaning.

- The selected data fields, including Name, Made, Fuel Type, Mileage, Gearbox, Engine, Power, Location, and Price, were extracted from the HTML content using BeautifulSoup.

- The extracted data was then cleaned, processed, transformed, and stored in an excel file named 'autogidas_listings_final.xlsx' in 'files' directory for further analysis using Power BI

- The file was then uplaoded to Power BI for further analysis, upon uploading the data was transformed making sure all the data types where correct, renaming the first column to 'ID' and pliting the 'Location' column intwo two new ones 'City' and 'Country'

**The data is then used to create a dashboard which includes:**
- Matrix table with minimum, maximum and average values and also a car count value for each make and model
- Stacked bar chart for car count by fuel type and gear box where the different gearboxes 'Automatinė' (Automatic) and 'Mechaninė' (Manual) are in different colours
- Line chart for average mileage by year in which it was made
- Clustered column chart for average price by city it's sold in
- Line chart for average price by year in which it was made
- Line chart for car listing count by year in which it was made
<br>
![Autogidas Dashboard](https://github.com/LaurynasBil/Autogidas-Project/blob/main/files/dashboard.png)

[Autogidas Dashboard](https://app.powerbi.com/view?r=eyJrIjoiMDBjNWI0ZjQtMDkxNy00YzQyLWE5NzktMzZhM2M4OTVlYWM2IiwidCI6IjIzOWEwODc4LTk5NDQtNDFlYi1iZWRjLTczNWY4MzdkNTI3YiIsImMiOjl9)



