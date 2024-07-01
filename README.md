# Attention-Management-System
This repository hosts a Python-based attention management system designed to simulate human attention fluctuations during tasks and meditation periods. It includes features for template selection, custom template creation, attention simulation, and visualization of attention trends over time. Users can clone the repository, run simulations, and contribute to its enhancement under the MIT License.

The project implements an attention management system that simulates the fluctuation of human attention based on specific tasks and meditation periods.

## Features

- **Template Selection**: Users can choose a custom model for the Attention-Management-System Simulator.
- **Attention Simulation**: The program simulates how attention varies over time based on tasks and meditation.
- **Simulation Graphs**: Generates graphs showing the attention trend over time.


→ This program is designed to help you understand and visualize how various tasks and meditation sessions impact your attention levels over time. It begins by asking you to input details about the tasks you need to perform. For each task, you'll specify the name, duration, difficulty, base attention level, criticality, and start time. The program ensures that all inputs are valid, prompting you to re-enter any incorrect values. ✅

→ Next, you’ll input details about your meditation sessions, including their start times, durations, and effectiveness. Again, the program validates these inputs to ensure accuracy. ☯️

→ Once all the data is entered, you have the opportunity to review and modify any values. The program presents a summary of your inputs and allows you to make changes before proceeding. This ensures that you can refine your schedule to match your real-life scenarios accurately. ✏️🔍

→ With all the data set, the program simulates your attention levels throughout the day, considering the impact of both tasks and meditation sessions. It plots these levels on a graph 📊, showing how your attention fluctuates over time. The areas representing tasks and meditation sessions are highlighted, and key points of attention changes are marked. 🌟

→ Additionally, the program generates a correction curve that compares your attention levels with and without meditation. This visual comparison helps you see the tangible benefits of incorporating meditation into your routine. 📈✨

→ After the simulation, a detailed explanation of the attention curve is provided. This includes insights into how each task and meditation session affected your attention, accumulated fatigue, and external factors. 💡🔍

→ Finally, you can choose to run the program again, modify the values, or exit. This flexibility allows you to experiment with different schedules and see how various adjustments can improve your attention management. 🔄⚙️🚪


### ➡️ New Features:

1. **Gurdjieff's Laws Integration**
   - **Law of Octaves 🎶**
     - Every 7th unit of time, attention gets a boost! 🚀
     - Example: `attention_level += 10` on these intervals.
   
   - **Law of Three 🔺**
     - Every 3rd unit of time, attention gets a minor reduction. 📉
     - Example: `attention_level -= 5` on these intervals.

2. **Enneagram Type Effects 🌀**
   - Choose your Enneagram type and see personalized effects! 🌟
   - Example: Reformers get a slight attention boost. (`attention_level += 5`)

3. **Breathing Practices 🌬️**
   - Integrate breathing exercises for attention recovery. 🌿
   - Example: Box breathing, diaphragmatic breathing.
   - Scheduled at strategic times to optimize attention.

### 📈 Visual Enhancements:

- **Gurdjieff's Laws on Graphs 📊**
  - **Blue Dashed Lines** for Law of Octaves Intervals. 🔵
  - **Red Dashed Lines** for Law of Three Intervals. 🔴

- **Attention Level Over Time Chart 📉**
  - Highlights when meditation 🧘‍♂️ and breathing 🌬️ practices are applied.
  - Shows boosts and reductions in attention according to Gurdjieff's laws.

### 🛠️ Code Snippets:

#### Simulation Adjustments:

```python
# Apply Law of Octaves and Law of Three
if (current_time % 7 == 0):  # Law of Octaves
    attention_level += 10  # Example boost for octave
if (current_time % 3 == 0):  # Law of Three
    attention_level -= 5  # Example reduction for interval
```

#### Visualization Enhancements:

```python
# Highlight Law of Octaves and Law of Three intervals
for time in range(int(max(attention_times))):
    if time % 7 == 0:
        plt.axvline(x=time, color='blue', linestyle='--', label='Law of Octaves' if time == 0 else "")
    if time % 3 == 0:
        plt.axvline(x=time, color='red', linestyle='--', label='Law of Three' if time == 0 else "")
```

### 💡 How to Use:

1. **Select Tasks & Meditations 📝**
2. **Choose Enneagram Type 🌀**
3. **Run Simulation & View Graph 📈**


{ Enjoy optimizing your day with this interactive and insightful tool! } 👍


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/attention-management.git
   cd attention-management
   ```

2. Ensure Python is installed. This project requires Python 3.

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:

   ```bash
   python main.py
   ```

2. Follow the on-screen instructions to select a template or create a custom template.

3. Input the required details such as task duration, attention demand, etc.

4. Provide additional details like initial attention, minimum attention threshold, etc.

5. View the generated graphs and attention trend analysis.

## Contributions

Contributions to improve this project are welcome. If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a branch for your feature (`git checkout -b feature-improvement`).
3. Commit your changes (`git commit -am 'Added feature X'`).
4. Push to your branch (`git push origin feature-improvement`).
5. Open a pull request.

##License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use the code in this repository as long as proper attribution is given.
```
