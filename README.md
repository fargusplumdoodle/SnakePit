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

## Isaac get to the point and tell me how to test this!
Login:
- username: fargusD
- password: 1234asdf


