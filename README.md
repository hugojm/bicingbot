# Bicing Bot

This project consist in creating a bicing bot on Telegram to display some live information about bicing.
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

First of all, we have to install python3 because is the coding language used in this project so it is essencial to have it installed.

```
sudo apt-get install python3
```
So, we will have installed python3
### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

Give an example


## How it works?

Well, we have implement an `O(n logn)` algorithm that follows the following pattern:
1. First of all, we do the bounding box of all the points to create a rectangle that envolves all the nodes.
2. We divide the bounding box by the distance given in the graph so we have a grill (in fact, it is a matrix)
3. Then, we sort out the nodes by its coordinates so every node its on his corresponding box.
4. Now, we have are ready to compare each box with itself and the box below, to the right, below to the right and below to the left. So, we have compare each node with the candidates to have an edge.

### How long it takes?

We have test it the program in many cases. But the problem is that if we have a very low distance, the algorithm creates a lot of boxes so it waste a lot of time. In general cases our algorithm is faster than the quadratic. Here is the comparation:
![distance = 1000 O(n logn)](/images/2019/05/Captura de pantalla 2019-05-30 a las 22.12.15.png)

![distance = 1000 (quadratic)](/images/2019/05/Captura de pantalla 2019-05-30 a las 22.12.44.png)


## Usage of the program
That bot has many function that can be easily used following that instruccions:

The commands that can be used are:
* ``` /help ``` Displays useful information about the usage of the Bot
* ```/start``` Initialize the bot and creates a graph with distance 1000 by default
* ```/graph <distance>``` It will create a graph whose edges distance are, at most, the given distance
* ```/plotgraph``` It will create and display a map with the nodes and the edges of the graph
* ```/nodes``` It will return the number of nodes of the graph
* ```/edges``` It will return the number of edges of the graph
* ```/components``` It will return the number of connected components of the graph
* ```/route <origin, target>``` Given the directions, it will return the shortest path.
* ``` /authors``` It will return the name and the emails of the authors of this bot.'


## Deployment

Add additional notes about how to deploy this on a live system

## Built With



## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Hugo Jiménez** - *Initial work* -
* **Jaume Martínez** - *Initial work* -

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
