// AppFrame.scala

import scala.swing._
import scala.swing.event._
import java.awt.{Font, Color}

/** The main application window for AutoTortoise */
class AppFrame(app: AutoTortoise) 
    extends MainFrame with Observable.Observer[MazeSolverRunnable] {

    title = "AutoTortoise"
    font = new Font("SansSerif", Font.PLAIN, 12)

    private val viewer = new MazeViewer(null, app)

    import AppFrame.PassiveTextField
    private val fromText = new PassiveTextField(20)
    private val toText = new PassiveTextField(20)

    private val mazeSize = new ComboBox(List("5x5","10x10","25x25",
                                             "50x50","100x100"))
    private val mazeGenerator = new ComboBox(List("Aldous-Broder","DFS",
                                                  "Division","Eller","Kruskal",
                                                  "Prim","Sidewinder",
                                                  "Wilson"))
    
    private val workCheck = new CheckBox("Show working")
    private val delayCheck = new CheckBox("Delay between steps")

    private val delaySlider = new Slider {
        min = 0; max = 100; value = 50
        majorTickSpacing = 50; minorTickSpacing = 10
        paintTicks = true; paintLabels = true
        visible = false
    }

    private val solveButton = Button("Solve") { app.solve() }

    private val resetButton = Button("Reset") { app.reset() }

    private val generateButton = Button("Generate") { app.generate() }

    private val buttons = new FlowPanel(solveButton, resetButton, 
                                        generateButton)

    private val labelFont = new Font("SansSerif", Font.BOLD, 12)    
    private class MyLabel(txt: String) extends Label {
        text = txt; font = labelFont
    }

    private val controls = new GridBagPanel {
        val elements = Array[Component](
            new MyLabel("From:"), fromText,
            new MyLabel("To:"), toText,
            new MyLabel("Size:"), mazeSize,
            new MyLabel("Generator:"), mazeGenerator,
            workCheck, 
            delayCheck, delaySlider)

        var i = 0
        for (c <- elements) {
            layout(c) = new Constraints {
                gridx = 0; gridy = i
                anchor = GridBagPanel.Anchor.West
                insets = new Insets(5, 5, 5, 5)
            }
            i += 1
        }
    }
                
    private val column = new BorderPanel {
        add(controls, BorderPanel.Position.North)
    }

    // Basic layout: map with controls at right, buttons at bottom
    contents = new BorderPanel {
        add(viewer, BorderPanel.Position.Center)
        add(column, BorderPanel.Position.East)
        add(buttons, BorderPanel.Position.South)
    }

    // Respond to mazeSize
    listenTo(mazeSize.selection)

    reactions += {
        case SelectionChanged(`mazeSize`) =>
            // Assumes mazeSize.selection.item is of the form width.toString+
            // "x"+height.toString
            val width = 
                mazeSize.selection.item.takeWhile(Character.isDigit).toInt
            val height =
                mazeSize.selection.item.dropWhile(Character.isDigit).tail.toInt
            app.changeSize(width,height)
    }

    // Respond to mazeGenerator
    listenTo(mazeGenerator.selection)

    reactions += {
        case SelectionChanged(`mazeGenerator`) =>
            app.changeGenerator(mazeGenerator.selection.item)
    }

    // Respond to workCheck
    listenTo(workCheck)
    reactions += {
        case ButtonClicked(`workCheck`) =>
            viewer.showWork = workCheck.selected
    }

    // Respond to delay controls
    listenTo(delayCheck, delaySlider)
    reactions += {
        case ButtonClicked(`delayCheck`) =>
            delaySlider.visible = delayCheck.selected
            setDelay()
        case ValueChanged(`delaySlider`) =>        
            setDelay()
    }
    
    /** Adjust the delay to match what is selected by the controls */
    private def setDelay() {
        if (delayCheck.selected)
            app.delay = delaySlider.value
        else
            app.delay = 0
    }

    // React to events from viewer
    listenTo(viewer)
    reactions += { 
        case MazeViewer.CellClicked(cell) => app.select(cell)
    }

    /** Refresh the display -- called from worker thread */
    def refresh(solver: MazeSolverRunnable) {
        viewer.refresh(solver)
        Swing.onEDT { updateDisplay(solver) }
    }
    
    def refresh(solver: MazeSolverRunnable, maze: Maze) {
        viewer.refresh(solver, maze)
        Swing.onEDT { updateDisplay(solver) }
    }
    
    /** Update the display -- called from event thread */
    private def updateDisplay(solver: MazeSolverRunnable) {
        if (app.fromCell == (-1, -1)) // (-1, -1) is our null cell
            fromText.text = ""
        else 
            fromText.text = app.fromCell.toString
        if (app.toCell == (-1, -1)) 
            toText.text = ""
        else 
            toText.text = app.toCell.toString

        if (solver == null) {
            solveButton.enabled = app.canSolve
            resetButton.enabled = app.canReset
        }
        else {
            solveButton.enabled = solver.isDone
            resetButton.enabled = solver.isDone
            generateButton.enabled = solver.isDone
            mazeSize.enabled = solver.isDone
            if (solver.isDone && !solver.foundSolution)
                Dialog.showMessage(contents.head, "Maze is unsolvable")
        }
    }
}

object AppFrame {
    /** An uneditable text field with a white background */
    private class PassiveTextField(w: Int) extends TextField {
        columns = w; editable = false
        background = Color.WHITE
    }
}