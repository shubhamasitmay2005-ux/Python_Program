import serial
import time
import tkinter as tk

# ---- Serial setup ----
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)

# ---- GUI setup ----
root = tk.Tk()
root.title("Smart AC Controller")
root.geometry("400x250")
root.config(bg="#2c3e50")  # dark background

temperature_var = tk.StringVar(value="Temperature: -- °C")
status_var = tk.StringVar(value="AC Status: OFF")

ac_manual_state = False  # manual override

def read_temperature():
    global ac_manual_state

    line = ser.readline().decode("utf-8").strip()

    if line:
        try:
            temp = int(line)
            temperature_var.set(f"Temperature: {temp} °C")

            # Color feedback based on temperature
            if temp > 24:
                temp_label.config(fg="red")
                if not ac_manual_state:
                    status_var.set("AC Status: ON (Auto)")
            else:
                temp_label.config(fg="lightgreen")
                if not ac_manual_state:
                    status_var.set("AC Status: OFF (Auto)")

        except ValueError:
            pass

    root.after(1000, read_temperature)

def toggle_ac():
    global ac_manual_state
    ac_manual_state = not ac_manual_state

    if ac_manual_state:
        if "OFF" in status_var.get():
            status_var.set("AC Status: ON (Manual)")
            status_label.config(fg="orange")
        else:
            status_var.set("AC Status: OFF (Manual)")
            status_label.config(fg="gray")
    else:
        status_label.config(fg="white")

# ---- Widgets ----
title_label = tk.Label(root, text="🌡 Smart AC Controller", font=("Arial", 18, "bold"),
                       bg="#2c3e50", fg="white")
title_label.pack(pady=10)

temp_label = tk.Label(root, textvariable=temperature_var, font=("Arial", 16, "bold"),
                      bg="#2c3e50", fg="lightgreen")
temp_label.pack(pady=10)

status_label = tk.Label(root, textvariable=status_var, font=("Arial", 16, "bold"),
                        bg="#2c3e50", fg="white")
status_label.pack(pady=10)

toggle_button = tk.Button(root, text="ON / OFF", font=("Arial", 14, "bold"),
                          bg="#3498db", fg="white", width=12, command=toggle_ac)
toggle_button.pack(pady=15)

# ---- Start reading loop ----
read_temperature()

root.mainloop()
