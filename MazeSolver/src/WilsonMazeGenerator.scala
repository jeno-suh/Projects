// WilsonMazeGenerator.scala

import scala.util.Random

/** Generate a random maze using Wilson's algorithm */
class WilsonMazeGenerator extends MazeGenerator {

    def generate(maze: Maze) {
        maze.fill()
        var directions = Map[(Int,Int), Maze.Direction.Value]()
        val visited = Array.ofDim[Boolean](maze.width,maze.height)
        val unvisited = scala.collection.mutable.ListBuffer[(Int,Int)]()
        for (x <- 0 until maze.width; y <- 0 until maze.height) {
            unvisited += ((x, y))
        }
        val random = unvisited.apply(Random.nextInt(unvisited.size))
        visited(random._1)(random._2) = true; unvisited -= random
        while (!unvisited.isEmpty) {
            // Perform a random walk keeping track of directions
            val start = unvisited.apply(Random.nextInt(unvisited.size))
            var current = start
            while (!visited(current._1)(current._2)) {
                val nbs = maze.neighbours(current)
                val next = nbs.apply(Random.nextInt(nbs.size))
                if (next._2 == current._2 + 1) {
                    directions += (current -> Maze.Direction.North)
                }
                else if (next._1 == current._1 + 1) {
                    directions += (current -> Maze.Direction.East)
                }
                else if (next._2 == current._2 - 1) {
                    directions += (current -> Maze.Direction.South)
                }
                else directions += (current -> Maze.Direction.West)
                current = next
            }
            // Follow the directions set during our walk to get from start to
            // end, removing any walls in the way
            val end = current; current = start
            while (current != end) {
                visited(current._1)(current._2) = true
                unvisited -= current
                val direction = directions(current); var next = (-1, -1)
                if (direction == Maze.Direction.North) {
                    next = (current._1, current._2+1)
                }
                else if (direction == Maze.Direction.East) {
                    next = (current._1+1, current._2)
                }
                else if (direction == Maze.Direction.South) {
                    next = (current._1, current._2-1)
                }
                else next = (current._1-1, current._2)
                maze.removeWallBetween(current, next)
                current = next
            }
            // Reached the end
            visited(current._1)(current._2) = true
            unvisited -= current
            directions = Map()
        }
    }
}