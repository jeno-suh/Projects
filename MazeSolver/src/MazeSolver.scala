// MazeSolver.scala

/** Solves mazes using the BFS algorithm */
class MazeSolver(maze: Maze) {
    import MazeSolver._
    
    /** Array storing length of shortest path from source i.e. (0,0)*/
    //We fill with infinity initially
    private val dist = 
        Array.tabulate(maze.width, maze.height)((_,_) => infinity)
    
    /** Array storing backpointers to predecessor on shortest path */
    //We fill with (-1,-1) (our 'null' maze coordinate) initially
    private val pred = 
        Array.tabulate(maze.width, maze.height)((_,_) => (-1,-1))

    def solve(): Option[List[(Int, Int)]] = {
        dist(0)(0) = 0
        val q = new scala.collection.mutable.Queue[(Int,Int)]
        q.enqueue((0,0))
        while (!q.isEmpty) {
            val (x,y) = q.dequeue
            for ((x1,y1) <- reachable(x,y)) {
                if (dist(x1)(y1) == infinity) {
                    dist(x1)(y1) = dist(x)(y) + 1
                    pred(x1)(y1) = (x,y)
                    q.enqueue((x1,y1))
                }
            }
        }
        if (dist(maze.width-1)(maze.height-1) == infinity) None
        else {
            var path = List[(Int, Int)]()
            var toAdd = (maze.width-1,maze.height-1)
            while (toAdd != (0,0)) {
                path = toAdd :: path
                toAdd = pred(toAdd._1)(toAdd._2)
            }
            path = (0,0) :: path
            return Some(path)
        }
    }

    /** Returns a list of all coordinates reachable from input coordinate */
    private def reachable(x: Int, y: Int): List[(Int, Int)] = {
        var _reachable = List[(Int, Int)]()
        val directions = List(Maze.Direction.North, Maze.Direction.East,
                              Maze.Direction.South, Maze.Direction.West)
        for (d <- directions) {
            if (!maze.isWall(new Maze.Wall(x, y, d)) && valid(move(x, y, d))) {
                _reachable = move(x, y, d) :: _reachable
            }
        }
        _reachable
    }

    /** Returns the coordinate after moving in the input direction */
    private def move(x: Int, y: Int, d: Maze.Direction.Value): (Int, Int) = {
        if (d == Maze.Direction.North) return (x,y+1)
        if (d == Maze.Direction.East) return (x+1,y)
        if (d == Maze.Direction.South) return (x,y-1)
        //Since we haven't returned yet, it must be that d is West. So,
        return (x-1,y)
    }

    /** Checks if a coordinate is valid (i.e. is part of the maze) */
    private def valid(coord: (Int, Int)): Boolean = {
        val x = coord._1; val y = coord._2
        0 <= x && x < maze.width && 0 <= y && y < maze.height
    }
}

object MazeSolver {
    val infinity = Int.MaxValue
}