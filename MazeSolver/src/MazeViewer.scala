// MazeViewer.scala

import scala.swing._
import scala.swing.event._
import java.awt.{Color, BasicStroke, RenderingHints}
import java.awt.geom.{Point2D, Line2D, Rectangle2D}
       
class MazeViewer(private var maze: Maze, app: AutoTortoise) extends Component {
    import MazeViewer._
    
    /** Current solve */
    private var solver: MazeSolverRunnable = null

    /** Whether to show progress or only the final result */
    var showWork = false

    preferredSize = new Dimension(width, height)

    val backgroundColor = Color.white
    background = backgroundColor
    val wallColor = Color.black
    val solutionColor = Color.yellow
    val workingColor = Color.cyan
    val activeColor = Color.blue
    val fromColor = Color.green
    val toColor = Color.red

    // Turn on mouse events
    listenTo(mouse.clicks)
    
    /** Respond to mouse clicks */
    reactions += {
        case e: MouseClicked =>
            val cell = findCell(e.point)
            if (cell != (-1,-1)) 
                publish(new MazeViewer.CellClicked(cell))
    }

    /** React to updates */
    def refresh(s: MazeSolverRunnable) {
        solver = s
        repaint()
    }
    
    def refresh(s: MazeSolverRunnable, m: Maze) {
        solver = s
        maze = m
        repaint()
    }

    /** Paint all parts of the maze */
    override def paintComponent(g: Graphics2D) {
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, 
                           RenderingHints.VALUE_ANTIALIAS_ON)
        g.setColor(background)
        g.fillRect(0, 0, size.width, size.height)
        paintCells(g)
        drawWalls(g)
    }

    /** Paint all the cells in the appropriate color */
    private def paintCells(g: Graphics2D) {
        for (x <- 0 until maze.width; y <- 0 until maze.height) {
            val cell = (x, y)
            val rectangle = transform(cell)
            g.setColor(cellColor(cell))
            g.fill(rectangle)
            g.draw(rectangle)
        }
    }

    /** Determine cell color according to status */
    private def cellColor(cell: (Int, Int)): Color = {
        if (cell == app.fromCell) 
            fromColor
        else if (cell == app.toCell) 
            toColor
        else if (solver == null) 
            backgroundColor
        else {
            import MazeSolverRunnable.CellStatus._

            val status = solver.cellStatus(cell)
            if (status == Solution) 
                solutionColor
            else if (!showWork) 
                backgroundColor
            else {
                status match {
                    case Unvisited => backgroundColor
                    case Active => activeColor
                    case Visited => workingColor
                }
            }
        }
    }

    /** Width for drawing a wall */
    private val wallWidth = 2.0f

    /** Draw all the walls */
    private def drawWalls(g: Graphics2D) {
        val stroke0 = g.getStroke()
        g.setStroke(new BasicStroke(wallWidth))
        for (w <- maze.walls) {
            g.setColor(wallColor)
            g.draw(transform(w))
        }
        g.setStroke(stroke0)
    }

    /** Transform a cell from the maze to a rectangle in the window */
    private def transform(cell: (Int, Int)): Rectangle2D.Float = {
        val (botLeft, topLeft, topRight, botRight) = corners(cell)
        val width = (topRight.getX - topLeft.getX).toFloat
        val height = (botLeft.getY - topLeft.getY).toFloat
        new Rectangle2D.Float(topLeft.getX.toFloat, topLeft.getY.toFloat,
                              width, height)
    }

    /** Transform a wall from maze to a line in the window */
    private def transform(wall: Maze.Wall): Line2D.Float = {
        val (botLeft, topLeft, topRight, botRight) = corners((wall.x,wall.y))
        if (wall.direction == Maze.Direction.North)
            new Line2D.Float(topLeft, topRight)
        else if (wall.direction == Maze.Direction.East)
            new Line2D.Float(topRight, botRight)
        else if (wall.direction == Maze.Direction.South)
            new Line2D.Float(botRight,botLeft)
        else // So wall.direction == Maze.Direction.West
            new Line2D.Float(botLeft, topLeft)
    }

    /** Return the window coordinates of the corners of the input cell where
      * the output tuple is of the form (botLeft,topLeft,topRight,botRight) */
    private def corners(cell: (Int, Int)): (Point2D.Float, Point2D.Float,
                                            Point2D.Float, Point2D.Float) = {
        // Height and width of each cell in the maze
        val wid = width.toFloat/maze.width
        val hei = height.toFloat/maze.height
        // Note y isn't cell._2 because in the window, the top left is (0,0)
        val x = cell._1; val y = maze.height-1-cell._2
        val botLeft = new Point2D.Float(x * wid, (y+1) * hei)
        val topLeft = new Point2D.Float(x * wid, y * hei)
        val topRight = new Point2D.Float((x+1) * wid, y * hei)
        val botRight = new Point2D.Float((x+1) * wid, (y+1) * hei)
        (botLeft, topLeft, topRight, botRight)
    }

    /** Find the cell that contains a given point or return the null cell i.e.
      * (-1,-1) */
    private def findCell(p: Point2D): (Int, Int) = {
        // Height and width of each cell in the maze
        val wid = width.toFloat/maze.width
        val hei = height.toFloat/maze.height
        var cell = (-1,-1)
        val x = (p.getX/wid).toInt
        val y = maze.height-1 - (p.getY/hei).toInt
        if (maze.valid((x,y))) 
            cell = (x, y)
        cell
    }
}

object MazeViewer {
    /** Canvas size */
    val width = 500; val height = 500

    /** Event when a cell is clicked */
    case class CellClicked(cell: (Int, Int)) extends Event
}