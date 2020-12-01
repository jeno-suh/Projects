// RecursiveDivisionMazeGenerator.scala

import scala.util.Random

/** Generate random mazes using the Recursive Division algorithm */
class RecursiveDivisionMazeGenerator extends MazeGenerator {

    def generate(maze: Maze) {
        maze.clear()
        divide(maze, (0,0), maze.width, maze.height)
    }

    private def divide(maze: Maze, cell: (Int, Int), width: Int, height: Int) {
        if (width < 2 || height < 2) return
        // Divide the maze vertically if the area we are considering is wider
        // than taller and vice versa
        val x = cell._1; val y = cell._2
        var direction = ""
        if (width > height) direction = "vertical"
        else if (height > width) direction = "horizontal"
        else {
            val directions = List("vertical", "horizontal")
            direction = directions.apply(Random.nextInt(2))
        }
        if (direction == "vertical" && width < 2) return
        if (direction == "horizontal" && height < 2) return
        if (direction == "vertical") {
            val r1 = Random.nextInt(width-1) + 1
            val divideAt = x + r1
            maze.addRunWall(divideAt, y, height, Maze.Direction.West)
            val r2 = Random.nextInt(height)
            val removeAt = y + r2
            maze.removeWall(divideAt, removeAt, Maze.Direction.West)
            divide(maze, (divideAt,y), width-r1, height)
            divide(maze, (x,y), r1, height)
        }
        else {
            val r1 = Random.nextInt(height-1) + 1
            val divideAt = y + r1
            maze.addRunWall(x, divideAt, width, Maze.Direction.South)
            val r2 = Random.nextInt(width)
            val removeAt = x + r2
            maze.removeWall(removeAt, divideAt, Maze.Direction.South)
            divide(maze, (x,divideAt), width, height-r1)
            divide(maze, (x,y), width, r1)
        }
    }
}