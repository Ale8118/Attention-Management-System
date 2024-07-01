import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

def validate_input(prompt, validation_fn, error_message):
    while True:
        try:
            value = validation_fn(input(prompt))
            return value
        except ValueError:
            print(error_message)

def get_task_details():
    tasks = []
    num_tasks = validate_input("Enter the number of tasks: ", int, "Please enter a valid number.")
    
    for i in range(num_tasks):
        task_name = input(f"Enter name for task {i+1}: ")
        task_duration = validate_input(f"Enter duration for task '{task_name}' in minutes: ", float, "Please enter a valid duration.")
        task_difficulty = validate_input(f"Enter difficulty for task '{task_name}' (1 to 5): ", lambda x: float(x) if 1 <= float(x) <= 5 else ValueError(), "Please enter a difficulty between 1 and 5.")
        base_attention = validate_input(f"Enter base attention level for task '{task_name}' (1 to 5): ", lambda x: float(x) if 1 <= float(x) <= 5 else ValueError(), "Please enter a base attention level between 1 and 5.")
        criticality = validate_input(f"Enter criticality for task '{task_name}' (0 to 5): ", lambda x: float(x) if 0 <= float(x) <= 5 else ValueError(), "Please enter a criticality between 0 and 5.")
        start_time = validate_input(f"Enter start time for task '{task_name}' in minutes: ", float, "Please enter a valid start time.")
        task = Task(
            task_id=i,
            name=task_name,
            base_attention=base_attention,
            difficulty=task_difficulty,
            criticality=criticality,
            duration=task_duration,
            start_time=start_time
        )
        tasks.append(task)
    
    return tasks

def get_meditation_sessions():
    sessions = []
    num_sessions = validate_input("Enter the number of meditation sessions: ", int, "Please enter a valid number.")
    
    for i in range(num_sessions):
        start_time = validate_input(f"Enter start time for meditation session {i+1} in minutes: ", float, "Please enter a valid start time.")
        duration = validate_input(f"Enter duration for meditation session {i+1} in minutes: ", float, "Please enter a valid duration.")
        effectiveness = validate_input(f"Enter effectiveness for meditation session {i+1} (0 to 7): ", lambda x: float(x) if 0 <= float(x) <= 7 else ValueError(), "Please enter an effectiveness between 0 and 7.")
        session = MeditationSession(start_time, duration, effectiveness)
        sessions.append(session)
    
    return sessions

def modify_values(tasks, meditation_sessions, initial_attention, min_attention, max_attention):
    while True:
        print("\nCurrent values:")
        print(f"Initial Attention: {initial_attention}")
        print(f"Minimum Attention Threshold: {min_attention}")
        print(f"Maximum Attention: {max_attention}")
        print("Tasks:")
        for task in tasks:
            print(f"  Task {task.task_id + 1}: {task.name}, Duration: {task.duration} min, Difficulty: {task.difficulty}, Base Attention: {task.base_attention}, Criticality: {task.criticality}, Start Time: {task.start_time} min")
        print("Meditation Sessions:")
        for i, session in enumerate(meditation_sessions):
            print(f"  Session {i + 1}: Start Time: {session.start_time} min, Duration: {session.duration} min, Effectiveness: {session.effectiveness}")

        modify = input("Do you want to modify any values? (yes/no): ").strip().lower()
        if modify == "no":
            break

        section = input("Which section do you want to modify? (initial/min/max/tasks/meditation): ").strip().lower()
        if section == "initial":
            initial_attention = validate_input("Enter the initial attention level (e.g., 100): ", float, "Please enter a valid initial attention level.")
        elif section == "min":
            min_attention = validate_input("Enter the minimum attention threshold (e.g., 50): ", float, "Please enter a valid minimum attention threshold.")
        elif section == "max":
            max_attention = validate_input("Enter the maximum attention level (e.g., 100): ", float, "Please enter a valid maximum attention level.")
        elif section == "tasks":
            task_id = validate_input("Enter the task number to modify: ", int, "Please enter a valid task number.") - 1
            if 0 <= task_id < len(tasks):
                task_name = input(f"Enter name for task {task_id + 1}: ")
                task_duration = validate_input(f"Enter duration for task '{task_name}' in minutes: ", float, "Please enter a valid duration.")
                task_difficulty = validate_input(f"Enter difficulty for task '{task_name}' (1 to 5): ", lambda x: float(x) if 1 <= float(x) <= 5 else ValueError(), "Please enter a difficulty between 1 and 5.")
                base_attention = validate_input(f"Enter base attention level for task '{task_name}' (1 to 5): ", lambda x: float(x) if 1 <= float(x) <= 5 else ValueError(), "Please enter a base attention level between 1 and 5.")
                criticality = validate_input(f"Enter criticality for task '{task_name}' (0 to 5): ", lambda x: float(x) if 0 <= float(x) <= 5 else ValueError(), "Please enter a criticality between 0 and 5.")
                start_time = validate_input(f"Enter start time for task '{task_name}' in minutes: ", float, "Please enter a valid start time.")
                tasks[task_id] = Task(
                    task_id=task_id,
                    name=task_name,
                    base_attention=base_attention,
                    difficulty=task_difficulty,
                    criticality=criticality,
                    duration=task_duration,
                    start_time=start_time
                )
            else:
                print("Invalid task number.")
        elif section == "meditation":
            session_id = validate_input("Enter the meditation session number to modify: ", int, "Please enter a valid session number.") - 1
            if 0 <= session_id < len(meditation_sessions):
                start_time = validate_input(f"Enter start time for meditation session {session_id + 1} in minutes: ", float, "Please enter a valid start time.")
                duration = validate_input(f"Enter duration for meditation session {session_id + 1} in minutes: ", float, "Please enter a valid duration.")
                effectiveness = validate_input(f"Enter effectiveness for meditation session {session_id + 1} (0 to 7): ", lambda x: float(x) if 0 <= float(x) <= 7 else ValueError(), "Please enter an effectiveness between 0 and 7.")
                meditation_sessions[session_id] = MeditationSession(start_time, duration, effectiveness)
            else:
                print("Invalid meditation session number.")
        else:
            print("Invalid section.")

    return tasks, meditation_sessions, initial_attention, min_attention, max_attention

def simulate(tasks, initial_attention, min_attention, max_attention, meditation_sessions, apply_meditation):
    history = []
    attention_curve = []
    meditation_points = []
    total_attention_gain = 0
    current_time = 0
    attention_level = initial_attention

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
            
            attention_level -= task.difficulty
            if attention_level < min_attention:
                attention_level = min_attention

            history.append((current_time, task.task_id, attention_level, task.difficulty))
            attention_curve.append((current_time, task.task_id, task.difficulty, attention_level))
            current_time += 1

    accumulated_fatigue = sum(task.difficulty for task in tasks)
    avg_external_factors = sum(task.criticality for task in tasks) / len(tasks) if tasks else 0
    return history, attention_curve, meditation_points, total_attention_gain, accumulated_fatigue, avg_external_factors

def plot_simulation(history, tasks, attention_curve, meditation_points, min_attention, meditation_sessions):
    plt.figure(figsize=(12, 6))
    attention_times = [entry[0] for entry in attention_curve]
    attention_levels = [entry[3] for entry in attention_curve]
    
    plt.plot(attention_times, attention_levels, label='Attention Level', color='b')
    
    for task in tasks:
        plt.axvspan(task.start_time, task.start_time + task.duration, alpha=0.2, color='yellow', label=f'Task: {task.name}')
    
    for session in meditation_sessions:
        plt.axvspan(session.start_time, session.start_time + session.duration, alpha=0.2, color='green', label='Meditation')
    
    for meditation_time, attention_level in meditation_points:
        plt.scatter(meditation_time, attention_level, color='r', s=50, label='Meditation Point' if meditation_time == meditation_points[0][0] else "")
    
    plt.axhline(y=min_attention, color='gray', linestyle='--', label='Min Attention Threshold')
    plt.xlabel('Global Clock (minutes)')
    plt.ylabel('Attention Level')
    plt.title('Attention Level Over Time Considering Fatigue and Task Difficulty')
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Legend")
    plt.tight_layout()
    plt.show()

def plot_correction_curve(tasks, initial_attention, min_attention, max_attention, meditation_sessions):
    # Simulate without meditation
    _, attention_curve_no_meditation, _, _, _, _ = simulate(tasks, initial_attention, min_attention, max_attention, meditation_sessions, apply_meditation=False)
    # Simulate with meditation
    _, attention_curve_with_meditation, _, _, _, _ = simulate(tasks, initial_attention, min_attention, max_attention, meditation_sessions, apply_meditation=True)
    
    plt.figure(figsize=(12, 6))
    
    # Plot attention curve without meditation
    times_no_meditation = [entry[0] for entry in attention_curve_no_meditation]
    levels_no_meditation = [entry[3] for entry in attention_curve_no_meditation]
    plt.plot(times_no_meditation, levels_no_meditation, label='Attention without Meditation', color='b')
    
    # Plot attention curve with meditation
    times_with_meditation = [entry[0] for entry in attention_curve_with_meditation]
    levels_with_meditation = [entry[3] for entry in attention_curve_with_meditation]
    plt.plot(times_with_meditation, levels_with_meditation, label='Attention with Meditation', color='g')
    
    plt.axhline(y=min_attention, color='gray', linestyle='--', label='Min Attention Threshold')
    plt.xlabel('Global Clock (minutes)')
    plt.ylabel('Attention Level')
    plt.title('Attention Level Correction Curve Due to Meditation')
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Legend")
    plt.tight_layout()
    plt.show()

def explain_attention_curve(attention_task_ids, task_names, fatigue_factors, continuous_times, attention_levels, meditation_points, total_fatigue, avg_external_factors):
    print("\nAttention Curve Analysis:")
    previous_task = None
    for idx, task_id in enumerate(attention_task_ids):
        if task_id is None or task_id >= len(task_names):
            task_name = "No task"
        else:
            task_name = task_names[task_id]

        if task_name != previous_task:
            print(f"Time: {continuous_times[idx]} minutes - Attention shifted to: {task_name}")
            print(f"Fatigue Factor: {fatigue_factors[idx]}")
            print(f"Attention Level: {attention_levels[idx]}")
            previous_task = task_name
    
    print(f"Total Accumulated Fatigue: {total_fatigue}")
    print(f"Average External Factors: {avg_external_factors}")

def create_custom_template():
    print("Enter your custom template details:")
    task_name = input("Enter task name: ")
    task_duration = validate_input(f"Enter duration for task '{task_name}' in minutes: ", float, "Please enter a valid duration.")
    task_difficulty = validate_input(f"Enter difficulty for task '{task_name}' (1 to 5): ", lambda x: float(x) if 1 <= float(x) <= 5 else ValueError(), "Please enter a difficulty between 1 and 5.")
    base_attention = validate_input(f"Enter base attention level for task '{task_name}' (1 to 5): ", lambda x: float(x) if 1 <= float(x) <= 5 else ValueError(), "Please enter a base attention level between 1 and 5.")
    criticality = validate_input(f"Enter criticality for task '{task_name}' (0 to 5): ", lambda x: float(x) if 0 <= float(x) <= 5 else ValueError(), "Please enter a criticality between 0 and 5.")
    start_time = validate_input(f"Enter start time for task '{task_name}' in minutes: ", float, "Please enter a valid start time.")
    custom_task = Task(
        task_id=0,
        name=task_name,
        base_attention=base_attention,
        difficulty=task_difficulty,
        criticality=criticality,
        duration=task_duration,
        start_time=start_time
    )
    return custom_task

# Main program
while True:
    tasks = get_task_details()
    initial_attention = validate_input("Enter the initial attention level (e.g., 100): ", float, "Please enter a valid initial attention level.")
    min_attention = validate_input("Enter the minimum attention threshold (e.g., 50): ", float, "Please enter a valid minimum attention threshold.")
    max_attention = validate_input("Enter the maximum attention level (e.g., 100): ", float, "Please enter a valid maximum attention level.")
    meditation_sessions = get_meditation_sessions()

    tasks, meditation_sessions, initial_attention, min_attention, max_attention = modify_values(tasks, meditation_sessions, initial_attention, min_attention, max_attention)

    history, attention_curve, meditation_points, total_attention_gain, accumulated_fatigue, avg_external_factors = simulate(
        tasks, initial_attention, min_attention, max_attention,
        meditation_sessions, apply_meditation=True
    )
    plot_simulation(history, tasks, attention_curve, meditation_points, min_attention, meditation_sessions)
    plot_correction_curve(tasks, initial_attention, min_attention, max_attention, meditation_sessions)

    total_attention_recovered = sum(session.duration * session.effectiveness for session in meditation_sessions)
    print(f"\nTotal attention gain from meditation: {total_attention_recovered}")

    continuous_times = [entry[0] for entry in attention_curve]
    attention_levels = [entry[3] for entry in attention_curve]

    explain_attention_curve(
        [entry[1] for entry in attention_curve],
        [task.name for task in tasks],
        [entry[2] for entry in attention_curve],
        continuous_times,
        attention_levels,
        meditation_points,
        accumulated_fatigue,
        avg_external_factors
    )

    action = input("Do you want to run the program again, modify values, or exit? (run/modify/exit): ").strip().lower()
    if action == "exit":
        break
    elif action == "modify":
        tasks, meditation_sessions, initial_attention, min_attention, max_attention = modify_values(tasks, meditation_sessions, initial_attention, min_attention, max_attention)
    elif action == "run":
        continue
    else:
        print("Invalid option. Exiting the program.")
        break
