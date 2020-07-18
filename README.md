# Flappy Bird with NEAT AI
This project is the implementation of Flappy Bird with NeuroEvolution of Augmenting Topologies (NEAT) AI in Python

## Motivation
This project was a friendly challenge by @SuperOats
At the same time I also wanted to explore about NEAT.

## Screenshots & Videos
### Run.py
Flappy Bird clone in Pygame
<br />
![Flappy Bird clone](media/run.gif)

### Train.py
NEAT training implementation with Flappy Bird clone
<br />
![NEAT Training](media/train.gif)

### Test.py
Testing of different NEAT models
![NEAT Test](media/test.gif)

Model ranking from test
<br />
![Alt text](media/test.png?raw=true "Test results")


## Core framework/concepts used
- Python NeuroEvolution of Augmenting Topologies (NEAT)
NEAT is a very powerful Artificial Intelligence (AI) algorithm, it is capable of creating AI networks by conducting
unsupervised reinforcement training. It is also capable of providing solutions to many kinds of different problems, 
be it different types of games.
To simply explain what NEAT is doing in this project:
    1. Creating a initial population of birds, let's just say 65. This also creates a different genome & network for 
    each bird.
    1. Play every bird simultaneously in the Flappy Bird clone, awarding fitness for each tick a bird is surviving or 
    passes a pipe.
    1. Fitness is then used for representing how each network fits the use case which is the game. Higher fitness 
    score = better network.
    1. Take the top x number of birds, let's just say 3 birds with the best fitness and "breed" them to form another 
    65 population with some random deviation between them, this will then be the next generation.
    1. Repeat steps until reaching the max number of generation and save the best performing bird by pickling.
    1. After that we can use the model freely without the need to wait for it to be trained.

To read more about NEAT, follow the link:
[NEAT documentation](https://neat-python.readthedocs.io/en/latest/neat_overview.html "NEAT documentation")

- Pygame
Using pygame to build the graphical user interface (GUI) for the Flappy Bird clone.

## Getting started
Follow the steps in order below

### Prerequisites
You will need to have these installed before doing anything else

- Python- 3.8.1 and above https://www.python.org/downloads/

### Installation
- Installing Python packages
```
# cd into the root folder of the project
# Change the path accordingly to your system
cd /home/flappy-bird-ai

# You should have pip installed as it comes with installing Python
# Installing python packages
pip install -r requirements.txt
```

## Usage
- Run Flappy Bird clone (Playable)
```
# Make sure your in the root directory of the project
python run.py
```

- Run Flappy Bird NEAT training (Non-playable)
```
# Make sure your in the root directory of the project
python train.py

# When the training is done by either reaching the max generation or the score threshold, the script will output the
best model in the model directory
```

- Run Flappy Bird NEAT testing (Non-playable)
```
# Make sure your in the root directory of the project
# The test script will load all models in the model directory
python test.py

# When the testing is done, the results will be displayed
```

## References
Configuration file description — NEAT-Python 0.92 documentation. (2017). Retrieved 18 July 2020, from https://neat-python.readthedocs.io/en/latest/config_file.html

Miikkulainen, K. (2002). Evolving Neural Networks Through Augmenting Topologies. Retrieved 18 July 2020, from http://nn.cs.utexas.edu/keyword?stanley:ec02

techwithtim/NEAT-Flappy-Bird. (2019). Retrieved 18 July 2020, from https://github.com/techwithtim/NEAT-Flappy-Bird/blob/master/config-feedforward.txt
