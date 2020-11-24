// Maze.scala

/** A maze is a collection of cells with walls to the north, south, east
  * or west of these cells. The bottom left cell will be represented
  * by (0,0) and the top right cell by (width-1, height-1). */
class Maze(_width: Int, _height: Int) {
    import Maze._

    /** Set of all walls in the maze */
    private val _walls = collection.mutable.Set[Wall]()

    /** Add walls around the maze's border */
    private def addBorders() {
        for (x <- 0 until width) {
            addWall(x, 0, Direction.South)
            addWall(x, height-1, Direction.North)
        }
        for (y <- 0 until height) {
            addWall(0, y, Direction.West)
            addWall(width-1, y, Direction.East)
        }
    }

    // Add borders at object creation
    addBorders()

    /** Return the width of the maze */
    def width: Int = _width

    /** Return the height of the maze */
    def height: Int = _height

    /** Return an iterator over the walls of the maze */
    def walls: Iterator[Wall] = _walls.toIterator

    /** Add a wall to the maze */
    def addWall(wall: Wall) {
        assert(valid(wall))
        _walls.add(wall)
        // Add wall's reflection if it exists
        if (reflect(wall) != None)
            _walls.add(reflect(wall).get)
    }
    
    /** Add a wall to the maze */
    def addWall(x: Int, y: Int, direction: Direction.Value) {
        addWall(Wall(x, y, direction))
    }

    /** Add a run (or line) of walls to the maze */
    def addRunWall(x: Int, y: Int, length: Int, direction: Direction.Value) {
        if (direction == Direction.North || direction == Direction.South) {
            for (i <- 0 until length) {
                addWall(x + i, y, direction)
            }
        }
        else if (direction == Direction.East || direction == Direction.West) {
            for (i <- 0 until length) {
                addWall(x, y + i, direction)
            }
        }
    }

    /** Remove a non-border wall from the maze */
    def removeWall(wall: Wall) {
        assert(valid(wall) && !border(wall))
        _walls.remove(wall)
        // Remove wall's reflection if it exists
        if (reflect(wall) != None) 
            _walls.remove(reflect(wall).get)
    }

    /** Remove a non-border wall from the maze */
    def removeWall(x: Int, y: Int, direction: Direction.Value) {
        removeWall(Wall(x, y, direction))
    }

    /** Remove a wall between two adjacent cells */
    def removeWallBetween(cell1: (Int, Int), cell2: (Int, Int)) {
        assert(neighbours(cell1).contains(cell2))
        if (cell1._1 == cell2._1 + 1) 
            removeWall(cell1._1, cell1._2, Direction.West)
        else if (cell1._1 == cell2._1 - 1) 
            removeWall(cell1._1, cell1._2, Direction.East)
        else if (cell1._2 == cell2._2 + 1) 
            removeWall(cell1._1, cell1._2, Direction.South)
        else if (cell1._2 == cell2._2 - 1) 
            removeWall(cell1._1, cell1._2, Direction.North)
    }

    /** Check if a wall is in the maze */
    def isWall(wall: Wall): Boolean = {
        assert(valid(wall))
        _walls.contains(wall)       
    }

    /** Check if a wall is in the maze */
    def isWall(x: Int, y: Int, direction: Direction.Value): Boolean = {
        isWall(Wall(x, y, direction))
    }

    /** Check if a wall is a border wall */
    def isBorderWall(wall: Wall): Boolean = {
        border(wall)
    }

    /** Check if a wall is a border wall */
    def isBorderWall(x: Int, y: Int, direction: Direction.Value): Boolean = {
        isBorderWall(Wall(x, y, direction))
    }

    /** Fill the maze i.e. add every wall possible */
    def fill() {
        for (x <- 0 until width; y <- 0 until height) {
            addWall(x, y, Direction.North)
            addWall(x, y, Direction.East)
        }
        addBorders
    }

    /** Clear the maze i.e. remove every wall (besides the borders) */
    def clear() {
        _walls.clear()
        addBorders
    }

    /** Return the neighbours of a cell */
    def neighbours(cell: (Int, Int)): List[(Int, Int)] = {
        var nbs = List[(Int, Int)]()
        if (valid(cell._1+1,cell._2)) 
            nbs = (cell._1+1,cell._2) :: nbs
        if (valid(cell._1-1,cell._2)) 
            nbs = (cell._1-1,cell._2) :: nbs
        if (valid(cell._1,cell._2+1)) 
            nbs = (cell._1,cell._2+1) :: nbs
        if (valid(cell._1,cell._2-1)) 
            nbs = (cell._1,cell._2-1) :: nbs
        nbs
    }

    /** Return a list of the walls of the specified cell in the maze */
    def walls(x: Int, y: Int): List[Wall] = {
        val directions = List(Direction.North, Direction.East,
                              Direction.South, Direction.West)
        var ws = List[Wall]()
        for (d <- directions) {
            if (isWall(x, y, d)) 
                ws = Wall(x, y, d) :: ws
        }
        ws
    }

    /** Return the cell that a wall is next to that isn't the cell the wall
      * belongs to i.e. that isn't (wall.x, wall.y) */
    def cellNextToWall(wall: Wall): Option[(Int, Int)] = {
        var cell: (Int, Int) = null
        if (wall.direction == Direction.North) 
            cell = (wall.x, wall.y+1)
        else if (wall.direction == Direction.East) 
            cell = (wall.x+1, wall.y)
        else if (wall.direction == Direction.South) 
            cell = (wall.x, wall.y-1)
        else if (wall.direction == Direction.West) 
            cell = (wall.x-1, wall.y)
        if (valid(cell)) 
            Some(cell)
        else 
            None
    }

    /** Check if a wall has an appropriate coordinate and direction */
    def valid(wall: Wall): Boolean = {
        if (0 <= wall.x && wall.x < width &&
            0 <= wall.y && wall.y < height &&
            (wall.direction == Direction.North || 
            wall.direction == Direction.East ||
            wall.direction == Direction.South || 
            wall.direction == Direction.West)) 
            true
        else 
            false
    }

    /** Check if a cell is valid i.e. has an appropriate coordinate */
    def valid(cell: (Int, Int)): Boolean = {
        0 <= cell._1 && cell._1 < width && 0 <= cell._2 && cell._2 < height
    }

    /** Check if a wall is a border wall */
    private def border(wall: Wall): Boolean = {
        if (valid(wall) && 
            ((wall.x == 0 && wall.direction == Direction.West) || 
             (wall.x == width-1 && wall.direction == Direction.East) ||
             (wall.y == 0 && wall.direction == Direction.South) ||
             (wall.y == height-1 && wall.direction == Direction.North))) 
            true
        else 
            false
    }

    /** Reflect a wall i.e. give representation as seen from the other side */
    // e.g. the reflection of (1,2,Direction.North) is (1,3,Direction.South)
    // Note that some walls won't have reflections e.g. (0,0,Direction.South)
    private def reflect(wall: Wall): Option[Wall] = {
        assert(valid(wall))
        var reflection: Wall = null
        if (wall.direction == Direction.North) 
            reflection = Wall(wall.x, wall.y+1, Direction.South)
        else if (wall.direction == Direction.East) 
            reflection = Wall(wall.x+1, wall.y, Direction.West)
        else if (wall.direction == Direction.South) 
            reflection = Wall(wall.x, wall.y-1, Direction.North)
        else if (wall.direction == Direction.West) 
            reflection = Wall(wall.x-1, wall.y, Direction.East)
        if (valid(reflection)) 
            Some(reflection)
        else 
            None
    }
}

object Maze {
    // We represent a wall by a coordinate and a direction 
    // e.g. (1,2,Direction.North) signifies a wall to the north of (1,2)
    case class Wall(val x: Int, val y: Int, val direction: Direction.Value)

    object Direction extends Enumeration {
        val North, East, South, West = Value
    }
}