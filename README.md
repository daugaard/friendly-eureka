# Predicting NFL games using Artificial Intelligence
Building and testing machine learning models to predict the outcomes of NFL games.

## Goal
Obtains a better prediction rating that the following:

| Algorithm / Person | Rating |
|--------------------|--------|
| Flipping a coin    | 50 %|
| Picking the home team | 56.78 %|
| ESPN Expert | 56.78 %|

## Methods

Feature vectors are designed with the following information from each game:
- Team 1 Home or Away (1 for home, 0 for away)
- Team 1 Score
- Team 1 Receiving Yards
- Team 1 Rushing Yards
- Team 1 Turnovers
- Team 2 Score
- Team 2 Receiving Yards
- Team 2 Rushing Yards
- Team 2 Turnovers

# Scheme 1
Our first attempt at a feature vector will use the following game information:
- Team 1 last game
- Team 2 last game

| Algorithm / Person | 5-fold CV Score |
|--------------------|--------|
| SVM (C=0.001,gamma=0.001)   | - %|
| Neural Network (34 hidden nodes)| 56.44 %|
| Logistic Regression (C=0.01) | 58.78 %|

# Scheme 2
- Team 1 last 2 games
- Team 2 last 2 games

| Algorithm / Person | 5-fold CV Score |
|--------------------|--------|
| SVM (C=0.001,gamma=0.001)   | - %|
| Neural Network (68 hidden nodes)| 57.42 %|
| Logistic Regression (C=0.01) | 59.57 %|

# Scheme 3
- Team 1 last 3 games
- Team 2 last 3 games

| Algorithm / Person | 5-fold CV Score |
|--------------------|--------|
| SVM (C=0.001,gamma=0.001)   | - %|
| Neural Network (34 hidden nodes)| 59.51 %|
| Logistic Regression (C=30) |60.74 %|

# Scheme 4
- Team 1 last game
- Team 1 rolling average of last 3 games (does not include the home/away parameter)
- Team 2 last game
- Team 2 rolling average of last 3 games (does not include the home/away parameter)

| Algorithm / Person | 5-fold CV Score |
|--------------------|--------|
| SVM (C=0.001,gamma=0.001)   | - %|
| Neural Network (16 hidden nodes)| 61.22 %|
| Logistic Regression (C=1) |62.64 %|

# Scheme 5
- Team 1 last game
- Team 1 rolling average of last 4 games (does not include the home/away parameter)
- Team 2 last game
- Team 2 rolling average of last 4 games (does not include the home/away parameter)

| Algorithm / Person | 5-fold CV Score | Season 2015 | Season 2016 |
|--------------------|-----------------|-------------|-------------|
| SVM (C=0.001,gamma=0.001)   | - %| - % | - %|
| Neural Network (68 hidden nodes)| 61.91 %| 63.26% | 64.45% |
| Logistic Regression (C=0.01) | 63.76 %| 60.16% | |