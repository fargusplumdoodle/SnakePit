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
| |||
||||
||||
||||
||||
- **DELETE Single object**: __games/delete endpoint:__ SnakePit can delete a single turn from the database
- **DELETE multiple objects**: SnakePit can delete a game from the database which will also delete all the turns associated with tit.
- **GET multiple objects**:

## Isaac get to the point and tell me how to test this!
Login:
- username: fargusD
- password: 1234asdf


