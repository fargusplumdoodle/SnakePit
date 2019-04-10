# SNAKE PIT!
Isaac Thiessen 2019 ICS 221

## What is it?!
Snakepit is a Battlesnake API testing suite

## How does it work?!
Whenever my battlesnake recieves a POST request, it forwards the request to the Snakepit API. 

This builds a database of all of my battlesnake games! 

So if there is a specific turn where my snake made a wrong decision, I can use the SnakePit web interface to call my snake until I figure out how to fix the issue. 

Because CORS exists and I cannot call the snake directly from the client, I instead have the client call the server with the turn it wants to send to the snake, and the URL of the snake. Then the server calls the snake passes the response to the client. This is where it will show up left/right/up/down on the GUI.

## REQUIREMENTS
Here I will outline how this project satisfies the requirements of the project:

| Requirement | HTTP Verb | Endpoint | Description |
| --- | --- | --- | --- |
| remove single object | DELETE | games/delete |  SnakePit can delete a single turn from the database | 
| remove multiple objects| DELETE | games/delete |SnakePit can delete a game from the database which will also delete all the turns associated with it.|
| get multiple rows| GET | games/list | Retrieves a list of every game in database|
| get single row| GET | games/ | API builds a Game object from information from Game and Turn tables in database |
| create a row| POST| games/| A snake (that is authenticated)  calls this when it recieves a turn from an actual battlesnake game. The web interface doesnt have this functionality.|
|??? | POST | games/snake | If thats not good enough, my API acts as an 'anti-cors' middleman for the client to talk to the snake|

## Security implications
I would like to record somewhere in here that I am very aware that it is a terrible idea to blindly call URL specified by the user and in a more serious enviroment I would never include such functionality. But for this its fine.

To be fair I do perform validation on the data that is sent so its less likely an attacker could do something malicious. Also its highly unlikely someone would be motivated to do anything malicious because theres really nothing at stake here, maybe they crash a battlesnake but thats it.  

## Login credentails
- username: fargusD
- password: 1234asdf

Again, security is very important to this project

## Dont have a battlesnake?
The URL for my battlesnake is: 
https://sekhnet-snek-2018.herokuapp.com/
__Make sure you leave the trailing slash!__

## What is battlesnake?
Probably none of this will make sense if you dont know what battlesnake is.

Heres a link to the battlesnake website: https://play.battlesnake.io/

Its a game where you write the AI for a snake in a grid based game and try not to die.

Snakes are APIs that conform to the battlesnake standard.

 
