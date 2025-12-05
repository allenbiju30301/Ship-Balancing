# Ship-Balancing Application

This application provides an automated solution for optimizing **ship load balancing** operations at a shipping port, ensuring compliance with legal safety requirements while **minimizing container move time** using the A* search algorithm.

---

## Summary

Our client, Mr. Keogh, requires a reliable method to ensure every ship departing his port is **legally balanced**. A ship is balanced if the **total weight difference** between the **port** and **starboard** sides is **less than or equal to 10%** of the ship's total weight.

Incoming ships provide a manifest listing up to 16 containers arranged on an $8 \times 12$ grid. The traditional process of manually interpreting this manifest, calculating weight distribution, determining necessary container movements, and updating the manifest is **time-consuming**.

This program automatically analyzes the incoming manifest, which includes each container's **position, description, and weight (in kilograms)**. It then calculates and outputs the **optimal sequence of container movements** required to achieve a legal balance in the **least possible time**, guiding the operator through the rearrangement process. 

---

## Program Description

Follow these steps to run the application:

### 1. File Setup
* **Place the Manifest:** Copy your incoming ship manifest file into the project subfolder named:
    ```
    P3_test_cases/
    ```

### 2. Execution
* **Open Terminal:** Open a terminal.
* **Navigate to Source Directory:** Change the current directory to the source folder:
    ```bash
    cd src/
    ```
* **Run the Program:** Execute the main script using Python:
    ```bash
    python main.py
    ```

### 3. Operator Interface
* **Enter Manifest Name:** When prompted, enter the exact filename of the desired manifest.
* **Follow Prompts:** The program will output the proposed moves sequentially. **Follow the on-screen prompts** to step through each required container movement in the suggested optimal order.

---

## Output

Upon successful completion, the program generates the following files:

| File Name | Location | Description |
| :--- | :--- | :--- |
| **Outbound Manifest** | `solutions/` | The final manifest reflecting the legally balanced, optimized container arrangement. |
| **Program Log** | `Log/` | A timestamped file detailing the program execution, including weight calculations and the sequence of moves determined. |