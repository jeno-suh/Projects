/**  With Scala 2.12:
fsc -cp ./scalatest.jar;./scalactic.jar Maze.scala MazeSolver.scala TestMazeSolver.scala
scala -cp ./scalatest.jar;./scalactic.jar org.scalatest.run TestMazeSolver
*/

import org.scalatest.FunSuite

class TestMazeSolver extends FunSuite {
    val smallMaze = new Maze(4,3)
    smallMaze.addWall(0,0,Maze.Direction.North); smallMaze.addWall(2,2,Maze.Direction.East)
    smallMaze.addWall(2,1,Maze.Direction.East); smallMaze.addWall(1,0,Maze.Direction.East)
    smallMaze.addWall(1,2,Maze.Direction.East); smallMaze.addWall(1,1,Maze.Direction.North)

    val impossibleMaze = new Maze(3,3)
    impossibleMaze.addWall(0,1,Maze.Direction.East); impossibleMaze.addWall(1,0,Maze.Direction.North)
    impossibleMaze.addWall(1,2,Maze.Direction.East); impossibleMaze.addWall(2,1,Maze.Direction.North)

    val largeMaze = new Maze(10,10)
    largeMaze.addRunWall(1,0,2,Maze.Direction.East); largeMaze.addRunWall(5,0,3,Maze.Direction.East)
    largeMaze.addRunWall(6,0,2,Maze.Direction.East); largeMaze.addRunWall(0,1,2,Maze.Direction.East)
    largeMaze.addRunWall(1,1,1,Maze.Direction.East); largeMaze.addRunWall(3,1,2,Maze.Direction.East)
    largeMaze.addRunWall(4,1,3,Maze.Direction.East); largeMaze.addRunWall(7,1,2,Maze.Direction.East)
    largeMaze.addRunWall(8,1,3,Maze.Direction.East); largeMaze.addRunWall(2,2,3,Maze.Direction.East)
    largeMaze.addRunWall(6,4,6,Maze.Direction.East); largeMaze.addRunWall(7,4,2,Maze.Direction.East)
    largeMaze.addRunWall(4,5,4,Maze.Direction.East); largeMaze.addRunWall(5,5,3,Maze.Direction.East)
    largeMaze.addRunWall(3,6,1,Maze.Direction.East); largeMaze.addRunWall(0,7,1,Maze.Direction.East)
    largeMaze.addRunWall(7,8,1,Maze.Direction.East); largeMaze.addRunWall(8,8,1,Maze.Direction.East)
    largeMaze.addRunWall(2,0,1,Maze.Direction.North); largeMaze.addRunWall(4,0,1,Maze.Direction.North)
    largeMaze.addRunWall(2,1,1,Maze.Direction.North); largeMaze.addRunWall(1,2,2,Maze.Direction.North)
    largeMaze.addRunWall(6,2,2,Maze.Direction.North); largeMaze.addRunWall(0,3,2,Maze.Direction.North)
    largeMaze.addRunWall(4,3,3,Maze.Direction.North); largeMaze.addRunWall(8,3,1,Maze.Direction.North)
    largeMaze.addRunWall(1,4,5,Maze.Direction.North); largeMaze.addRunWall(9,4,1,Maze.Direction.North)
    largeMaze.addRunWall(0,5,4,Maze.Direction.North); largeMaze.addRunWall(8,5,2,Maze.Direction.North)
    largeMaze.addRunWall(2,6,2,Maze.Direction.North); largeMaze.addRunWall(7,6,2,Maze.Direction.North)
    largeMaze.addRunWall(1,7,4,Maze.Direction.North); largeMaze.addRunWall(8,7,1,Maze.Direction.North)
    largeMaze.addRunWall(0,8,4,Maze.Direction.North); largeMaze.addRunWall(6,8,1,Maze.Direction.North)
    largeMaze.addRunWall(9,8,1,Maze.Direction.North)

    test("solving small maze") {
        val smallMazeSolver = new MazeSolver(smallMaze)
        assert(smallMazeSolver.solve === Some(List((0,0),(1,0),(1,1),(2,1),(2,0),(3,0),(3,1),(3,2))))
    }
    test("solving impossible maze") {
        val impossibleMazeSolver = new MazeSolver(impossibleMaze)
        assert(impossibleMazeSolver.solve === None)
    }
    test("solving large maze") {
        val largeMazeSolver = new MazeSolver(largeMaze)
        assert(largeMazeSolver.solve === Some(List((0,0),(0,1),(0,2),(0,3),(1,3),(2,3),(2,4),(1,4),
                                                   (0,4),(0,5),(1,5),(2,5),(3,5),(4,5),(4,6),(4,7),
                                                   (3,7),(2,7),(1,7),(1,6),(0,6),(0,7),(0,8),(1,8),
                                                   (2,8),(3,8),(4,8),(4,9),(5,9),(5,8),(6,8),(6,7),
                                                   (6,6),(6,5),(6,4),(5,4),(4,4),(3,4),(3,3),(3,2),
                                                   (3,1),(3,0),(4,0),(5,0),(5,1),(5,2),(5,3),(6,3),
                                                   (7,3),(7,4),(7,5),(7,6),(8,6),(9,6),(9,7),(8,7),
                                                   (7,7),(7,8),(7,9),(8,9),(9,9))))
    }
}