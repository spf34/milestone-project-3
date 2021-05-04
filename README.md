# Online Portfolio Tool

## A tool to manage online ETF portfolios and share them amongst a community of users.

### Application Features ###
Online Portfolio Tool allows users to select and build portfolios from amongst a collection of 10 Exchange Traded Funds (ETFs). These cover major US equity and fixed income indices for the development of a diversified portfolio.

The available ETFS are:
['AGG', 'EMB', 'HYG', 'IAU', 'IEMG', 'IEFA', 'MBB', 'QQQ', 'SDY', 'SPY']

## UX ##
User stories:
- Users may want to track their investment ideas through time and can do that by uploading and editing a portfolio
- Users may want to view relative performances of a range of assets to decide how to build their portfolios
- (Future feature) Users want to build a virtual portfolio and track it's performance through time, in essence allowing the 'backtesting' of investment ideas
- (Future feature) View other users' portfolios or their performance 

### Five Planes ###
* Strategy: The site exists to provide a free and easy way for retail investors to use construct portfolios and track them 

* Scope: The requirements of the site can all be addressed through a handful of pages focused on the key features. A jinja template will be used that each page can extend. The required pages are
    - Home: welcoming the user and explaining the site's purpose
    - Register/Log In/Log Out: pages to create accounts and log in/out
    - Assets: Give an overview of the assets that can be incorporated within a portfolio
    - Position Upload: Enable users to upload single position to their portfolio
    - Bulk Upload: Enable users to upload CSV of positions to their portfolio
The final two pages could be combined but it was technically easier to have them being separate to use one separate 'POST' method on each.


* Structure: The pages will be very simple, utilising printed tables for Assets and Portfolio Overview and cards encapsulating forms where data input is required.


* Skeleton: In concrete terms, the app will make use of a range of materialze components, similar to what was seen in the miniproject. In particular, card-panels will be utilised to give the upload pages a clear structure. A file upload form will be used for bulk uploads and a combination of a datepicker input, select input and standard text input will be used for the date, ticker, weight components of the individual position upload.

* Surface: Visually, the page will make use of simple greys and blues. The aim is to allow the user to focus on the portfolio/statistics tables.

## Features ##

- The app downloads financial time series data from Yahoo Finance on any day that it is used and saves the most up to date dataset in a file called 'asset_prices.csv' for easy access. 
- This time series data is used to compute statistics for each of the financial assets in which users can invest. These statistics are displayed on the 'Assets' page.
- Users can register accounts, which are then saved in the 'users' collection of the underlying mongodb database.
- Users can log in and out of the app, which will keep track of session details including the user's username and email.
- Users can upload/edit their own portfolios through two methods:
    * Position Upload: Allows uploading a single position on a given date using interactive forms
    * Bulk Upload: More flexible approach allowing dataframe of positions through time to be uploaded. Note that adding, editing and deleting records can all be accomplished through usage of this feature. There is no need for a standalone edit/delete method.

## Technologies, Frameworks & Tools Used ##
- Python/Python3
- Flask
- MongoDB
- HTML/HTML5
- CSS/CSS3
- JavaScript
- Gitpod: online IDE
- Github: version control framework hosting code repository


## Testing ##
- [HTML code validator](https://validator.w3.org/) - Analysing rendered source code due to use of jinja.
    * base.html: 1 error, 1 warning removed. Move 'script' tags inside body to remove error. Warning corresponds to flash section not having header. Adjust jinja code to only display this section when there are messages to display.
    * portfolio_bulk_upload.html: 2 errors. Replace multiline paragraph by div. Accept file of type ".csv" instead of "csv".
- [CSS code validator](https://jigsaw.w3.org/css-validator/) - No errors or warnings.
- [JavaScript Linter](https://jshint.com/) - 1 error in script.js of missing semi-colon.
- Python - PEP8 followed according to gutpod guidelines. 1 warning caused by "potentially unused" import of 'env'.

- Application:
    * Check site navigation using navbar
    * Check correct navbar elements display depending on whether user is logged in or out
    * Check the creation of new users works correctly:
        - Discovery of bug showing empty portfolio due to pandas operations, fixed.
    * Check new users added to database
    * Check password matching requirement upon registration
    * Check password matching requirement upon logging in
    * Check correct portfolio displays on 'Portfolio Overview' page
    * Check asset data is correctly downloaded and extended
- General
    * Check local and Heroku deployments have the same functionality
    * Check for and remove any unused HTML, CSS, JavaScript or Python code
    * Check mobile navbar functioning correctly
    * Test mobile friendliness - display tables will not fit on mobile screen e.g. on 'Assets' page
    

## Issues encountered ##

- For several days during development the flask 'redirect' method did not work - the website would get stuck before a 'too long to respond' error was shown. The Heroku deployment of the project did not have this The issue eventually solved itself and seems to have been related to gitpod according to other users in the Code Institute Slack chat. During the period in which this error persisted I tested code updates through Heroku, which was a slower process.

- Deciding the form of data to save in the database was not straightforward. I realised after starting the project that a relational database was a more natural structure for storing stock portfolio data. After deciding to restrict users to one portfolio, I attempted using username as the only key in each document and a dictionary of dictionaries, with keys being dates and values being dictionaries of portfolio weights, as values. Due to the difficulty of editing records stored in this format, I eventually switched to using documents with username, date, assets as keys.

- I encountered an error when trying to view my Heroku app because I had not updated the requirements.txt file to ensure all required packages were available for the deployed version of the project. 

- The 'Select Ticker' drop-down menu from the 'Position Upload' page was not displaying on the Heroku deployment of the app despite working locally. This was resolved by a hard reload.

- I encountered difficulties getting the 'datepicker' form working correctly. These were due to incorrect date formatting in the JavaScript initialisation.

- The 'Select Ticker' drop-down menu from the 'Position Upload' page was not displaying a drop-down menu. I am unsure what fixed this problem. It may have been fixing the above initialising issue with 'datepicker' as the select form was initialised after this.

### Unresolved ###
- Not responsive for mobile design at this stage.

- The current record overwrite logic is not ideal. Records are overwritten at the date level but it would be preferable if this were done at the (date, asset) level. That way, updating the weight of one security on a given date would not impact the rest of the portfolio on that date.


## Deployment ##

The project was developed using the Gitpod IDE and committed to github with git. The project was deployed to Heroku.

The process for deploying the project was:
1. Create a 'Procfile' for your project containing "web: python app.py", assuming that the Python file running the flask app is named "app.py". This will tell Heroku how to run the app.
2. Create a requirements.txt file so that all required depencies are stored.
3. Create a new app from the Heroku dashboard by selecting 'New/Create new app' from the top-right
4. Select the app and access the 'Deploy' page. Here you can link your app to the corresponding github repository by selecting 'GitHub' as deployment method and then clicking 'Connect'
5. Navigate to 'Settings' and select 'Reveal Config Vars'. Here we should set those variables contained within env.py that will not be added to github, i.e. IP, PORT, SECRET_KEY, MONGO_URI, MONGO_DBNAME
6. Navigate back to the deploy tab. You can decide to select a branch of the project to automatically deploy. Each new commit will trigger such a deployment.
7. Manually deploy by selecting 'Deploy Branch'


The project was deployed from its [GitHub repository](https://github.com/spf34/milestone-project-3)

## Credits ##

### Code ###
The project borrows heavily from the mini project section of the 'Backend Development' module. In particular, the overall design is quite similar and the logic behind logging in/out and registering is almost the same. 

The basis of two features was taken from the below links:
- Display pandas dataframe in html: 
https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table

- Upload csv via HTML and access as pandas dataframe: 
https://stackoverflow.com/questions/51356402/how-to-upload-excel-or-csv-file-to-flask-as-a-pandas-data-frame




