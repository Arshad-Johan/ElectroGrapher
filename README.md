# ElectroGrapher
## Overview  
This project is an interactive GUI application built with Python and Tkinter, designed to model and optimize the runtime scheduling of VLSI transistors. Using a graph coloring algorithm, it assigns non-overlapping time slots to transistors represented as nodes on a canvas. The application provides an intuitive drag-and-drop interface for placing transistors and offers a visual representation of their runtime slots through color-coded scheduling.

## Features  
- **Interactive Node Placement**: Drag-and-drop functionality to place transistor nodes on the canvas.
- **Dynamic Edge Creation**: Edges are automatically created based on proximity thresholds to depict connectivity between transistors.
- **Graph Coloring Algorithm**: Assigns distinct colors (time slots) to adjacent transistors, ensuring no interference in runtime.
- **Customizable Time Slots**: Input start time and duration for time slots to calculate and display schedules for each transistor.
- **Table View**: Displays a detailed runtime table with transistor IDs, assigned colors, and calculated runtimes.
- **Toggle Edges**: Option to show or hide edges between transistors for better visualization.
- **Canvas Management**: Clear the canvas and start fresh with a single button.
- **Problem Statement Viewer**: Built-in description of the problem statement for user understanding.

## Technologies Used  
- **Python**: Core programming language.
- **Tkinter**: GUI framework for building the application interface.
- **Pillow (PIL)**: For handling and resizing transistor node images.
- **Math**: Used for calculating distances between nodes for edge creation.
- **Datetime**: For runtime slot calculations and scheduling.

 **Run the Application**  
   Start the application by running the Python script:
   ```bash
   python runtime_assignment.py
   ```
## How to Use  

### 1. Place Nodes  
- **Drag and drop** transistor nodes from the draggable image to the canvas.  
- Nodes will be automatically assigned **unique IDs** and placed on the canvas.  

### 2. Define Runtime Parameters  
- Enter the **Start Time** (e.g., `10:00`) and **Duration** (in minutes) for time slots in the input fields provided.  

### 3. Apply Graph Coloring  
- Click the **"Apply"** button to execute the **graph coloring algorithm**.  
- The algorithm assigns distinct **colors** to nodes based on their connectivity, ensuring that adjacent nodes do not share the same color.  

### 4. View Results  
- The **runtime table** will display:  
  - Assigned **colors** for each node.  
  - Corresponding **numbers** associated with the colors.  
  - Calculated **runtimes** for each transistor.  

### 5. Additional Options  
- **Toggle Edges**: Show or hide edges between transistors by clicking the **"Toggle Edges"** button.  
- **Clear Canvas**: Remove all nodes and edges by clicking the **"Clear Canvas"** button.  
- **View Problem Statement**: Open a popup window explaining the VLSI transistor scheduling problem.  
