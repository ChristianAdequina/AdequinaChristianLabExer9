import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches


# ---------------- Encoding Functions -----------------
def nrz_l(bits):
    return [1 if bit == '1' else 0 for bit in bits]


def nrz_i(bits):
    level = 0  # Initially low
    signal = []
    for bit in bits:
        if bit == '1':
            level = 1 - level  # If '1', flip the level (low -> high, high -> low)
        signal.append(level)
    return signal


def bipolar_ami(bits):
    level = 1  # Start at positive voltage for the first '1'
    signal = []

    for bit in bits:
        if bit == '1':
            signal.append(level)  # Attach the bit, then flip the level
            level = 0 if level == 1 else 1
        else:
            signal.append(0.5)  # Stay at middle if '0'

    return signal


def pseudoternary(bits):
    level = 1  # Start at positive voltage for the first '0'
    signal = []

    for bit in bits:
        if bit == '0':
            signal.append(level)  # Attach the bit, then flip the level
            level = 0 if level == 1 else 1
        else:
            signal.append(0.5)  # Middle voltage for '1'

    return signal


def manchester(bits):
    signal = []
    for bit in bits:
        if bit == '0':
            signal.extend([1, 0])  # High to low
        else:
            signal.extend([0, 1])  # Low to high
    return signal


def diff_manchester(bits):
    signal = []
    previous_level = 1

    for bit in bits:
        if bit == '0':
            # If the previous signal was high-to-low, stay high-to-low
            if previous_level == 0:
                signal.extend([1, 0])  # High to low
                previous_level = 0  # The current level is now low
            # Else if it was low-to-high, stay low-to-high
            else:
                signal.extend([0, 1])  # Low to high
                previous_level = 1  # The current level is now high
        else:  # bit == '1'
            # If the previous signal was high-to-low, go low-to-high
            if previous_level == 0:
                signal.extend([0, 1])  # Low to high
                previous_level = 1  # The current level is now high
            # If the previous signal was low-to-high, go high-to-low
            else:
                signal.extend([1, 0])  # High to low
                previous_level = 0  # The current level is now low

    return signal

# ------------------- Plotting ----------------------
def plot_signal(bits, signal, title):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Add an extra time point to draw the last horizontal line
    time = np.arange(0, len(signal) + 1)  # Add 1 to time to extend it by one step
    signal = np.append(signal, signal[-1])  # Append the last value to signal to hold it

    ax.set_ylim(-0.5, 2)
    ax.set_xlim(0, len(signal))
    ax.set_xlabel("Time")
    ax.set_ylabel("Voltage Level")
    ax.set_title(f"{title} Encoding")
    ax.grid(True)
    ax.step(time, signal, where='post', label=title)
    ax.legend()

    # Draw the bit text
    step_size = 1  # Step size '1' for NRZ's, Bipolar, Pseudo
    for i, bit in enumerate(bits):
        if title in ["Manchester", "Differential Manchester"]:
            step_size = 2 # Different step size due to the transition in the middle
            # Draw a rectangle behind each digit
            rect_x = i * step_size + 0.6  # Adjust position for "block" layout
            rect = patches.Rectangle((rect_x, 1.5), 0.8, 0.5, linewidth=1, edgecolor='black', facecolor='lightgray',
                                     zorder=2)
            ax.add_patch(rect)

            # Place the bit text over the rectangle
            ax.text(i * step_size + 1, 1.75, bit, ha='center', va='center', fontsize=12, color='black', zorder=3)
        else:
            rect_x = i * step_size + 0.25  # Adjust position for "block" layout
            rect = patches.Rectangle((rect_x, 1.5), 0.5, 0.5, linewidth=1, edgecolor='black', facecolor='lightgray',
                                     zorder=2)
            ax.add_patch(rect)

            ax.text(i * step_size + 0.5, 1.75, bit, ha='center', va='center', fontsize=12, color='black', zorder=3)

    return fig


# ----------------- Streamlit UI ----------------------------
st.title("Signal Encoding Viewer")

# Input field for the bit string
bit_string = st.text_input("Enter bit string (e.g., 101010):")

if bit_string:
    # Encoding selection
    encoding_type = st.selectbox("Choose Encoding Type:", [
        "NRZ-L", "NRZ-I", "Bipolar AMI", "Pseudoternary", "Manchester", "Differential Manchester"
    ])

    # Update the plot based on the selected encoding type
    if encoding_type == 'NRZ-L':
        signal = nrz_l(bit_string)
        title = 'NRZ-L'
    elif encoding_type == 'NRZ-I':
        signal = nrz_i(bit_string)
        title = 'NRZ-I'
    elif encoding_type == 'Bipolar AMI':
        signal = bipolar_ami(bit_string)
        title = 'Bipolar AMI'
    elif encoding_type == 'Pseudoternary':
        signal = pseudoternary(bit_string)
        title = 'Pseudoternary'
    elif encoding_type == 'Manchester':
        signal = manchester(bit_string)
        title = 'Manchester'
    elif encoding_type == 'Differential Manchester':
        signal = diff_manchester(bit_string)
        title = 'Differential Manchester'

    # Plot the signal and display it in Streamlit
    fig = plot_signal(bit_string, signal, title)

    # Display the plot
    st.pyplot(fig)

