/**  With Scala 2.12:
fsc -cp ./scalatest.jar;./scalactic.jar Maze.scala MazeSolver.scala MazeGenerator.scala AldousBroderMazeGenerator.scala DFSMazeGenerator.scala EllerMazeGenerator.scala KruskalMazeGenerator.scala PrimMazeGenerator.scala RecursiveDivisionMazeGenerator.scala SidewinderMazeGenerator.scala WilsonMazeGenerator.scala TestMazeGenerator.scala
scala -cp ./scalatest.jar;./scalactic.jar org.scalatest.run TestMazeGenerator
*/

import org.scalatest.FunSuite

class TestMazeGenerator extends FunSuite {
    val maze = new Maze(10,10)
    for (gen <- List(new AldousBroderMazeGenerator, new DFSMazeGenerator,
                     new EllerMazeGenerator, new KruskalMazeGenerator,
                     new PrimMazeGenerator, new RecursiveDivisionMazeGenerator,
                     new SidewinderMazeGenerator, new WilsonMazeGenerator)) {
        test(gen.toString.takeWhile(_ != '@')+": generates solvable mazes") {
            for (i <- 1 to 1000) {
                gen.generate(maze)
                val solver = new MazeSolver(maze)
                assert(solver.solve() != None)
            }
        }
    }
}