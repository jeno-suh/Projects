// MazeSolverRunnable.scala

/** A runnable variant of the MazeSolver class with some modifications */
class MazeSolverRunnable(maze: Maze, from: (Int, Int), to: (Int, Int)) 
    extends Runnable with Observable[MazeSolverRunnable] {

    import MazeSolverRunnable._
    
    /** Array containing dynamic data for each cell */
    private val cellData = Array.ofDim[CellData](maze.width, maze.height)

    initCellData()

    /** Starting and finishing points for the solve */
    val source = cellData(from._1)(from._2)
    val dest = cellData(to._1)(to._2)

    /** Whether the solve is complete */
    private var done = false
    
    /** Whether a solution was found */
    private var found = false

    def isDone = done
    def foundSolution = found

    /** Solve the maze using DFS */
    def run() {
        source.status = CellStatus.Visited
        val q = new scala.collection.mutable.Queue[CellData]
        q.enqueue(source)
        notifyObservers()
        
        while (!q.isEmpty && dest.status != CellStatus.Visited) {
            val active = q.dequeue
            active.status = CellStatus.Active
            notifyObservers()
            for ((x,y) <- reachable(active.cell)) {
                val neighbour = cellData(x)(y)
                if (neighbour.status == CellStatus.Unvisited) {
                    neighbour.status = CellStatus.Visited
                    neighbour.prev = active
                    q.enqueue(neighbour)
                }
            }
            active.status = CellStatus.Visited
            notifyObservers()
        }

        if (dest.status != CellStatus.Visited) { // Destination is unreachable
            found = false
            done = true
        }
        else { // Destination is reachable
            found = true
            done = true
            highlightSolution
        }
        notifyObservers()
    }

    /** Return the status of the cell */
    def cellStatus(cell: (Int, Int)): CellStatus.Value = {
        val x = cell._1; val y = cell._2
        val data = cellData(x)(y)
        data.status
    }

    /** Initialise the cellData array by filling each element with an
      * appropriate CellData object */
    private def initCellData() {
        for (x <- 0 until maze.width; y <- 0 until maze.height) {
            cellData(x)(y) = new CellData((x,y))
        }
    }

    /** Return a list of all cells reachable from input cell */
    private def reachable(cell: (Int, Int)): List[(Int, Int)] = {
        val x = cell._1; val y = cell._2
        var _reachable = List[(Int, Int)]()
        val directions = List(Maze.Direction.North, Maze.Direction.East,
                              Maze.Direction.South, Maze.Direction.West)
        for (d <- directions) {
            if (!maze.isWall(x, y, d) && maze.valid(move(cell, d))) 
                _reachable = move(cell, d) :: _reachable
        }
        _reachable
    }

    /** Return the cell after moving from input cell in the input direction */
    private def move(cell: (Int, Int), d: Maze.Direction.Value): (Int, Int) = {
        val x = cell._1; val y = cell._2
        if (d == Maze.Direction.North) 
            (x, y+1)
        else if (d == Maze.Direction.East) 
            (x+1, y)
        else if (d == Maze.Direction.South) 
            (x, y-1)
        else // So d == Maze.Direction.West
            (x-1, y)
    }

    /** Mark the appropriate cells as part of the solution */
    private def highlightSolution() {
        assert(foundSolution)
        var cell = dest
        while (cell != source) {
            cell.status = CellStatus.Solution
            cell = cell.prev
        }
        cell.status = CellStatus.Solution // cell == source now
    }
}

object MazeSolverRunnable {
    val infinity = Int.MaxValue

    /** Status for a cell */
    object CellStatus extends Enumeration {
        val Unvisited, Active, Visited, Solution = Value
    }

    class CellData(val cell: (Int, Int)) {
        var status = CellStatus.Unvisited
        var prev: CellData = null
    }
}