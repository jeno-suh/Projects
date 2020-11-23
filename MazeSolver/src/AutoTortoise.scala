// AutoTortoise.scala

import scala.swing._

/** The main application class */
class AutoTortoise {
    private var maze = new Maze(5, 5) // Should match first selection item in
                                      // AppFrame's mazeSize ComboBox
    private val frame = new AppFrame(this)
    
    private var solver: MazeSolverRunnable = null
    private var generator: MazeGenerator = new AldousBroderMazeGenerator
    private var from = (0, 0)                      // Default is to solve from
    private var to = (maze.width-1, maze.height-1) // botLeft to topRight
    var delay = 0

    /** Allow clicks on cells to select them as 'from' or 'to' */
    def select(cell: (Int, Int)) {
        if (from == (-1, -1)) // (-1, -1) is our null cell
            from = cell
        else if (to == (-1, -1) && cell != from) 
            to = cell
        frame.refresh(solver)
    }

    /** Change the size of the maze */
    def changeSize(width: Int, height: Int) {
        maze = new Maze(width, height)
        generate()
    }

    /** Change the generator used to create the mazes */
    def changeGenerator(name: String) {
        if (name == "Aldous-Broder") 
            generator = new AldousBroderMazeGenerator
        else if (name == "DFS") 
            generator = new DFSMazeGenerator
        else if (name ==  "Division") 
            generator = new RecursiveDivisionMazeGenerator
        else if (name == "Eller") 
            generator = new EllerMazeGenerator
        else if (name == "Kruskal") 
            generator = new KruskalMazeGenerator
        else if (name == "Prim") 
            generator = new PrimMazeGenerator
        else if (name == "Sidewinder") 
            generator = new SidewinderMazeGenerator
        else if (name == "Wilson") 
            generator = new WilsonMazeGenerator
    }

    /** Can solve if two cells selected */
    def canSolve = (from != (-1, -1) && to != (-1, -1))

    /** Can reset if any cells selected */
    def canReset = (from != (-1, -1) || to != (-1, -1))

    def fromCell = from
    def toCell = to

    /** Solve the maze */
    def solve() {
        assert(canSolve)
        solver = new MazeSolverRunnable(maze, from, to) {
            override def notifyObservers() {
                // Add delay after each display update
                super.notifyObservers()
                if (delay > 0) 
                    Thread.sleep(delay)
            }
        }
        solver.addObserver(frame)
        val thread = new Thread(solver)
        thread.start()
    }

    /** Reset the maze and the from/to selections */
    def reset() {
        from = (-1, -1); to = (-1, -1)
        solver = null
        frame.refresh(solver)
    }

    /** Generate a random maze */
    def generate() {
        generator.generate(maze)
        // Default is to solve from botLeft to topRight
        from = (0, 0); to = (maze.width-1, maze.height-1)
        solver = null
        frame.refresh(solver, maze)
    }

    /** Activate the AutoTortoise app */
    def activate() {
        generate()
        frame.location = new Point(250, 50)
        frame.pack()
        frame.visible = true
    }
}

object AutoTortoise {
    def main(args: Array[String]) {
        Swing.onEDT {
            val app = new AutoTortoise
            app.activate()
        }
    }
}