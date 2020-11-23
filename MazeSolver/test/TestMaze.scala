/**  With Scala 2.12:
fsc -cp ./scalatest.jar;./scalactic.jar Maze.scala TestMaze.scala
scala -cp ./scalatest.jar;./scalactic.jar org.scalatest.run TestMaze
*/

import org.scalatest.FunSuite

class TestMaze extends FunSuite {
    val maze = new Maze(4,3)
    test("border walls in place at object creation") {
        assert(maze.isWall(0,2,Maze.Direction.North) && maze.isWall(1,2,Maze.Direction.North) &&
               maze.isWall(2,2,Maze.Direction.North) && maze.isWall(3,2,Maze.Direction.North) &&
               maze.isWall(3,0,Maze.Direction.East) && maze.isWall(3,1,Maze.Direction.East) &&
               maze.isWall(3,2,Maze.Direction.East) && maze.isWall(0,0,Maze.Direction.South) &&
               maze.isWall(1,0,Maze.Direction.South) && maze.isWall(2,0,Maze.Direction.South) &&
               maze.isWall(3,0,Maze.Direction.South) && maze.isWall(0,0,Maze.Direction.West) &&
               maze.isWall(0,1,Maze.Direction.West) && maze.isWall(0,2,Maze.Direction.West))
    }
    test("adding valid walls") {
        maze.addWall(1,1,Maze.Direction.North)
        assert(maze.isWall(1,1,Maze.Direction.North))
        //Test reflection added
        assert(maze.isWall(1,2,Maze.Direction.South))
        //Add a different wall in the same square
        maze.addWall(1,1,Maze.Direction.East)
        assert(maze.isWall(1,1,Maze.Direction.East));assert(maze.isWall(2,1,Maze.Direction.West))
        //Check first wall is still there
        assert(maze.isWall(1,1,Maze.Direction.North));assert(maze.isWall(1,2,Maze.Direction.South))
    }
    test("adding invalid walls") {
        intercept[AssertionError]{maze.addWall(4,3,Maze.Direction.South)}
        intercept[AssertionError]{maze.addWall(0,-1,Maze.Direction.North)}
        intercept[AssertionError]{maze.addWall(-1,-1,Maze.Direction.East)}
    }
    test("adding a run of walls") {
        maze.addRunWall(0,2,4,Maze.Direction.South)
        assert(maze.isWall(0,2,Maze.Direction.South) && maze.isWall(1,2,Maze.Direction.South) &&
               maze.isWall(2,2,Maze.Direction.South) && maze.isWall(3,2,Maze.Direction.South))
    }
    test("removing valid walls") {
        maze.addWall(1,1,Maze.Direction.North); maze.addWall(1,1,Maze.Direction.East)
        maze.removeWall(1,1,Maze.Direction.North)
        //Remove the reflection of wall that was added
        maze.removeWall(2,1,Maze.Direction.West)
        assert(maze.isWall(1,1,Maze.Direction.North) === false);assert(maze.isWall(1,2,Maze.Direction.South) === false)
        assert(maze.isWall(1,1,Maze.Direction.East) === false);assert(maze.isWall(2,1,Maze.Direction.West) === false)
    }
    test("removing invalid walls") {
        intercept[AssertionError]{maze.removeWall(4,3,Maze.Direction.South)}
        intercept[AssertionError]{maze.removeWall(0,-1,Maze.Direction.North)}
        intercept[AssertionError]{maze.removeWall(-1,-1,Maze.Direction.East)}
    }
    test("removing border walls") {
        intercept[AssertionError]{maze.removeWall(3,2,Maze.Direction.North)}
        intercept[AssertionError]{maze.removeWall(0,0,Maze.Direction.South)}
        intercept[AssertionError]{maze.removeWall(3,1,Maze.Direction.East)}
        intercept[AssertionError]{maze.removeWall(0,2,Maze.Direction.West)}    
    }
}