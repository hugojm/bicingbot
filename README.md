# Bicing Bot

This project consists in creating a bicing bot on Telegram to display some live information about bicing.
## Getting Started

First of all, we will begin installing the requeriments of the project in order to make the program work properly and having no problems.

### Installing

We have to install python3 because that is the coding language used in this project, so it is essential to have it installed.

```
sudo apt-get install python3
```
Now, we have python3 installed.

Then, as have created a text file that contains all the requeriments needed to launch our program, you only need to execute that comand:
```
pip install -r requirements.txt
```


## How does it work?

Well, we have implement an `O(n logn)` algorithm that follows the following pattern:
1. First of all, we do the bounding box of all the points to create a rectangle that envolves all the nodes.
2. We divide the bounding box by the distance given in the graph so we have a grill (in fact, it is a matrix).
3. Then, we sort out the nodes by its coordinates so every node is on its corresponding box.
4. Now, we are ready to compare each box with itself and the boxes below, to the right, below to the right and below to the left. Then, we will have compared each node with the candidates to have an edge with.

### How long does take?

We have tested the program in many cases. But the problem is that if we have a very short distance, the algorithm creates a lot of boxes so it wastes a lot of time. However, in general cases, our algorithm is faster than the quadratic.




We have realized that when we compute the graph with distance <= 250 the quadratic program is faster than the linear. In order to improve the computation we have implemented the quadratic when the given distance is <= 250.
On the one hand, the quadratic algorithm lasts more or less 1 second disregarding the distance.
On the other hand, the linear depends on the given distance, making it much faster in most cases.



## Execution of the program
To execute the code we have to initialize the program by accessing to a terminal and running:
```
python3 bot.py
```
We are ready to use the bot on Telegram.

**NOTE**: If you want to execute the bot in your own bot you have to change the token.txt
file by giving the token of your Bot


## Access to the bot
Now, we are ready to interact with the bot by accessing to:
https://t.me/bicing_HJ_bot



## Usage of the program
That bot has many functions that can be easily used following these instructions:

The commands that can be used are:
* ` /help ` Displays useful information about the usage of the Bot.
* `/start` Initialize the bot and creates a graph with distance 1000 by default.
* `/graph <distance>` It will create a graph whose edges distance are, at most, the given distance.
* `/plotgraph` It will create and display a map with the nodes and the edges of the graph.
* `/nodes` It will return the number of nodes of the graph.
* `/edges` It will return the number of edges of the graph.
* `/components` It will return the number of connected components of the graph.
* `/route <origin, target>` Given the directions, it will return the shortest path. **Remark:** if no `origin` is given it will compute the shortest path between your position and the target direction.
* ` /authors` It will return the name and the emails of the authors of this bot.
* `/distribute <**bikes docks**>`: It will return the total cost of the transfer and the transportation with more cost.



## Authors

* **Hugo Jiménez Muñoz** - hugo.jimenez@est.fib.upc.edu -
* **Jaume Martínez Ara**  - jaume.martinez.ara@est.fib.upc.edu -


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
