# TicTacToe
> A simple command-line app to play Tic-Tac-Toe in

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
* [Available AIs](#available-ais)
* [Inspiration](#inspiration)

## General info
The app includes several AIs that users can play against. Users can also test the effectiveness of these AIs by playing them against each other. This project was created to get a small taste for AI programming.

## Technologies
Project created with Python 3.8

## Setup
Clone this repo to your desktop and install [Python](https://www.python.org/downloads/).

## Usage
After you clone this repo to your desktop, go to its root directory and run either `python tictactoe.py` or `python tictactoe.py -test`. 

The former is used to play a single game of Tic-Tac-Toe; the latter is used to test the effectiveness of two AIs by having them play a specified number of games against each other and reporting on the results.

## Available AIs
* random: plays random moves
* winning: plays winning moves if they exist; otherwise plays random moves
* winning-losing: plays winning moves and blocking moves if they exist; otherwise plays random moves
* perfect: plays perfect moves using the minimax algorithm
* cache-perfect: plays perfect moves quickly using the minimax algorithm and caching
* alpha-beta: plays perfect moves quickly using the minimax algorithm with alpha-beta pruning
* quick-perfect: plays perfect moves quickly using the minimax algorithm with alpha-beta pruning and caching
* ultimate: plays perfect moves quickly but also actively sets itself up to punish mistakes

## Inspiration
Project based on Robert Heaton's [Programming Projects for Advanced Beginners #3](https://robertheaton.com/2018/10/09/programming-projects-for-advanced-beginners-3-a/).