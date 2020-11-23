// KruskalMazeGenerator.scala

import scala.util.Random
import scala.collection.mutable.ListBuffer
import scala.collection.immutable.Set

/** Generate random mazes using Kruskal's algorithm */
class KruskalMazeGenerator extends MazeGenerator {
    private var sets = ListBuffer[Set[(Int, Int)]]()

    def generate(maze: Maze) {
        sets = ListBuffer[Set[(Int, Int)]]()
        for (x <- 0 until maze.width; y <- 0 until maze.height) {
            sets += Set((x,y))
        }
        maze.fill()
        var walls = maze.walls.to[ListBuffer]
        while (!walls.isEmpty) {
            val wall = walls.apply(Random.nextInt(walls.size))
            val cell1 = (wall.x, wall.y)
            val cell2 = maze.cellNextToWall(wall)
            if (cell2 != None && findSet(cell1).get != findSet(cell2.get).get) {
                maze.removeWall(wall)
                union(cell1, cell2.get)
            }
            walls -= wall
        }
    }

    /** Return the set that contains the specified cell */
    private def findSet(cell: (Int, Int)): Option[Set[(Int, Int)]] = {
        for (set <- sets) {
            if (set.contains(cell))
                return Some(set)
        }
        None
    }

    /** Join the sets that contain the specified cells */
    private def union(cell1: (Int, Int), cell2: (Int, Int)) {
        val set1 = findSet(cell1).get; val set2 = findSet(cell2).get
        if (set1 != set2) {
            sets -= set1; sets -= set2
            sets += set1 union set2
        }
    }
}