# Visualize spreading epidemic with prediction

[![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## A visual representation of the spread of an epidemic. Simulations are performed for different values of input parameters.

### Description
The simulation is implemented in the Python language. The numpy library was used to manipulate the data, and visualizations are implemented using the matplotlib.pyplot and matplotlib.animation packages. The result of the simulation is a generated graphical representation of the position and state of individuals in a confined space showing their movement and interactions, as well as graphs of the number of each category of individuals over time.

Finally, the collected data is fed to a neural network to predict the number of each category of individuals.

### Installation Dependencies:

- Python 2.7 or 3
- TensorFlow 0.7
- Matplotlib
- Numpy

### How to Run?
```
git clone https://github.com/Uladzisluk/pandemia-ai.git
cd pandemia-ai
python generator.py
python ai.py
```

### Screenshots

![Screenshot from program](/Screenshots/Screenshot1.png)

### Description of the model
For the purpose of the simulation, was created the following model:

The population is divided into three categories: infected(I - infected), susceptible(S - suspectible) and recovered(R - recovered). Defined input parameters:

- n - number of initial population
- p_infected - percentage of people infected at the beginning of the simulation
- r_transmission - transmission radius
- p_transmission - probability of transmission
- t_recover - time required for recovery and transition to R - recovered state
- p_isolated - percentage of individuals in quarantine

### How to Use
The file generator.py has the ```SIMULATION PARAMETERS``` described above, which can be edited to suit your needs. However, this file generates data for different probabilities of transmission in percentage leaving the basic parameters the same. Running this file runs 5 simulations, the results of which are written to the data.csv file.

After that, you can run the file ai.py, where you can write your variable ```p_transmission_value```, which is the probability of transmission in percentage. Once run, MLP will predict the number of infected, susceptible and recovered individuals.