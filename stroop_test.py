import tkinter as tk
import random
import time
import csv
import os

NUM_TRIALS = 20

COLORS = ["red", "green", "blue", "yellow"]

trial_count = 0
correct_count = 0

congruent_times = []
incongruent_times = []

current_color = ""
current_trial_type = ""

start_time = 0
experiment_running = False

participant_age = ""

trial_types = []


def save_results(
    age,
    accuracy,
    congruent_count,
    incongruent_count,
    avg_congruent,
    avg_incongruent,
    stroop_effect
):
    filename = "stroop_results.csv"

    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Age",
                "Accuracy (%)",
                "Congruent Trials",
                "Incongruent Trials",
                "Congruent RT (s)",
                "Incongruent RT (s)",
                "Stroop Effect (s)"
            ])

        writer.writerow([
            age,
            round(accuracy, 2),
            congruent_count,
            incongruent_count,
            round(avg_congruent, 2),
            round(avg_incongruent, 2),
            round(stroop_effect, 2)
        ])


def start_experiment():
    global participant_age
    global trial_types

    participant_age = age_entry.get().strip()

    if participant_age == "":
        message_label.config(
            text="Please enter your age."
        )
        return

    if not participant_age.isdigit():
        message_label.config(
            text="Please enter a valid age."
        )
        return

    trial_types = (
        ["congruent"] * (NUM_TRIALS // 2)
        + ["incongruent"] * (NUM_TRIALS // 2)
    )

    random.shuffle(trial_types)

    title_label.pack_forget()
    age_label.pack_forget()
    age_entry.pack_forget()
    start_button.pack_forget()
    message_label.pack_forget()

    instructions.pack(pady=10)
    word_label.pack(expand=True)

    countdown(3)


def countdown(seconds):
    if seconds > 0:
        word_label.config(
            text=f"Starting in\n{seconds}",
            fg="black"
        )

        root.after(
            1000,
            lambda: countdown(seconds - 1)
        )

    else:
        word_label.config(
            text="GO!",
            fg="green"
        )

        root.after(1000, next_trial)


def next_trial():
    global trial_count
    global current_color
    global current_trial_type
    global start_time
    global experiment_running

    if trial_count >= NUM_TRIALS:
        show_results()
        return

    current_trial_type = trial_types[trial_count]

    if current_trial_type == "congruent":
        current_color = random.choice(COLORS)
        word = current_color

    else:
        current_color = random.choice(COLORS)

        possible_words = [
            color
            for color in COLORS
            if color != current_color
        ]

        word = random.choice(possible_words)

    word_label.config(
        text=word.upper(),
        fg=current_color
    )

    experiment_running = True
    start_time = time.time()


def key_pressed(event):
    global trial_count
    global correct_count
    global experiment_running

    if not experiment_running:
        return

    key = event.keysym.lower()

    color_map = {
        "r": "red",
        "g": "green",
        "b": "blue",
        "y": "yellow"
    }

    if key not in color_map:
        return

    reaction_time = time.time() - start_time

    experiment_running = False

    selected_color = color_map[key]

    if selected_color == current_color:
        correct_count += 1

    if current_trial_type == "congruent":
        congruent_times.append(reaction_time)
    else:
        incongruent_times.append(reaction_time)

    trial_count += 1

    word_label.config(
        text="+",
        fg="black"
    )

    root.after(1000, next_trial)


def show_results():
    instructions.pack_forget()
    word_label.pack_forget()

    accuracy = (correct_count / NUM_TRIALS) * 100

    avg_congruent = (
        sum(congruent_times) / len(congruent_times)
        if len(congruent_times) > 0
        else 0
    )

    avg_incongruent = (
        sum(incongruent_times) / len(incongruent_times)
        if len(incongruent_times) > 0
        else 0
    )

    stroop_effect = avg_incongruent - avg_congruent

    save_results(
        participant_age,
        accuracy,
        len(congruent_times),
        len(incongruent_times),
        avg_congruent,
        avg_incongruent,
        stroop_effect
    )

    result_text = (
        f"Age: {participant_age}\n\n"
        f"Accuracy: {accuracy:.1f}%\n\n"
        f"Congruent Trials: {len(congruent_times)}\n"
        f"Incongruent Trials: {len(incongruent_times)}\n\n"
        f"Average Congruent RT: "
        f"{avg_congruent:.2f} s\n"
        f"Average Incongruent RT: "
        f"{avg_incongruent:.2f} s\n\n"
        f"Stroop Effect: "
        f"{stroop_effect:.2f} s\n\n"
        f"Results saved to:\n"
        f"stroop_results.csv"
    )

    result_label = tk.Label(
        root,
        text=result_text,
        font=("Arial", 18),
        justify="center"
    )

    result_label.pack(expand=True)


# ---------- GUI ----------

root = tk.Tk()
root.title("Stroop Test Experiment")
root.geometry("800x600")

title_label = tk.Label(
    root,
    text="Stroop Test Experiment",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=20)

age_label = tk.Label(
    root,
    text="Enter Your Age:",
    font=("Arial", 14)
)
age_label.pack()

age_entry = tk.Entry(
    root,
    font=("Arial", 14),
    width=25
)
age_entry.pack(pady=5)

start_button = tk.Button(
    root,
    text="Start Test",
    font=("Arial", 14),
    command=start_experiment
)
start_button.pack(pady=20)

message_label = tk.Label(
    root,
    text="",
    fg="red",
    font=("Arial", 12)
)
message_label.pack()

instructions = tk.Label(
    root,
    text=(
        "Respond to the COLOR, not the word\n\n"
        "R = Red\n"
        "G = Green\n"
        "B = Blue\n"
        "Y = Yellow"
    ),
    font=("Arial", 16)
)

word_label = tk.Label(
    root,
    text="",
    font=("Arial", 64, "bold")
)

root.bind("<Key>", key_pressed)

root.mainloop()