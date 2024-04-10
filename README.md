### Introduction

The files in this repository contain code for an inference factory class. This class receives a configuration of inference engines, and is supposed to act as the intermediary facilitating routing and connection maintenance. The code provided is a bare-bones implementation of this idea and your task is to improve it by implementing **health check, failover, and load-balancing mechanisms.** 
Current implementation involves a factory that receives a dictionary containing the LLM name as the key, and a list of inference engines that host the LLM of the specified name. 

### Failover

There are two types of failover, one condition in which an inference engine fails and there is another inference engine available for the LLM; the other condition being that there is no inference engine available for the specified LLM, but there are available engines of other LLM types.

### Health Checks

The function to evaluate the health of a specific engine is already implemented, but the exact implementation of how/when health checks are done for instances is up to you. It should optimize the means by which you keep track of active and healthy instances. One option is active health checks, where you keep track of health as requests are being to the inference engine. The other being a passive methodology where health checks are made in a specific time-interval. You can also use a mix of both depending on your implementation of failover. 

### Load-Balancing

Implement multiple load balancing strategies for spreading the requests over any number of inference engines for a given LLM. The load-balancing should not be done between different LLM types, and just between the inference engines of a single LLM type. 


### Notes

#### Getting Started

Install Python + Poetry using the following [guide](https://python-poetry.org/docs/).

```bash
poetry shell
poetry install
chmod +x mock.sh
./mock.sh
```

Then in another shell you can use the entry-point:

```bash
poetry shell
python main.py
```

You can modify ‘inference.py’ and ‘main.py’, to your heart’s content, but all other files must be left untouched. 

*Leave the mock script running while you test as it sets up the mock servers your service will be sending requests against.*

#### Load Testing
Your code will be put under strain with a load testing mechanism that evaluates different types of loads in varying degrees, so we encourage you to write your own tests to ensure not only proper code execution, but also the efficacy of your design.
