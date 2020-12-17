# Chatroom
> A simple chatroom in the terminal

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Features](#features)
* [Inspiration](#inspiration)

## General info
This app allows users to chat with each other via a simple chatroom in the terminal. This project was created to practice C and get a taste for socket programming.

## Technologies
Project created with C using gcc 9.3 as the compiler.

## Setup
Clone this repo to your desktop and install [gcc](https://gcc.gnu.org/install/). Then go to the project directory and run `make all`.

## Usage
After setting up as above, run `./server` to set up the server and `./client` to connect once the server has been initialised.

## Features
Currently implemented features are:
* Basic chatting
* Basic user commands: help, quit, list, name, pm

To-do list:
* Automated testing 
* More user commands
* Admin system
* GUI

## Inspiration
The socket programming in this project was learnt from the [Eduonix YouTube tutorials](https://www.youtube.com/watch?v=LtXEMwSG5-8&ab_channel=EduonixLearningSolutions). The project was inspired by the following videos: [#1](https://www.youtube.com/watch?v=fNerEo6Lstw&ab_channel=IdiotDeveloper) and [#2](https://www.youtube.com/watch?v=3FvHW3uzZA0&ab_channel=%E7%8E%8B%E8%BE%B0%E6%97%AD)