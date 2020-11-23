import scala.swing._

class TestMazeViewer(val maze: Maze) extends MainFrame {
    title = "Test MazeViewer Class"

    private val viewer = new MazeViewer(maze)
    contents = new BoxPanel(Orientation.Vertical){
        contents += viewer
        border = Swing.EmptyBorder(10,10,10,10)
    }
}

object TestMazeViewer {
    def main(args: Array[String]) {
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

        val randomMaze = new Maze(50,50)
        randomMaze.generate()

        val app = new TestMazeViewer(randomMaze)
        app.visible = true
    }
}