Issues encountered:

- redirect method not working (seemed to be an issue with gitpod, as discovered by looking at Slack). Heroku deployment does not have this issue

- Heroku app error. Must maintain up to date requirements.txt file to ensure all required packages available for the deployed version 

- Having to test updates through Heroku due to redirect method issue

- Select not showing up on Heroku despite working locally. Fixed by hard reload

- General issues with datepicker and select. Former due to date formatting, latter still a mystery.

- Deciding the form of data to save in the db. Had originally just used username as key and then dict of dicts with keys being dates and values being dicts of portfolio weights. Changed and chose username, date, assets as keys

- Overwrite logic is not ideal at the moment - done at the date level, whereas the ideal would be asset level by date. The current setup means that uploading individual assets

Sources used:

- To display pandas dataframe in html: 
https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table

- To upload csv via HTML and access as pandas dataframe:
https://stackoverflow.com/questions/51356402/how-to-upload-excel-or-csv-file-to-flask-as-a-pandas-data-frame




# Online Portfolio Tool

### A tool to manage online ETF portfolios and share them amongst a community of users.
Online Portfolio Tool allows users to select and build portfolios from amongst a collection of 10 Exchange Traded Funds (ETFs). These cover major US equity and fixed income indices for the development of a diversified portfolio.

The available ETFS are:
['AGG', 'EMB', 'HYG', 'IAU', 'IEMG', 'IEFA', 'MBB', 'QQQ', 'SDY', 'SPY']

### Gameplay ###
- The single-player game consists of the player turning over cards, two by two, until the full grid of cards has been 'matched'
- A match occurs when the two cards turned over by a player within one 'move' show the same prime minister
- A timer will begin counting down from 100 (seconds) when the game starts. The player must match all cards before time runs out
- The number of moves, or 'turns', made by a player will be recorded, with the goal being to complete the game in as few moves as possible

### Application Features ###

The current key features of the application are:
* Providing a simple, intuitive and fun online game that can be played in a short period of time
* Possibly stoking interest in who past prime ministers might have been in the case that the user does not recognise their image

## UX ##
User stories:
- Anyone looking to stimulate their memory through a game requiring minimal effort to grasp
- Possibly school children who, it is hoped, will take some interest in their political leaders - past and present - after encountering them in an enjoyable scenario

### Five Planes ###
* Strategy: The site exists to host a fun variant of a classic game to be played for leisure and mental stimulation

* Scope: The requirements of the site can all be addressed with a single page consisting of:
    - Title indicating nature of the site ('Match the Minister')
    - Game grid
    - Game information, e.g. tracking time remainaing and moves made
    - Ability to start/restart the game when appropriate 

* Structure: The below images show wireframes for the desktop and mobile versions of the site, as well as how the overlay would work in the desktop case. The mobile variant follows the same pattern

    #### Wireframes ####

    - [Desktop](https://github.com/spf34/milestone-project-2/tree/master/assets/images/wireframes/desktop.png)
    - [Desktop Overlay](https://github.com/spf34/milestone-project-2/tree/master/assets/images/wireframes/desktop_overlay.png)
    - [Mobile](https://github.com/spf34/milestone-project-2/tree/master/assets/images/wireframes/mobile.png)
  
* Skeleton: In concrete terms, the game will be based around a flexbox table consisting of equally sized card objects
It will be necessary for the cards to be two-sided, represented by 'front' and 'back' face classes, and to be able to 'rotate' to toggle the users' view between the two
The underlying logic behind how this is achieved closely follows sources 1 and 2 outlined in the Code/Credits section below

* Surface: Visually, the page will make use of a family of clean blues for the title and background, with white for the overlay text and a classical, official image for the card backs
Together these design choices aim to evoke the idea of tradition associated with the post of prime minister

## Features ##

Overlays:
- A new game will always be started from an overlay screen with a click of the mouse or a tap of the screen
- There are three overlays:
    * New game - appearing upon first arriving on the page
    * Victory - appearing after the user has 'won' by matching all cards within the alloted time
    * Gameover - appearing after the user has 'lost' by not matching all cards before the timer runs out

- [New Game Overlay](https://github.com/spf34/milestone-project-2/tree/master/assets/images/gameplay/home_screen.png)
- [Victory Overlay](https://github.com/spf34/milestone-project-2/tree/master/assets/images/gameplay/victory.png)
- [Gameover Overlay](https://github.com/spf34/milestone-project-2/tree/master/assets/images/gameplay/gameover.png)

Game Information:
- We store the number of moves made by the user and the time remainaing until gameover above the game grid
- These elements are dynamically updated in Javascript as the game progresses
    <br>

    [Game Information](https://github.com/spf34/milestone-project-2/tree/master/assets/images/gameplay/play_begins.png)


Interactive Game and Game Grid
- Each of the 16 cards is clickable and will turn over if it is not already part of a matched pair
- Consideration was taken to
    * Randomly shuffle the cards so that gameplay is not deterministic
    * Provide the illusion of cards being 3 dimensional whilst they are turning
    * Return any two cards constituting an unsuccesful move to be face down with a delay so that the user can take note of their positions
    * Prohibit moves that consist of flipping and then reflipping the same card
    * Prohibit moves that flip an already matched card
    * Prohibit more than two cards being flipped as part of any one move
    * Reset the game grid upon a new game being started following victory or defeat
- Sound effects were added to the game to improve the user experience
    * A celebratory trumpet sound plays when two cards are matched
    * Overlapping matches are handled in such a way that both sound clips will play
    * Upbeat and downbeat piano clips play upon victory and gameover, respectively

* [Matched Cards](https://github.com/spf34/milestone-project-2/tree/master/assets/images/gameplay/first_match.png)
* [Middle of Move](https://github.com/spf34/milestone-project-2/tree/master/assets/images/gameplay/mid_turn.png)

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
base.html: 1 error, 1 warning removed. Move 'script' tags inside body to remove error. Warning corresponds to flash section not having header. Adjust jinja code to only display this section when there are messages to display
- [CSS code validator](https://jigsaw.w3.org/css-validator/) - No errors or warnings
- [JavaScript Linter](https://jshint.com/) - No errors or warnings after making changes to avoid the following warnings:
    * Undefined variables caused by omission of 'var', 'let', etc.
    * Warnings on use of 'let' versus 'var' for global variables
    * Warning on iterating through array objects directly instead of using an index for access
    * Unused variable definition warning
- Gameplay:
    * Check that number of clicks is correctly recorded. In particular, this includes not counting clicks as part of illegitimate moves
    * Check that time remaining is correctly recorded and gameover is triggered upon reaching zero
    * Check that overlays respond to click events and cause a clean new game to be started, including reset of time remaining, clicks made and resetting all cards to be facedown
    * Check that the appropriate overlay is triggered by the appropriate event
    * Check that appropriate sounds are played when they should be, including when two matches follow closely after one another
    * Check that no illegitimate moves are allowed, including double-flips, flips of matched cards and flipping more than two cards per move
    * Check that card shuffle is taking effect and that the ordering of the cards is non-deterministic
- General
    * Check all images have alternate text
    * Check for and remove any unused CSS classes
    * View the game on all of the available devices in Chrome developer tools. Several issues discovered this way and fixed satisfactorily. In particular, the inability to use a double click feature to trigger events on mobile 
    * Test the transition from four columns to two columns on devices of smaller screen sizes
    * Test game using Chrome and Safari - at the last minute I noticed that there seem to be some real problems on Safari with cards not rendering properly when turning and sometimes remaining facedown after clicking

## Bugs ##
 [How can I prevent text/element selection with cursor drag](https://stackoverflow.com/questions/5429827/how-can-i-prevent-text-element-selection-with-cursor-drag)


### Unresolved ###



## Deployment ##
This section closely follows the example given here: [README example](https://github.com/AJGreaves/portrait-artist/blob/master/README.md)

The project was developed using the Gitpod IDE and committed to github with git

The project was deployed from its [GitHub repository](https://github.com/spf34/milestone-project-2) to GitHub pages using the usual steps:
1. Navigate to the repository on GitHub
2. Click 'Settings' and scroll down to the 'GitHub Pages' subsection
3. Under Source click the drop-down menu labelled None and select Master Branch
4. On selecting Master Branch the page is refreshed and the website will now be deployed
5. Here is a link to the deployed page: [GitHub Pages Deployment](https://spf34.github.io/milestone-project-2/)

## Credits ##

### Code ###
The overall sturcture of my code, and particularly the way in which HTML & CSS were used to form the game grid and allow cards to be turned, very closely follows a mixture of the following three sources:
1. [Memory Card Game - JavaScript Tutorial](https://www.youtube.com/watch?v=ZniVgo8U7ek&ab_channel=freeCodeCamp.org)
2. [How to Code a Card Matching Game](https://www.youtube.com/watch?v=28VfzEiJgy4&t=0s)
3. [Live Coding a Memory Game: HTML, CSS, Javascript](https://www.youtube.com/watch?v=bbb9dZotsOc)
