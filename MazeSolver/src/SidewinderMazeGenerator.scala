// SidewinderMazeGenerator.scala

import scala.util.Random

/** Generate random mazes using the Sidewinder algorithm */
class SidewinderMazeGenerator extends MazeGenerator {

    def generate(maze: Maze) {
        maze.fill()
        for (y <- 0 until maze.height) {
            var startRunAt = 0; var runLength = 0 
            // Current cell = startRunAt+runLength
            while (startRunAt+runLength < maze.width && 
                   (startRunAt+runLength,y) != (maze.width-1,maze.height-1)) {
                if (startRunAt+runLength < maze.width-1 &&
                    (y == maze.height-1 || Random.nextInt(2) == 0)) {
                    // Carve East
                    runLength += 1
                    maze.removeWallBetween((startRunAt+runLength-1,y),
                                           (startRunAt+runLength,y))
                }
                else {
                    // Carve North
                    val northAt = startRunAt + Random.nextInt(runLength+1)
                    maze.removeWallBetween((northAt,y), (northAt,y+1))
                    startRunAt = startRunAt + runLength + 1
                    runLength = 0
                }
            }
        }
    }
}