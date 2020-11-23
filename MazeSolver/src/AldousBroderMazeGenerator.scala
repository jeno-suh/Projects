// AldousBroderMazeGenerator.scala

import scala.util.Random

/** Generate random mazes using the Aldous-Broder algorithm */
class AldousBroderMazeGenerator extends MazeGenerator {

    def generate(maze: Maze) {
        maze.fill()
        val visited = Array.ofDim[Boolean](maze.width,maze.height)
        var currentCell = (0,0)
        visited(0)(0) = true
        var visitedCells = 1
        while (visitedCells < maze.width*maze.height) {
            val nbs = maze.neighbours(currentCell)
            val nb = nbs.apply(Random.nextInt(nbs.size))
            if (!visited(nb._1)(nb._2)){
                maze.removeWallBetween(currentCell, nb)
                visited(nb._1)(nb._2) = true
                visitedCells += 1
            }
            currentCell = nb
        } 
    }
}