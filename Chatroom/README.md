# Chatroom
> A simple chatroom in the terminal

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Features](#features)

## General info
This app allows users to chat with each other via a simple chatroom in the terminal. This project was created to practice C and get a taste for socket programming.

## Technologies
Project created with C using gcc 9.3 as the compiler.

## Setup
Clone this repo to your desktop and install [gcc](https://gcc.gnu.org/install/). Then go to the root directory and run `make all`.

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