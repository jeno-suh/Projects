// EllerMazeGenerator.scala

import scala.util.Random
import scala.collection.mutable.Set

/** Generate a random maze using Eller's algorithm */
class EllerMazeGenerator extends MazeGenerator {

    def generate(maze: Maze) {
        maze.fill()
        var cellToSet = Map[(Int,Int), Set[(Int,Int)]]()
        for (y <- 0 until maze.height-1) {
            // Assign each cell in the row to its own set (if it is not already
            // part of another set)
            for (x <- 0 until maze.width) {
                if (!cellToSet.contains((x,y))) {
                    cellToSet += ((x,y) -> Set((x,y)))
                }
            }
            // Randomly join adjacent cells and merge their sets
            for (x <- 0 until maze.width) {
                if (x < maze.width-1 && cellToSet((x,y)) != cellToSet((x+1,y))
                    && Random.nextInt(2) == 0) {
                    maze.removeWallBetween((x,y), (x+1,y))
                    val merge = cellToSet((x,y)).union(cellToSet((x+1,y)))
                    for (cell <- merge) {
                        cellToSet += (cell -> merge)
                    }
                }
            }
            // Add at least one vertical connection for each set in the row
            var cellsInRow = List[(Int,Int)]()
            for (x <- 0 until maze.width) cellsInRow = (x,y) :: cellsInRow
            val groupBySet = cellsInRow.groupBy(cellToSet)
            for ((set, cells) <- groupBySet) {
                var connectionsAdded = 0
                for (cell <- cells) {
                    if (Random.nextInt(4) == 0) {
                        val above = (cell._1, cell._2+1)
                        maze.removeWallBetween(cell, above)
                        set += above
                        cellToSet += (above -> set)
                        connectionsAdded += 1
                    }
                }
                if (connectionsAdded == 0) {
                    val random = cells.apply(Random.nextInt(cells.size))
                    val above = (random._1, random._2+1)
                    maze.removeWallBetween(random, above)
                    set += above
                    cellToSet += (above -> set)
                }
            }
        }
        // For last row connect all adjacent and disjoint cells
        val y = maze.height-1
        for (x <- 0 until maze.width) {
            if (!cellToSet.contains((x,y))) {
                cellToSet += ((x,y) -> Set((x,y)))
            }
        }
        for (x <- 0 until maze.width) {
            if (x < maze.width-1 && cellToSet((x,y)) != cellToSet((x+1,y))) {
                maze.removeWallBetween((x,y), (x+1,y))
                val merge = cellToSet((x,y)).union(cellToSet((x+1,y)))
                for (cell <- merge) {
                    cellToSet += (cell -> merge)
                }
            }
        }
    }
}