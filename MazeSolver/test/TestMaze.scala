/**  With Scala 2.12:
fsc -cp ./scalatest.jar;./scalactic.jar Maze.scala TestMaze.scala
scala -cp ./scalatest.jar;./scalactic.jar org.scalatest.run TestMaze
*/

import org.scalatest.FunSuite

class TestMaze extends FunSuite {
    val maze = new Maze(4,3)
    test("border walls in place at object creation") {
        assert(maze.isWall(0,2,Maze.Direction.North) &&
               maze.isWall(1,2,Maze.Direction.North) &&
               maze.isWall(2,2,Maze.Direction.North) && 
               maze.isWall(3,2,Maze.Direction.North) &&
               maze.isWall(3,0,Maze.Direction.East) && 
               maze.isWall(3,1,Maze.Direction.East) &&
               maze.isWall(3,2,Maze.Direction.East) && 
               maze.isWall(0,0,Maze.Direction.South) &&
               maze.isWall(1,0,Maze.Direction.South) && 
               maze.isWall(2,0,Maze.Direction.South) &&
               maze.isWall(3,0,Maze.Direction.South) && 
               maze.isWall(0,0,Maze.Direction.West) &&
               maze.isWall(0,1,Maze.Direction.West) && 
               maze.isWall(0,2,Maze.Direction.West))
    }
    test("addWall: adding valid walls") {
        maze.addWall(1,1,Maze.Direction.North)
        assert(maze.isWall(1,1,Maze.Direction.North))
        // Test reflection added
        assert(maze.isWall(1,2,Maze.Direction.South))
        // Add a different wall in the same square
        maze.addWall(1,1,Maze.Direction.East)
        assert(maze.isWall(1,1,Maze.Direction.East))
        assert(maze.isWall(2,1,Maze.Direction.West))
        // Check first wall is still there
        assert(maze.isWall(1,1,Maze.Direction.North))
        assert(maze.isWall(1,2,Maze.Direction.South))
    }
    test("addWall: adding invalid walls") {
        intercept[AssertionError]{maze.addWall(4,3,Maze.Direction.South)}
        intercept[AssertionError]{maze.addWall(0,-1,Maze.Direction.North)}
        intercept[AssertionError]{maze.addWall(-1,-1,Maze.Direction.East)}
    }
    test("addRunWall: adding a run of walls") {
        maze.addRunWall(0,2,4,Maze.Direction.South)
        assert(maze.isWall(0,2,Maze.Direction.South) && 
               maze.isWall(1,2,Maze.Direction.South) &&
               maze.isWall(2,2,Maze.Direction.South) && 
               maze.isWall(3,2,Maze.Direction.South))
    }
    test("removeWall: removing valid walls") {
        maze.addWall(1,1,Maze.Direction.North)
        maze.addWall(1,1,Maze.Direction.East)
        maze.removeWall(1,1,Maze.Direction.North)
        // Remove the reflection of wall that was added
        maze.removeWall(2,1,Maze.Direction.West)
        assert(maze.isWall(1,1,Maze.Direction.North) === false)
        assert(maze.isWall(1,2,Maze.Direction.South) === false)
        assert(maze.isWall(1,1,Maze.Direction.East) === false)
        assert(maze.isWall(2,1,Maze.Direction.West) === false)
    }
    test("removeWall: removing invalid walls") {
        intercept[AssertionError]{maze.removeWall(4,3,Maze.Direction.South)}
        intercept[AssertionError]{maze.removeWall(0,-1,Maze.Direction.North)}
        intercept[AssertionError]{maze.removeWall(-1,-1,Maze.Direction.East)}
    }
    test("removeWall: removing border walls") {
        intercept[AssertionError]{maze.removeWall(3,2,Maze.Direction.North)}
        intercept[AssertionError]{maze.removeWall(0,0,Maze.Direction.South)}
        intercept[AssertionError]{maze.removeWall(3,1,Maze.Direction.East)}
        intercept[AssertionError]{maze.removeWall(0,2,Maze.Direction.West)}    
    }
    test("removeWall: removing wall between two cells") {
        maze.addWall(1,1,Maze.Direction.North)
        maze.removeWallBetween((1,1),(1,2))
        assert(maze.isWall(1,1,Maze.Direction.North) === false)
    }
    test("isBorderWall") {
        maze.clear()
        for (w <- maze.walls) {
            assert(maze.isBorderWall(w))
        }
        assert(maze.isBorderWall(1,1,Maze.Direction.North) === false)
    }
    test("fill") {
        maze.fill()
        for (x <- 0 until maze.width; y <- 0 until maze.height) {
            assert(maze.isWall(x,y,Maze.Direction.North))
            assert(maze.isWall(x,y,Maze.Direction.East))
            assert(maze.isWall(x,y,Maze.Direction.South))
            assert(maze.isWall(x,y,Maze.Direction.West))
        }
    }
    test("clear") {
        maze.clear()
        for (w <- maze.walls) {
            assert(maze.isBorderWall(w))
        }
    }
    test("neighbours") {
        // Cell in middle
        var nbs = List((1,2), (2,1), (0,1), (1,0))
        assert(maze.neighbours((1,1)).sorted === nbs.sorted)
        // Edge cell
        nbs = List((0,2), (1,1), (0,0))
        assert(maze.neighbours((0,1)).sorted === nbs.sorted)
        // Corner cell
        nbs = List((0,1), (1,0))
        assert(maze.neighbours((0,0)).sorted === nbs.sorted)
    }
    test("walls") {
        // Cell with walls
        maze.addWall(1,1,Maze.Direction.North)
        maze.addWall(1,1,Maze.Direction.East)
        var ws = List(Maze.Wall(1,1,Maze.Direction.North),
                      Maze.Wall(1,1,Maze.Direction.East))
        // We use .toSet instead of .sorted because Maze.Wall doesn't have
        // order defined
        assert(maze.walls(1,1).toSet === ws.toSet)
        // Cell without walls
        maze.clear()
        ws = List()
        assert(maze.walls(1,1) === ws)
    }
    test("cellNextToWall") {
        // Wall in middle
        assert(maze.cellNextToWall(Maze.Wall(1,1,Maze.Direction.North)) 
               === Some(1,2))
        // Edge wall
        assert(maze.cellNextToWall(Maze.Wall(0,0,Maze.Direction.South)) 
               === None)
    }
}