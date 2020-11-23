// DFSMazeGenerator.scala

import scala.util.Random

/** Generate random mazes using the DFS algorithm */
class DFSMazeGenerator extends MazeGenerator{

    def generate(maze: Maze) {
        maze.fill()
        val stack = new scala.collection.mutable.Stack[(Int, Int)]
        val visited = Array.ofDim[Boolean](maze.width,maze.height)
        visited(0)(0) = true; stack.push((0,0))
        while (!stack.isEmpty) {
            val cell = stack.pop
            val nbs = maze.neighbours(cell)
            // Filter to get the unvisited neighbours of cell
            val uvnbs = nbs.filter(coord => !visited(coord._1)(coord._2))
            if (!uvnbs.isEmpty) {
                stack.push(cell)
                val uvnb = uvnbs.apply(Random.nextInt(uvnbs.size))
                maze.removeWallBetween(cell,uvnb)
                visited(uvnb._1)(uvnb._2) = true
                stack.push(uvnb)
            }
        }
    }
}