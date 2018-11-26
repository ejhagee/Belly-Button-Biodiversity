# Belly-Button-Biodiversity
Web Dashboard Displaying Data About Belly Button Microbes Using Javascript and Python Flask

# Description
This project uses data originally collected by the [Belly Button Biodiversity Dataset](http://robdunnlab.com/projects/belly-button-biodiversity/) which contains information about microbes found in belly buttons.

The data stored in a sqlite SQL database.  The Python library SQLAlchemy is used to access the database which is then deployed in a server by the Python Flask library.  Flask is also used to render the web dashboard.

Javascript is used to access Flask's json outputs.  Then, Plotly.js is used to create the plots of interest.  A panel displays the sample's metadata, a pie chart of the top ten measurements is produced, a gauge chart shows the average belly button washes per week, and the entire dataset for this sample is at the bottom in a bubble chart.

# File Structure
 - The db folder contains two sqlite files, of which bellybutton.sqlite is used in this application.
 - The static folder contains the js folder, with two javascript files, app.js and bonus.js that produce the graphs.
 - The templates folder is used by Flask to render web pages.  One folder, index.html contains the home page template.
 - The Python file app.py produces the back end of the server, accessing the data, rendering the homepage for the javascript files, and also producing pages for sample data that can be accessed in the javascript scripts.
 - The file requirements.txt contains all python libraries required for the app.py file.  Running `pip install -r requirements.txt` in the command line will install the needed packages.
 - This file, README.md gives a brief description about the application.