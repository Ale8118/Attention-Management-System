import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import make_interp_spline

class BasicTask:
    def __init__(self, name, duration, difficulty):
        self.name = name
        self.duration = duration
        self.difficulty = difficulty
        self.waiting_time = 0

class Task:
    def __init__(self, task_id, name, basic_tasks, base_attention, criticality):
        self.task_id = task_id
        self.name = name
        self.basic_tasks = basic_tasks
        self.base_attention = base_attention
        self.criticality = criticality
        self.current_index = 0

    def is_completed(self):
        return self.current_index >= len(self.basic_tasks)

    def next_basic_task(self):
        if self.is_completed():
            return None
        return self.basic_tasks[self.current_index]

    def complete_basic_task(self):
        if not self.is_completed():
            self.current_index += 1

def meditation(current_attention, max_attention, meditation_duration, meditation_effectiveness):
    attention_gain = meditation_duration * meditation_effectiveness
    new_attention = current_attention + attention_gain
    return min(new_attention, max_attention), attention_gain

class CustomTask:
    def __init__(self, name, duration, attention_demand):
        self.name = name
        self.duration = duration
        self.attention_demand = attention_demand
        self.completed = False
        self.basic_tasks = []

    def is_completed(self):
        return all(task.is_completed() for task in self.basic_tasks)

    def complete_task(self):
        self.completed = True

    def add_basic_task(self, name, duration, difficulty):
        basic_task = BasicTask(name, duration, difficulty)
        self.basic_tasks.append(basic_task)

    def next_basic_task(self):
        if self.basic_tasks:
            return self.basic_tasks[0]
        else:
            return None

def simulate(tasks, initial_attention, min_attention, max_attention, meditation_start, meditation_duration, meditation_effectiveness):
    global_clock = 0
    history = []
    attention_curve = []
    fatigue_factor = 1.0
    current_attention = initial_attention
    meditation_points = []
    total_attention_gain = 0

    while not all(task.is_completed() for task in tasks):
        enabled_tasks = [(task, task.next_basic_task()) for task in tasks if not task.is_completed() and task.next_basic_task().waiting_time <= global_clock]
        if enabled_tasks:
            probabilities = [task.criticality * basic_task.duration * basic_task.difficulty / fatigue_factor for task, basic_task in enabled_tasks]
            total = sum(probabilities)
            if total == 0:
                probabilities = [1 / len(enabled_tasks)] * len(enabled_tasks)
            else:
                probabilities = [p / total for p in probabilities]
            chosen_index = np.random.choice(len(enabled_tasks), p=probabilities)
            chosen_task, chosen_basic_task = enabled_tasks[chosen_index]
            if current_attention >= min_attention:
                history.append((global_clock, chosen_task.task_id, chosen_basic_task.duration))
                global_clock += chosen_basic_task.duration
                attention_curve.append((global_clock, chosen_task.task_id, fatigue_factor, current_attention))
                chosen_task.complete_basic_task()
                current_attention -= chosen_basic_task.difficulty * chosen_basic_task.duration * 0.01
                fatigue_factor *= (1 + chosen_basic_task.difficulty * 0.1)
            else:
                if global_clock >= meditation_start:
                    previous_attention = current_attention
                    current_attention, attention_gain = meditation(current_attention, max_attention, meditation_duration, meditation_effectiveness)
                    total_attention_gain += attention_gain
                    meditation_points.append((global_clock, current_attention, fatigue_factor))
                    attention_curve.append((global_clock, None, fatigue_factor, current_attention, "Meditation performed"))
                    print(f"Meditation at {global_clock} minutes increased attention by {attention_gain} to {current_attention}")
                    global_clock += meditation_duration
                    fatigue_factor *= 1.01
                    continue
        else:
            global_clock += 1
            attention_curve.append((global_clock, None, fatigue_factor, current_attention))
            fatigue_factor *= 1.01
            current_attention -= 0.1

    # Add calculated attention gain at the end of the process
    final_attention_gain = meditation_duration * meditation_effectiveness
    if attention_curve:
        last_entry = attention_curve[-1]
        new_attention_level = last_entry[3] + final_attention_gain
        attention_curve.append((global_clock + 1, None, fatigue_factor, new_attention_level, "Final Attention Gain"))
        print(f"\nFinal attention gain of {final_attention_gain} added, resulting in new attention level of {new_attention_level}.")

    # Calculate attention recovered using the provided formula
    for meditation_time, attention_level, fatigue in meditation_points:
        attention_recovered = meditation_effectiveness * meditation_duration * (attention_level / fatigue)
        print(f"At time {meditation_time} minutes, attention recovered by meditation: {attention_recovered:.2f}")

    return history, attention_curve, meditation_points, total_attention_gain



def plot_simulation(history, tasks, attention_curve, meditation_points, min_attention, meditation_duration):
    times = [entry[0] for entry in history]
    task_ids = [entry[1] for entry in history]
    durations = [entry[2] for entry in history]

    plt.figure(figsize=(12, 6))
    task_colors = plt.cm.tab20(np.linspace(0, 1, len(tasks)))
    task_patches = []

    for task, color in zip(tasks, task_colors):
        task_patches.append(mpatches.Patch(color=color, label=task.name))
        task_history = [(time, duration) for time, task_id, duration in zip(times, task_ids, durations) if task_id == task.task_id]
        for start_time, duration in task_history:
            plt.plot([start_time, start_time + duration], [task.task_id, task.task_id], color=color, lw=2)

    task_names = [task.name for task in tasks]
    plt.xlabel('Global Clock (minutes)')
    plt.ylabel('Task')
    plt.title('Simulation of Selective Attention')
    plt.yticks(range(len(task_names)), task_names)
    plt.legend(handles=task_patches, loc='upper right')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(12, 6))
    attention_times = [entry[0] for entry in attention_curve]
    attention_task_ids = [entry[1] if entry[1] is not None else -1 for entry in attention_curve]
    fatigue_factors = [entry[2] for entry in attention_curve]
    attention_levels = [entry[3] for entry in attention_curve]

    continuous_times = []
    continuous_task_ids = []
    continuous_fatigue_factors = []
    continuous_attention_levels = []

    last_time = 0
    last_task_id = -1

    for time, task_id, fatigue, attention in zip(attention_times, attention_task_ids, fatigue_factors, attention_levels):
        if task_id != last_task_id:
            continuous_times.append(last_time)
            continuous_task_ids.append(last_task_id)
            continuous_fatigue_factors.append(fatigue)
            continuous_attention_levels.append(attention)
        continuous_times.append(time)
        continuous_task_ids.append(task_id)
        continuous_fatigue_factors.append(fatigue)
        continuous_attention_levels.append(attention)
        last_time = time
        last_task_id = task_id

    plt.plot(continuous_times, continuous_attention_levels, label='Attention Levels')
    plt.axhline(y=min_attention, color='r', linestyle='--', label='Min Attention Threshold')
    for meditation_time, attention_level, _ in meditation_points:
        plt.scatter(meditation_time, attention_level, color='g', s=50, label='Meditation' if meditation_time == meditation_points[0][0] else "")
        plt.plot([meditation_time - meditation_duration, meditation_time], [attention_levels[attention_times.index(meditation_time) - 1], attention_level], color='g', linestyle='--')
    plt.xlabel('Global Clock (minutes)')
    plt.ylabel('Attention Level')
    plt.title('Attention Levels Over Time')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(attention_times, fatigue_factors, label='Fatigue Factor')
    for meditation_time, _, fatigue_factor in meditation_points:
        plt.scatter(meditation_time, fatigue_factor, color='b', s=50, label='Meditation' if meditation_time == meditation_points[0][0] else "")
        plt.plot([meditation_time - meditation_duration, meditation_time], [fatigue_factors[attention_times.index(meditation_time) - 1], fatigue_factor], color='b', linestyle='--')
    plt.xlabel('Global Clock (minutes)')
    plt.ylabel('Fatigue Factor')
    plt.title('Fatigue Factor Over Time')
    plt.grid(True)
    plt.legend()
    plt.show()

def explain_attention_curve(attention_task_ids, task_names, fatigue_factors, continuous_times, attention_levels, meditation_points):
    print("\nAttention Curve Analysis:")
    previous_task = None
    for idx, task_id in enumerate(attention_task_ids):
        if task_id is None:
            task_name = "No task"
        else:
            task_name = task_names[task_id]

        if task_name != previous_task:
            print(f"Time: {continuous_times[idx]} minutes - Attention shifted to: {task_name}")
            print(f"Fatigue Factor: {fatigue_factors[idx]}")
            print(f"Attention Level: {attention_levels[idx]}")
            previous_task = task_name

def create_custom_template():
    print("Enter your custom template details:")
    task_name = input("Enter task name: ")
    task_duration = float(input(f"Enter duration for task '{task_name}' in minutes: "))
    task_difficulty = float(input(f"Enter difficulty for task '{task_name}' (1 to 5): "))
    base_attention = float(input(f"Enter base attention level for task '{task_name}' (0 to 1): "))
    criticality = float(input(f"Enter criticality for task '{task_name}' (0 to 5): "))
    custom_task = Task(
        task_id=0,
        name=task_name,
        basic_tasks=[BasicTask(name=task_name, duration=task_duration, difficulty=task_difficulty)],
        base_attention=base_attention,
        criticality=criticality
    )
    return [custom_task]




def calculate_attention_gain(meditation_points, attention_levels, continuous_times, focus_level_function):
    total_attention_gain = 0
    attention_gains = []
    for meditation_time, attention_level, _ in meditation_points:
        prev_index = continuous_times.index(meditation_time) - 1
        previous_attention_level = attention_levels[prev_index] if prev_index >= 0 else 0
        attention_gain = attention_level - previous_attention_level
        focus_level = focus_level_function((meditation_time, attention_level))

        adjusted_attention_gain = attention_gain * focus_level * (meditation_time - continuous_times[prev_index])

        total_attention_gain += adjusted_attention_gain
        attention_gains.append((meditation_time, attention_gain, adjusted_attention_gain))
        print(f"Meditation at {meditation_time} minutes increased attention by {attention_gain} to {attention_level} (Adjusted Gain: {adjusted_attention_gain:.2f})")

    print(f"\nTotal attention gain from meditation: {total_attention_gain:.2f}")
    return total_attention_gain, attention_gains

# Example usage (replace focus_level_function with your implementation)
def example_focus_level_function(meditation_point):
    return 0.7  # Placeholder focus level


def create_custom_template():
    print("Enter your custom template details:")
    task_name = input("Enter task name: ")
    task_duration = float(input(f"Enter duration for task '{task_name}' in minutes: "))
    task_difficulty = float(input(f"Enter difficulty for task '{task_name}' (1 to 5): "))
    base_attention = float(input(f"Enter base attention level for task '{task_name}' (0 to 1): "))
    criticality = float(input(f"Enter criticality for task '{task_name}' (0 to 5): "))
    custom_task = Task(
        task_id=0,
        name=task_name,
        basic_tasks=[BasicTask(name=task_name, duration=task_duration, difficulty=task_difficulty)],
        base_attention=base_attention,
        criticality=criticality
    )
    return [custom_task]

def choose_template():
    print("Choose a template:")
    print("1. Office Work")
    print("2. Home Chores")
    print("3. Personal Projects")
    print("4. Critical Situations")
    print("5. Emergency Management")
    print("6. Product Launch")
    print("7. Medical Facility Operations")
    print("8. Software Development")
    print("9. Scientific Research Project")
    print("10. Construction Project Management")
    print("11. Event Planning and Coordination")
    print("12. High-Stress Office Work")
    print("13. Intense Academic Research")
    print("14. Critical Infrastructure Maintenance")
    print("15. Emergency Response Coordination")
    print("16. Intensive Care Unit Management")
    #print("17. Custom Template")
    choice = int(input("Enter the number of your choice: "))

    if choice == 1:
        return office_work_template()
    elif choice == 2:
        return home_chores_template()
    elif choice == 3:
        return personal_projects_template()
    elif choice == 4:
        return critical_situations_template()
    elif choice == 5:
        return emergency_management_template()
    elif choice == 6:
        return product_launch_template()
    elif choice == 7:
        return medical_facility_operations_template()
    elif choice == 8:
        return software_development_template()
    elif choice == 9:
        return scientific_research_project_template()
    elif choice == 10:
        return construction_project_management_template()
    elif choice == 11:
        return event_planning_coordination_template()
    elif choice == 12:
        return high_stress_office_work_template()
    elif choice == 13:
        return intense_academic_research_template()
    elif choice == 14:
        return critical_infrastructure_maintenance_template()
    elif choice == 15:
        return emergency_response_coordination_template()
    elif choice == 16:
        return intensive_care_unit_management_template()
    elif choice == 17:
        return create_custom_template()
    else:
        print("Invalid choice. Please try again.")
        return choose_template()



def create_custom_template():
    print("Enter your custom template details:")
    task_name = input("Enter task name: ")
    task_duration = float(input(f"Enter duration for task '{task_name}' in minutes: "))
    task_attention_demand = float(input(f"Enter attention demand for task '{task_name}' (0 to 1): "))
    custom_task = CustomTask(task_name, task_duration, task_attention_demand)
    return [custom_task]

def office_work_template():
    tasks = [
        Task(0, "Email Management", [BasicTask("Email Management", 15, 0.5), BasicTask("Follow Up", 10, 0.5)], 0.8, 0),
        Task(1, "Project Planning", [BasicTask("Initial Planning", 30, 0.7)], 0.75, 1),
        Task(2, "Meeting", [BasicTask("Team Meeting", 45, 0.6)], 0.7, 2),
        Task(3, "Report Writing", [BasicTask("Write Report", 60, 0.5)], 0.65, 3),
        Task(4, "Team Coordination", [BasicTask("Coordinate", 30, 0.6)], 0.7, 4)
    ]
    return tasks

def home_chores_template():
    tasks = [
        Task(0, "Cooking", [BasicTask("Prepare Ingredients", 15, 0.5), BasicTask("Cook Meal", 10, 0.5)], 0.8, 0),
        Task(1, "Cleaning", [BasicTask("Clean Kitchen", 20, 0.6)], 0.7, 1),
        Task(2, "Laundry", [BasicTask("Wash Clothes", 30, 0.4)], 0.6, 2)
    ]
    return tasks

def personal_projects_template():
    tasks = [
        Task(0, "Reading", [BasicTask("Read Book", 30, 0.5)], 0.7, 0),
        Task(1, "Writing", [BasicTask("Write Article", 45, 0.7)], 0.8, 1),
        Task(2, "Exercise", [BasicTask("Workout", 20, 0.6)], 0.9, 2)
    ]
    return tasks

def critical_situations_template():
    tasks = [
        Task(0, "Emergency Response", [BasicTask("Initial Response", 10, 1.0), BasicTask("Follow Up", 15, 1.0)], 1.0, 0),
        Task(1, "System Monitoring", [BasicTask("Monitor Systems", 60, 0.8)], 0.9, 1),
        Task(2, "Critical Decision Making", [BasicTask("Make Decision", 30, 0.9)], 0.95, 2)
    ]
    return tasks

def emergency_management_template():
    tasks = [
        Task(0, "Fire Alarm Response", [BasicTask("Initial Response", 5, 1.0), BasicTask("Follow Up", 10, 1.0)], 1.0, 0),
        Task(1, "Evacuation Plan", [BasicTask("Plan Evacuation", 20, 0.9)], 0.9, 1),
        Task(2, "Medical Assistance", [BasicTask("Assist Patients", 30, 0.8)], 0.95, 2),
        Task(3, "Resource Coordination", [BasicTask("Coordinate Resources", 25, 0.7)], 0.85, 3),
        Task(4, "Communication Management", [BasicTask("Manage Communication", 15, 0.8), BasicTask("Follow Up", 10, 0.8)], 0.9, 4)
    ]
    return tasks

def product_launch_template():
    tasks = [
        Task(0, "Market Research", [BasicTask("Research Market", 30, 0.6)], 0.8, 0),
        Task(1, "Product Design", [BasicTask("Design Product", 45, 0.9)], 0.9, 1),
        Task(2, "Prototyping", [BasicTask("Create Prototype", 60, 0.8)], 0.9, 2),
        Task(3, "Testing", [BasicTask("Test Product", 50, 0.7)], 0.8, 3),
        Task(4, "Marketing Strategy", [BasicTask("Plan Marketing", 40, 0.7)], 0.85, 4),
        Task(5, "Sales Plan", [BasicTask("Plan Sales", 35, 0.8)], 0.8, 5),
        Task(6, "Launch Event", [BasicTask("Plan Event", 20, 0.9)], 0.9, 6)
    ]
    return tasks

def medical_facility_operations_template():
    tasks = [
        Task(0, "Patient Checkup", [BasicTask("Initial Checkup", 20, 0.5), BasicTask("Follow Up", 15, 0.5)], 0.7, 0),
        Task(1, "Surgery", [BasicTask("Perform Surgery", 90, 1.0)], 1.0, 1),
        Task(2, "Emergency Care", [BasicTask("Provide Care", 30, 0.9)], 0.95, 2),
        Task(3, "Medication Administration", [BasicTask("Administer Medication", 10, 0.7)], 0.8, 3),
        Task(4, "Record Keeping", [BasicTask("Update Records", 25, 0.6)], 0.7, 4),
        Task(5, "Staff Coordination", [BasicTask("Coordinate Staff", 20, 0.7)], 0.75, 5),
        Task(6, "Facility Maintenance", [BasicTask("Maintain Facility", 40, 0.6)], 0.65, 6)
    ]
    return tasks

def software_development_template():
    tasks = [
        Task(0, "Requirement Analysis", [BasicTask("Analyze Requirements", 30, 0.5)], 0.7, 0),
        Task(1, "System Design", [BasicTask("Design System", 45, 0.8)], 0.85, 1),
        Task(2, "Coding", [BasicTask("Write Code", 60, 0.9)], 0.9, 2),
        Task(3, "Testing", [BasicTask("Test Code", 40, 0.7)], 0.8, 3),
        Task(4, "Debugging", [BasicTask("Debug Code", 30, 0.8)], 0.8, 4),
        Task(5, "Documentation", [BasicTask("Write Documentation", 20, 0.6)], 0.65, 5),
        Task(6, "Deployment", [BasicTask("Deploy System", 35, 0.8)], 0.8, 6)
    ]
    return tasks

def scientific_research_project_template():
    tasks = [
        Task(0, "Literature Review", [BasicTask("Review Literature", 40, 0.6)], 0.75, 0),
        Task(1, "Experiment Design", [BasicTask("Design Experiment", 50, 0.7)], 0.8, 1),
        Task(2, "Data Collection", [BasicTask("Collect Data", 60, 0.8)], 0.85, 2),
        Task(3, "Data Analysis", [BasicTask("Analyze Data", 45, 0.8)], 0.85, 3),
        Task(4, "Hypothesis Testing", [BasicTask("Test Hypothesis", 30, 0.9)], 0.9, 4),
        Task(5, "Report Writing", [BasicTask("Write Report", 35, 0.7)], 0.75, 5),
        Task(6, "Presentation Preparation", [BasicTask("Prepare Presentation", 25, 0.7)], 0.75, 6)
    ]
    return tasks

def construction_project_management_template():
    tasks = [
        Task(0, "Site Preparation", [BasicTask("Prepare Site", 20, 0.7)], 0.75, 0),
        Task(1, "Foundation Work", [BasicTask("Lay Foundation", 50, 0.9)], 0.9, 1),
        Task(2, "Framing", [BasicTask("Frame Building", 40, 0.8)], 0.85, 2),
        Task(3, "Electrical and Plumbing", [BasicTask("Install Systems", 60, 0.8)], 0.85, 3),
        Task(4, "Interior Work", [BasicTask("Finish Interior", 45, 0.7)], 0.8, 4),
        Task(5, "Exterior Work", [BasicTask("Finish Exterior", 35, 0.7)], 0.8, 5),
        Task(6, "Final Inspection", [BasicTask("Inspect Building", 30, 0.9)], 0.9, 6)
    ]
    return tasks

def event_planning_coordination_template():
    tasks = [
        Task(0, "Venue Selection", [BasicTask("Select Venue", 15, 0.6)], 0.7, 0),
        Task(1, "Guest List Management", [BasicTask("Manage List", 25, 0.7)], 0.75, 1),
        Task(2, "Catering Arrangement", [BasicTask("Arrange Catering", 20, 0.8)], 0.8, 2),
        Task(3, "Decoration", [BasicTask("Decorate Venue", 30, 0.7)], 0.75, 3),
        Task(4, "Entertainment Planning", [BasicTask("Plan Entertainment", 35, 0.8)], 0.8, 4),
        Task(5, "Logistics Coordination", [BasicTask("Coordinate Logistics", 20, 0.7)], 0.75, 5),
        Task(6, "On-site Management", [BasicTask("Manage On-site", 40, 0.9)], 0.85, 6)
    ]
    return tasks

def high_stress_office_work_template():
    tasks = [
        Task(0, "Urgent Emails", [BasicTask("Respond to Emails", 5, 1.0), BasicTask("Follow Up", 5, 1.0)], 1.0, 0),
        Task(1, "Critical Report", [BasicTask("Write Report", 60, 1.0)], 1.0, 1),
        Task(2, "Emergency Meeting", [BasicTask("Attend Meeting", 30, 0.9)], 0.95, 2),
        Task(3, "Client Presentation", [BasicTask("Prepare Presentation", 40, 0.9)], 0.95, 3),
        Task(4, "System Outage", [BasicTask("Fix Outage", 50, 1.0)], 1.0, 4),
        Task(5, "Budget Review", [BasicTask("Review Budget", 45, 0.9)], 0.9, 5),
        Task(6, "Team Coordination", [BasicTask("Coordinate Team", 35, 0.8)], 0.85, 6)
    ]
    return tasks

def intense_academic_research_template():
    tasks = [
        Task(0, "Grant Proposal Writing", [BasicTask("Write Proposal", 60, 1.0)], 1.0, 0),
        Task(1, "Data Analysis", [BasicTask("Analyze Data", 50, 0.9)], 0.95, 1),
        Task(2, "Field Study", [BasicTask("Conduct Study", 90, 1.0)], 1.0, 2),
        Task(3, "Manuscript Preparation", [BasicTask("Prepare Manuscript", 45, 0.9)], 0.95, 3),
        Task(4, "Conference Presentation", [BasicTask("Prepare Presentation", 30, 0.8)], 0.9, 4),
        Task(5, "Collaborative Meeting", [BasicTask("Attend Meeting", 35, 0.7)], 0.85, 5),
        Task(6, "Experiment Setup", [BasicTask("Setup Experiment", 40, 0.8)], 0.9, 6)
    ]
    return tasks

def critical_infrastructure_maintenance_template():
    tasks = [
        Task(0, "Power Grid Monitoring", [BasicTask("Monitor Grid", 60, 1.0)], 1.0, 0),
        Task(1, "Network Security Check", [BasicTask("Check Security", 45, 0.9)], 0.95, 1),
        Task(2, "Emergency Repair", [BasicTask("Repair System", 50, 1.0)], 1.0, 2),
        Task(3, "System Diagnostics", [BasicTask("Run Diagnostics", 30, 0.8)], 0.9, 3),
        Task(4, "Routine Maintenance", [BasicTask("Perform Maintenance", 40, 0.7)], 0.85, 4),
        Task(5, "Backup System Activation", [BasicTask("Activate Backup", 35, 0.9)], 0.9, 5),
        Task(6, "Load Balancing", [BasicTask("Balance Load", 20, 0.7)], 0.8, 6)
    ]
    return tasks

def emergency_response_coordination_template():
    tasks = [
        Task(0, "Disaster Assessment", [BasicTask("Assess Disaster", 20, 1.0)], 1.0, 0),
        Task(1, "Resource Allocation", [BasicTask("Allocate Resources", 40, 0.9)], 0.95, 1),
        Task(2, "Team Deployment", [BasicTask("Deploy Teams", 30, 0.8)], 0.9, 2),
        Task(3, "Public Communication", [BasicTask("Communicate with Public", 25, 0.8)], 0.85, 3),
        Task(4, "Situation Monitoring", [BasicTask("Monitor Situation", 35, 0.7)], 0.85, 4),
        Task(5, "Coordination with Authorities", [BasicTask("Coordinate with Authorities", 50, 0.9)], 0.9, 5),
        Task(6, "Medical Assistance", [BasicTask("Provide Medical Assistance", 60, 1.0)], 1.0, 6)
    ]
    return tasks

def intensive_care_unit_management_template():
    tasks = [
        Task(0, "Patient Monitoring", [BasicTask("Monitor Patient", 15, 0.8), BasicTask("Follow Up", 15, 0.8)], 0.9, 0),
        Task(1, "Emergency Procedures", [BasicTask("Perform Procedure", 30, 1.0)], 1.0, 1),
        Task(2, "Medication Administration", [BasicTask("Administer Medication", 20, 0.7)], 0.8, 2),
        Task(3, "Family Communication", [BasicTask("Communicate with Family", 25, 0.6)], 0.75, 3),
        Task(4, "Staff Coordination", [BasicTask("Coordinate Staff", 35, 0.8)], 0.85, 4),
        Task(5, "Equipment Management", [BasicTask("Manage Equipment", 40, 0.7)], 0.8, 5),
        Task(6, "Documentation", [BasicTask("Document Records", 30, 0.6)], 0.75, 6)
    ]
    return tasks

def plot_meditation_efficiency(meditation_duration, meditation_effectiveness, attention_curve):
    if not attention_curve:
        print("No attention curve data to plot.")
        return

    # Simulating an improvement in attention recovery over time with consideration of fatigue and task difficulty
    meditation_times = np.arange(0, meditation_duration + 1, 1)
    attention_recovered = []

    for t in meditation_times:
        fatigue_factor = np.interp(t, [0, meditation_duration], [attention_curve[0][2], attention_curve[-1][2]])
        task_difficulty_factor = np.mean([entry[2] for entry in attention_curve])
        recovered = meditation_effectiveness * t * (1 / (1 + fatigue_factor * task_difficulty_factor))
        attention_recovered.append(recovered)

    plt.figure(figsize=(12, 6))
    plt.plot(meditation_times, attention_recovered, 'ro-', label='Attention Recovered by Meditation')
    plt.xlabel('Meditation Duration (minutes)')
    plt.ylabel('Attention Recovered')
    plt.title('Attention Recovered by Meditation Over Time Considering Fatigue and Task Difficulty')
    plt.grid(True)
    plt.legend()
    plt.show()


# Main program
tasks = choose_template()
initial_attention = float(input("Enter the initial attention level (e.g., 100): "))
min_attention = float(input("Enter the minimum attention threshold (e.g., 50): "))
max_attention = 100  # Define the maximum attention level
meditation_start = float(input("Enter the time (in minutes) when meditation should start: "))
meditation_duration = float(input("Enter the duration of meditation in minutes (e.g., 5): "))
meditation_effectiveness = float(input("Enter the effectiveness of meditation (0 to 7): "))

history, attention_curve, meditation_points, total_attention_gain = simulate(tasks, initial_attention, min_attention, max_attention, meditation_start, meditation_duration, meditation_effectiveness)
plot_simulation(history, tasks, attention_curve, meditation_points, min_attention, meditation_duration)
# Plot meditation-specific graph
plot_meditation_efficiency(meditation_duration, meditation_effectiveness, attention_curve)

total_attention_recovered = meditation_duration * meditation_effectiveness
print(f"\nTotal attention gain from meditation: {total_attention_recovered}")

# Call explain_attention_curve and print the result once
continuous_times = [entry[0] for entry in attention_curve]
attention_levels = [entry[3] for entry in attention_curve]

explain_attention_curve(
    [entry[1] for entry in attention_curve],
    [task.name for task in tasks],
    [entry[2] for entry in attention_curve],
    continuous_times,
    attention_levels,
    meditation_points
)

#plot_simulation(history, tasks, attention_curve, meditation_points, min_attention, meditation_duration)






# Call calculate_attention_gain and print the result
#total_gain, gains = calculate_attention_gain(meditation_points, attention_levels, continuous_times, example_focus_level_function)
#print(f"\nTotal attention gain from meditation: {total_gain:.2f}")

