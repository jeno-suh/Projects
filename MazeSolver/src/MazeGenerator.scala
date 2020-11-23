// MazeGenerator.scala

/** A simple interface for classes that generate random mazes **/
trait MazeGenerator {
    
    /** Take the input maze and randomize it */
    def generate(maze: Maze)
}