import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from io import BytesIO
from PIL import Image
import numpy as np

# Define the Task, MeditationSession, BreathingPractice, and EnneagramType classes
class Task:
    def __init__(self, task_id, name, base_attention, difficulty, criticality, duration, start_time):
        self.task_id = task_id
        self.name = name
        self.base_attention = base_attention
        self.difficulty = difficulty
        self.criticality = criticality
        self.duration = duration
        self.start_time = start_time

class MeditationSession:
    def __init__(self, start_time, duration, effectiveness):
        self.start_time = start_time
        self.duration = duration
        self.effectiveness = effectiveness

class BreathingPractice:
    def __init__(self, name, start_time, duration, effectiveness):
        self.name = name
        self.start_time = start_time
        self.duration = duration
        self.effectiveness = effectiveness

class EnneagramType:
    def __init__(self, type_id, name, transmutation_practices):
        self.type_id = type_id
        self.name = name
        self.transmutation_practices = transmutation_practices

    def apply_effects(self, attention_level):
        if self.type_id == 1:
            attention_level += 5  # Reformer gets a slight attention boost
        elif self.type_id == 2:
            attention_level += 3  # Helper gets a smaller attention boost
        return attention_level

# Define the simulate_with_voluntary function
def simulate_with_voluntary(tasks, initial_attention, min_attention, max_attention, meditation_sessions, breathing_practices, enneagram_type, apply_meditation, apply_breathing):
    history = []
    attention_curve = []
    correction_curve = []  # Correction curve initialization
    meditation_points = []
    breathing_points = []
    voluntary_intention_points = []
    total_attention_gain = 0
    total_breathing_gain = 0
    total_voluntary_intention_gain = 0
    current_time = 0
    attention_level = initial_attention

    # Apply initial Enneagram effects
    attention_level = enneagram_type.apply_effects(attention_level)

    # Ensure the attention line starts from point 0
    history.append((current_time, None, attention_level, 0))
    attention_curve.append((current_time, None, 0, attention_level))
    correction_curve.append((current_time, attention_level))

    for task in tasks:
        current_time = task.start_time
        task_end_time = task.start_time + task.duration
        while current_time < task_end_time:
            if apply_meditation:
                for session in meditation_sessions:
                    if session.start_time <= current_time < session.start_time + session.duration:
                        attention_level += session.effectiveness
                        if attention_level > max_attention:
                            attention_level = max_attention
                        meditation_points.append((current_time, attention_level))
                        total_attention_gain += session.effectiveness

            if apply_breathing:
                for practice in breathing_practices:
                    if practice.start_time <= current_time < practice.start_time + practice.duration:
                        attention_level += practice.effectiveness
                        if attention_level > max_attention:
                            attention_level = max_attention
                        breathing_points.append((current_time, attention_level))
                        total_breathing_gain += practice.effectiveness

            # Apply Law of Octaves and Law of Three
            if (current_time % 7 == 0):  # Law of Octaves
                attention_level += 10  # Example boost for octave
            if (current_time % 3 == 0):  # Law of Three
                attention_level -= 5  # Example reduction for interval

            # Adjust the rate of decrease when attention is below the minimum threshold
            if attention_level < min_attention:
                attention_level -= task.difficulty * 0.5  # Reduce the rate by half
                voluntary_intention_points.append((current_time, attention_level))
                total_voluntary_intention_gain += task.difficulty * 0.5
            else:
                attention_level -= task.difficulty

            history.append((current_time, task.task_id, attention_level, task.difficulty))
            attention_curve.append((current_time, task.task_id, task.difficulty, attention_level))
            correction_curve.append((current_time, attention_level))  # Update correction curve
            current_time += 1

    accumulated_fatigue = sum(task.difficulty for task in tasks)
    avg_external_factors = sum(task.criticality for task in tasks) / len(tasks) if tasks else 0
    return history, attention_curve, correction_curve, meditation_points, breathing_points, voluntary_intention_points, total_attention_gain, total_breathing_gain, total_voluntary_intention_gain, accumulated_fatigue, avg_external_factors



def simulate(tasks, initial_attention, min_attention, max_attention, meditation_sessions, breathing_practices, enneagram_type, apply_meditation, apply_breathing):
    history = []
    attention_curve = []
    meditation_points = []
    breathing_points = []
    total_attention_gain = 0
    total_breathing_gain = 0
    current_time = 0
    attention_level = initial_attention

    # Apply initial Enneagram effects
    attention_level = enneagram_type.apply_effects(attention_level)

    for task in tasks:
        current_time = task.start_time
        task_end_time = task.start_time + task.duration
        while current_time < task_end_time:
            if apply_meditation:
                for session in meditation_sessions:
                    if session.start_time <= current_time < session.start_time + session.duration:
                        attention_level += session.effectiveness
                        if attention_level > max_attention:
                            attention_level = max_attention
                        meditation_points.append((current_time, attention_level))
                        total_attention_gain += session.effectiveness

            if apply_breathing:
                for practice in breathing_practices:
                    if practice.start_time <= current_time < practice.start_time + practice.duration:
                        attention_level += practice.effectiveness
                        if attention_level > max_attention:
                            attention_level = max_attention
                        breathing_points.append((current_time, attention_level))
                        total_breathing_gain += practice.effectiveness

            # Apply Law of Octaves and Law of Three
            if (current_time % 7 == 0):  # Law of Octaves
                attention_level += 10  # Example boost for octave
            if (current_time % 3 == 0):  # Law of Three
                attention_level -= 5  # Example reduction for interval

            attention_level -= task.difficulty

            history.append((current_time, task.task_id, attention_level, task.difficulty))
            attention_curve.append((current_time, task.task_id, task.difficulty, attention_level))
            current_time += 1

    accumulated_fatigue = sum(task.difficulty for task in tasks)
    avg_external_factors = sum(task.criticality for task in tasks) / len(tasks) if tasks else 0
    return history, attention_curve, meditation_points, breathing_points, total_attention_gain, total_breathing_gain, accumulated_fatigue, avg_external_factors






def plot_simulation_with_voluntary(history, tasks, attention_curve, correction_curve, meditation_points, breathing_points, voluntary_intention_points, min_attention, meditation_sessions, breathing_practices):
    # First graph with attention levels
    plt.figure(figsize=(12, 6))
    attention_times = [entry[0] for entry in attention_curve]
    attention_levels = [entry[3] for entry in attention_curve]

    plt.plot(attention_times, attention_levels, label='Attention Level', color='b')

    for task in tasks:
        plt.axvspan(task.start_time, task.start_time + task.duration, alpha=0.2, color='yellow', label=f'Task: {task.name}')

    # Plotting meditation sessions with color mapping
    note_colors = {
        "C Do": "red",
        "D Re": "orange",
        "E Mi": "yellow",
        "F Fa": "green",
        "G So": "yellow",  # inverted from blue to yellow
        "A La": "indigo",
        "B Si": "violet"
    }

    note_sections = [
        ("C Do", "1/1"),
        ("D Re", "9/8"),
        ("E Mi", "5/4"),
        ("F Fa", "4/3"),
        ("G So", "3/2"),
        ("A La", "5/3"),
        ("B Si", "15/8")
    ]

    for session in meditation_sessions:
        start = session.start_time
        duration = session.duration
        step = duration / len(note_sections)
        for i, (note, ratio) in enumerate(note_sections):
            plt.axvspan(start + i * step, start + (i + 1) * step, alpha=0.2, color=note_colors[note], label=f'Meditation: {note}' if i == 0 else "")

    for practice in breathing_practices:
        plt.axvspan(practice.start_time, practice.start_time + practice.duration, alpha=0.2, color='purple', label='Breathing')

    for meditation_time, attention_level in meditation_points:
        plt.scatter(meditation_time, attention_level, color='r', s=50, label='Meditation Point' if meditation_time == meditation_points[0][0] else "")

    for breathing_time, attention_level in breathing_points:
        plt.scatter(breathing_time, attention_level, color='pink', s=50, label='Breathing Point' if breathing_time == breathing_points[0][0] else "")

    for voluntary_time, attention_level in voluntary_intention_points:
        plt.scatter(voluntary_time, attention_level, color='orange', s=50, label='Voluntary Intention' if voluntary_time == voluntary_intention_points[0][0] else "")

    for time in range(int(max(attention_times))):
        if time % 7 == 0:
            plt.axvline(x=time, color='blue', linestyle='--', label='Law of Octaves' if time == 0 else "")
        if time % 3 == 0:
            plt.axvline(x=time, color='red', linestyle='--', label='Law of Three' if time == 0 else "")

    plt.axhline(y=min_attention, color='gray', linestyle='--', label='Min Attention Threshold')
    plt.xlabel('Global Clock (minutes)')
    plt.ylabel('Attention Level')
    plt.title('Attention Level Over Time Considering Fatigue, Task Difficulty, Meditation, Breathing Practices, and Voluntary Intention')
    plt.grid(True)
    
    # Add legend for note colors
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    note_legend = [plt.Line2D([0], [0], color=color, lw=4) for color in note_colors.values()]
    note_labels = list(note_colors.keys())
    note_legend_handles = dict(zip(note_labels, note_legend))
    by_label.update(note_legend_handles)
    plt.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1, 1), title="Legend")

    plt.tight_layout()
    plt.show()

    # Second graph with correction curve and attention levels
def plot_correction_curve(tasks, initial_attention, min_attention, max_attention, meditation_sessions, breathing_practices, enneagram_type):
    _, attention_curve_no_meditation, _, _, _, _, _, _ = simulate(tasks, initial_attention, min_attention, max_attention, meditation_sessions, breathing_practices, enneagram_type, apply_meditation=False, apply_breathing=False)
    _, attention_curve_with_meditation_breathing, _, _, _, _, _, _ = simulate(tasks, initial_attention, min_attention, max_attention, meditation_sessions, breathing_practices, enneagram_type, apply_meditation=True, apply_breathing=True)

    plt.figure(figsize=(12, 6))

    times_no_meditation = [entry[0] for entry in attention_curve_no_meditation]
    levels_no_meditation = [entry[3] for entry in attention_curve_no_meditation]
    plt.plot(times_no_meditation, levels_no_meditation, label='Attention without Meditation/Breathing', color='b')

    times_with_meditation_breathing = [entry[0] for entry in attention_curve_with_meditation_breathing]
    levels_with_meditation_breathing = [entry[3] for entry in attention_curve_with_meditation_breathing]
    plt.plot(times_with_meditation_breathing, levels_with_meditation_breathing, label='Attention with Meditation/Breathing', color='g')

    plt.axhline(y=min_attention, color='gray', linestyle='--', label='Min Attention Threshold')
    plt.xlabel('Global Clock (minutes)')
    plt.ylabel('Attention Level')
    plt.title('Attention Level Over Time Considering Fatigue, Task Difficulty, Meditation, Breathing Practices, and Voluntary Intention')    
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Legend")
    plt.tight_layout()
    plt.show()





# Define the run_simulation_with_voluntary function
def run_simulation_with_voluntary():
    try:
        initial_attention = float(initial_attention_entry.get())
        min_attention = float(min_attention_entry.get())
        max_attention = float(max_attention_entry.get())

        tasks = []
        for i in range(num_tasks.get()):
            name = task_entries[i][0].get()
            duration = float(task_entries[i][1].get())
            difficulty = float(task_entries[i][2].get())
            base_attention = float(task_entries[i][3].get())
            criticality = float(task_entries[i][4].get())
            start_time = float(task_entries[i][5].get())
            tasks.append(Task(i, name, base_attention, difficulty, criticality, duration, start_time))

        meditation_sessions = []
        for i in range(num_meditations.get()):
            start_time = float(meditation_entries[i][0].get())
            duration = float(meditation_entries[i][1].get())
            effectiveness = float(meditation_entries[i][2].get())
            meditation_sessions.append(MeditationSession(start_time, duration, effectiveness))

        breathing_practices = []
        for i in range(num_breathings.get()):
            name = breathing_entries[i][0].get()
            start_time = float(breathing_entries[i][1].get())
            duration = float(breathing_entries[i][2].get())
            effectiveness = float(breathing_entries[i][3].get())
            breathing_practices.append(BreathingPractice(name, start_time, duration, effectiveness))

        enneagram_type_index = enneagram_var.get() - 1
        enneagram_type = enneagram_types[enneagram_type_index]

        history, attention_curve, correction_curve, meditation_points, breathing_points, voluntary_intention_points, total_attention_gain, total_breathing_gain, total_voluntary_intention_gain, accumulated_fatigue, avg_external_factors = simulate_with_voluntary(
            tasks, initial_attention, min_attention, max_attention,
            meditation_sessions, breathing_practices, enneagram_type, apply_meditation=True, apply_breathing=True
        )

        plot_simulation_with_voluntary(history, tasks, attention_curve, correction_curve, meditation_points, breathing_points, voluntary_intention_points, min_attention, meditation_sessions, breathing_practices)
        correction_buffer = plot_correction_curve(tasks, initial_attention, min_attention, max_attention, meditation_sessions, breathing_practices, enneagram_type)
        
        display_results(history, total_attention_gain, total_breathing_gain, total_voluntary_intention_gain, accumulated_fatigue, avg_external_factors, tasks)
        messagebox.showinfo("Success", "Simulation complete!")
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers.")

# Define other necessary functions for the GUI
def create_input_frame(label_text, row, container):
    frame = ttk.Frame(container, padding="10")
    frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))
    label = ttk.Label(frame, text=label_text)
    label.grid(row=0, column=0, sticky=tk.W)
    entry = ttk.Entry(frame)
    entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
    container.grid_columnconfigure(1, weight=1)
    return entry

def create_task_input_frame(row, task_num, container):
    frame = ttk.LabelFrame(container, text=f"Task {task_num + 1}", padding="10")
    frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))

    name_entry = create_labeled_entry(frame, "Name:", 0)
    duration_entry = create_labeled_entry(frame, "Duration (min):", 1)
    difficulty_entry = create_labeled_entry(frame, "Difficulty (1-5):", 2)
    base_attention_entry = create_labeled_entry(frame, "Base Attention (1-5):", 3)
    criticality_entry = create_labeled_entry(frame, "Criticality (0-5):", 4)
    start_time_entry = create_labeled_entry(frame, "Start Time (min):", 5)

    return [name_entry, duration_entry, difficulty_entry, base_attention_entry, criticality_entry, start_time_entry]

def create_meditation_input_frame(row, session_num, container):
    frame = ttk.LabelFrame(container, text=f"Meditation Session {session_num + 1}", padding="10")
    frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))

    start_time_entry = create_labeled_entry(frame, "Start Time (min):", 0)
    duration_entry = create_labeled_entry(frame, "Duration (min):", 1)
    effectiveness_entry = create_labeled_entry(frame, "Effectiveness (0-7):", 2)

    return [start_time_entry, duration_entry, effectiveness_entry]

def create_breathing_input_frame(row, practice_num, container):
    frame = ttk.LabelFrame(container, text=f"Breathing Practice {practice_num + 1}", padding="10")
    frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E))

    name_entry = create_labeled_entry(frame, "Name:", 0)
    start_time_entry = create_labeled_entry(frame, "Start Time (min):", 1)
    duration_entry = create_labeled_entry(frame, "Duration (min):", 2)
    effectiveness_entry = create_labeled_entry(frame, "Effectiveness (0-7):", 3)

    return [name_entry, start_time_entry, duration_entry, effectiveness_entry]

def create_labeled_entry(parent, label_text, row):
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=0, sticky=tk.W)
    entry = ttk.Entry(parent)
    entry.grid(row=row, column=1, sticky=(tk.W, tk.E))
    parent.grid_columnconfigure(1, weight=1)
    return entry

def on_num_tasks_change(*args):
    for widget in task_frames:
        widget.destroy()
    task_frames.clear()
    task_entries.clear()
    for i in range(num_tasks.get()):
        task_frames.append(create_task_input_frame(i + 6, i, scrollable_frame))
        task_entries.append(task_frames[-1])
    update_layout()

def on_num_meditations_change(*args):
    for widget in meditation_frames:
        widget.destroy()
    meditation_frames.clear()
    meditation_entries.clear()
    for i in range(num_meditations.get()):
        meditation_frames.append(create_meditation_input_frame(i + len(task_frames) + 6, i, scrollable_frame))
        meditation_entries.append(meditation_frames[-1])
    update_layout()

def on_num_breathings_change(*args):
    for widget in breathing_frames:
        widget.destroy()
    breathing_frames.clear()
    breathing_entries.clear()
    for i in range(num_breathings.get()):
        breathing_frames.append(create_breathing_input_frame(i + len(task_frames) + len(meditation_frames) + 6, i, scrollable_frame))
        breathing_entries.append(breathing_frames[-1])
    update_layout()

def update_layout():
    enneagram_frame.grid(row=len(task_frames) + len(meditation_frames) + len(breathing_frames) + 6, column=0, columnspan=2, sticky=(tk.W, tk.E))
    run_button.grid(row=len(task_frames) + len(meditation_frames) + len(breathing_frames) + 7, column=0, columnspan=2, pady=10)
    save_button.grid(row=len(task_frames) + len(meditation_frames) + len(breathing_frames) + 8, column=0, columnspan=2, pady=10)

def display_results(history, total_attention_gain, total_breathing_gain, total_voluntary_intention_gain, accumulated_fatigue, avg_external_factors, tasks):
    result_window = tk.Toplevel(root)
    result_window.title("Simulation Results")

    text = tk.Text(result_window, wrap='word', width=100, height=30, state='normal')
    text.grid(row=0, column=0, padx=10, pady=10)

    results = f"Total attention gain from meditation: {total_attention_gain}\n"
    results += f"Total attention gain from breathing practices: {total_breathing_gain}\n"
    results += f"Total attention gain from voluntary intention: {total_voluntary_intention_gain}\n\n"
    results += explain_attention_curve(history, tasks)
    results += f"\nTotal Accumulated Fatigue: {accumulated_fatigue}\n"
    results += f"Average External Factors: {avg_external_factors}\n"

    text.insert(tk.END, results)
    text.config(state='disabled')

def explain_attention_curve(history, tasks):
    result = "\nAttention Curve Analysis:\n"
    previous_task = None
    for entry in history:
        time, task_id, attention_level, fatigue_factor = entry
        task_name = tasks[task_id].name if task_id is not None else "No task"

        if task_name != previous_task:
            result += f"Time: {time} minutes - Attention shifted to: {task_name}\n"
            result += f"Fatigue Factor: {fatigue_factor}\n"
            result += f"Attention Level: {attention_level}\n"
            previous_task = task_name

    return result

def save_simulation_with_voluntary():
    result = run_simulation_with_voluntary()
    if result:
        history, attention_curve, tasks, meditation_sessions, breathing_practices, min_attention, buffer, correction_buffer, total_attention_gain, total_breathing_gain, accumulated_fatigue, avg_external_factors = result
        save_pdf(history, attention_curve, tasks, meditation_sessions, breathing_practices, min_attention, buffer, correction_buffer, total_attention_gain, total_breathing_gain, accumulated_fatigue, avg_external_factors)
        messagebox.showinfo("Success", "PDF saved!")

# Initialize the GUI
root = tk.Tk()
root.title("Attention Simulation")
root.geometry("600x400")  # Imposta la finestra a medie dimensioni
# Configura la griglia principale per espandersi con la finestra
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Configura la griglia del canvas per espandersi
scrollable_frame.grid_columnconfigure(0, weight=1)

initial_attention_entry = create_input_frame("Initial Attention Level:", 0, scrollable_frame)
min_attention_entry = create_input_frame("Minimum Attention Threshold:", 1, scrollable_frame)
max_attention_entry = create_input_frame("Maximum Attention Level:", 2, scrollable_frame)

num_tasks = tk.IntVar()
num_tasks.trace('w', on_num_tasks_change)
task_num_entry = create_input_frame("Enter the number of tasks:", 3, scrollable_frame)
task_num_entry.config(textvariable=num_tasks)

num_meditations = tk.IntVar()
num_meditations.trace('w', on_num_meditations_change)
meditation_num_entry = create_input_frame("Enter the number of meditation sessions:", 4, scrollable_frame)
meditation_num_entry.config(textvariable=num_meditations)

num_breathings = tk.IntVar()
num_breathings.trace('w', on_num_breathings_change)
breathing_num_entry = create_input_frame("Enter the number of breathing practices:", 5, scrollable_frame)
breathing_num_entry.config(textvariable=num_breathings)

task_frames = []
task_entries = []

meditation_frames = []
meditation_entries = []

breathing_frames = []
breathing_entries = []

enneagram_types = [
    EnneagramType(1, "Reformer", ["Precision", "Discipline"]),
    EnneagramType(2, "Helper", ["Empathy", "Generosity"]),
    EnneagramType(3, "Achiever", ["Focus", "Drive"]),
    EnneagramType(4, "Individualist", ["Creativity", "Authenticity"]),
    EnneagramType(5, "Investigator", ["Observation", "Analysis"]),
    EnneagramType(6, "Loyalist", ["Loyalty", "Responsibility"]),
    EnneagramType(7, "Enthusiast", ["Enthusiasm", "Curiosity"]),
    EnneagramType(8, "Challenger", ["Strength", "Protection"]),
    EnneagramType(9, "Peacemaker", ["Harmony", "Peace"])
]

enneagram_var = tk.IntVar()
enneagram_frame = ttk.LabelFrame(scrollable_frame, text="Select your Enneagram type:", padding="10")

for i, et in enumerate(enneagram_types):
    radio_button = ttk.Radiobutton(enneagram_frame, text=et.name, variable=enneagram_var, value=i+1)
    radio_button.grid(row=i, column=0, sticky=tk.W)

run_button = ttk.Button(scrollable_frame, text="Run Simulation", command=run_simulation_with_voluntary)
save_button = ttk.Button(scrollable_frame, text="Save PDF", command=save_simulation_with_voluntary)

# Inizializza il layout
update_layout()

root.mainloop()
