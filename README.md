# Flappy bird game

A Python implementation of the classic Flappy Bird game using `pygame-ce`. In this small project I have made two different versions with two subversions for each versions. The objective was to made a base game playable by a human and another one where an "AI" learn to play.

For the first version, I have followed the youtube video of Tech with Tim (here is the link to the video https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2). 
I have tweaked a bit its code to my taste. For the "AI" subversion, the `NEAT` (https://neat-python.readthedocs.io/en/latest/) package is used. To take their words, "NEAT is a method developed by Kenneth O. Stanley for evolving arbitrary neural networks. It is an evolutionary algorithm that creates artificial neural networks". 
I mainly followed Tim's tutorial and played a bit with the configuration file. I mainly change the different possibilty for the activations functions, population size, network topology...
For the second subversion, the "playable one", I included a game over system, input detection and best score saving / loading.

For the second version, I have redone the game differently by using features of `pygame-ce` like Sprites, Rect, Groups / Layered group etc. This version is probably too complicated for the simple game that is Flappy bird, but I found it more enjoyable to code and play.
For the "AI" suversion, I followed the tutorial of Max on Tech (here is the link to the video https://www.youtube.com/watch?v=zsGvCwaaMOI&list=PLYBM90Idq20YL_q3K-8tNrQuxl3loxhTw&index=4), where the AI is implemented with a genetic algorithm without the use of "external" libraries.
To implement this algorithm I hade to tweak a bit my game version and Max's code in order for everything to work as desired.

To use this code, there is therefore two required packages, `pygame` or `pygame-ce` (I would recommend to use `pygame-ce`) and `NEAT`. Follow the next step for installation.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/Flappy-Bird---base-game-and-AI.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Flappy-Bird---base-game-and-AI
    ```
3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the required dependencies:
    ```bash
    pip install neat-python
    pip install pygame-ce
    ```
If you use conda then use the Anaconda Prompt and follow these instructions for step 3 and 4

3. Create a virtual environment (optional but recommended):
    ```bash
    conda create --name FlappyBird_env
    conda install -n FlappyBird_env pip
    conda activate FlappyBird_env
    ```
4. Install the required dependencies:
    ```bash
    pip install neat-python
    pip install pygame-ce
    ```
    
## Usage

To play the game go to either the Tech with Tim version or mine with the following command:
```bash
cd My_version/base_game_redone/code
```
or
```bash
cd TWT_version/base_game/code
```

Once in one of these directory execute the script
```bash
python main.py
```
or 
```bash
python3 main.py
```
if you want to play my version and
```bash
python flappy_bird.py
```
or 
```bash
python3 flappy_bird.py
```
if you want to play the Tech with Tim one.

For the "AI" subversion, just go back to the main directory and then to the corresponding directory and execute the python file
```bash
cd ../..
cd My_version/Genetic_algorithm/code
python main.py
```
for my version, and
```bash
cd ../..
cd TWT_version/neat_version/code
python flappy_bird.py
```
for the Tech with Tim one.

## Futur project

Next I would like to try implementing another version where an AI learn to play the game with reinforcement learning.
