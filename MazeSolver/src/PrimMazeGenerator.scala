// PrimMazeGenerator.scala

import scala.util.Random

/** Generate random mazes using Prim's algorithm */
class PrimMazeGenerator extends MazeGenerator {

    def generate(maze: Maze) {
        maze.fill()
        val visited = Array.ofDim[Boolean](maze.width,maze.height)
        visited(0)(0) = true
        var walls = maze.walls(0,0).to[scala.collection.mutable.ListBuffer]
        while (!walls.isEmpty) {
            val wall = walls.apply(Random.nextInt(walls.size))
            visited(wall.x)(wall.y) = true
            val cell = maze.cellNextToWall(wall)
            if (cell != None) {
                val c = cell.get
                if (!visited(c._1)(c._2)) {
                    visited(c._1)(c._2) = true
                    maze.removeWall(wall)
                    walls ++= maze.walls(c._1, c._2)
                }
            }
            walls -= wall
        }
    }
}