import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import configData
import configUI
import model 

# Create the main window
root = tk.Tk()
root.title("Energy Consumption Predictor")
root.geometry("600x800")
root.configure(bg="#f0f4f8")

# Custom styles
style = ttk.Style()
style.theme_use("clam")

# Configure custom styles
style.configure("TButton", 
                font=("Helvetica", 14, "bold"), 
                background="#007acc", 
                foreground="white", 
                padding=10)
style.map("TButton", background=[('active', '#005c99')])

style.configure("TEntry", 
                font=("Helvetica", 12), 
                padding=5)

style.configure("TCombobox", 
                font=("Helvetica", 12), 
                padding=5)

# Fonts
title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
label_font = tkfont.Font(family="Helvetica", size=12)
entry_font = tkfont.Font(family="Helvetica", size=12)
checkbox_font = tkfont.Font(family="Helvetica", size=11)

# Main Frame
main_frame = tk.Frame(root, bg=configUI.bg_color, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# Title
title_label = tk.Label(main_frame, text="Energy Consumption Predictor", font=title_font, bg=configUI.bg_color, fg="#2c3e50")
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Left Column
left_frame = tk.Frame(main_frame, bg=configUI.section_bg, padx=15, pady=15, relief="ridge", bd=2)
left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

# Right Column
right_frame = tk.Frame(main_frame, bg=configUI.section_bg, padx=15, pady=15, relief="ridge", bd=2)
right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

def validate_float(action, value_if_allowed):
    if action == '1':  # insert
        if value_if_allowed in ["", "-"]:
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    return True

def validate_float_non_negative(action, value_if_allowed):
    if action == '1':  # insert
        if value_if_allowed == "":
            return True
        try:
            value = float(value_if_allowed)
            return value >= 0
        except ValueError:
            return False
    return True

# Function to create labeled input
def create_labeled_input(parent, label_text, input_type, values=None, row=None, allow_negative=False):
    label = tk.Label(parent, text=label_text, font=label_font, bg=configUI.section_bg, anchor="w")
    label.grid(row=row, column=0, sticky="w", pady=(10, 5))
    
    if input_type == "entry":
        if allow_negative:
            vcmd = (parent.register(validate_float), '%d', '%P')
        else:
            vcmd = (parent.register(validate_float_non_negative), '%d', '%P')
        widget = ttk.Entry(parent, validate="key", validatecommand=vcmd)
        widget.insert(0, "0")  # Set default value to 0
    elif input_type == "combobox":
        widget = ttk.Combobox(parent, values=list(values.keys()), state="readonly")
        widget.set(list(values.keys())[0])  # Set default value
    
    widget.grid(row=row+1, column=0, sticky="ew", pady=(0, 10))
    return widget

# Left Column Inputs
car_entry = create_labeled_input(left_frame, "Car Model:", "combobox", values=configData.car_type, row=0)
quantity_entry = create_labeled_input(left_frame, "Quantity (kWh):", "entry", row=2)
avg_speed_entry = create_labeled_input(left_frame, "Average Speed (km/h):", "entry", row=4)
encoded_driving_style = create_labeled_input(left_frame, "Driving Style:", "combobox", values=configData.driving_styles, row=6)
encoded_tire_type = create_labeled_input(left_frame, "Tire Type:", "combobox", values=configData.tire_types, row=8)
ecr_deviation = create_labeled_input(left_frame, "ECR Dev Type:", "entry", row=10, allow_negative=True)

# Checkboxes with tooltips (Right Column)
def create_checkbox_with_tooltip(parent, text, row, tooltip_text):
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(parent, text=text, variable=var, font=checkbox_font, bg=configUI.section_bg, 
                              activebackground=configUI.section_bg, padx=5, pady=5)
    checkbox.grid(row=row, column=0, sticky="w", pady=5)
    
    def show_tooltip(event):
        tooltip = tk.Toplevel(parent)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(tooltip, text=tooltip_text, justify='left', background="#ffffd0", 
                         relief="solid", borderwidth=1, font=("Helvetica", 10))
        label.pack(ipadx=5, ipady=5)
        
        def hide_tooltip(event):
            tooltip.destroy()
        
        checkbox.bind("<Leave>", hide_tooltip)
        tooltip.bind("<Leave>", hide_tooltip)
    
    checkbox.bind("<Enter>", show_tooltip)
    return var

model_selection = create_labeled_input(right_frame, "Model Using for predict:", "combobox", values=configData.model_type, row=0)
city_var = create_checkbox_with_tooltip(right_frame, "City", 2, "Indicates if the trip is in an urban environment")
motor_way_var = create_checkbox_with_tooltip(right_frame, "Motorway", 3, "Indicates if the trip includes highway driving")
country_roads_var = create_checkbox_with_tooltip(right_frame, "Country Roads", 4, "Indicates if the trip includes rural road driving")
ac_var = create_checkbox_with_tooltip(right_frame, "A/C", 5, "Indicates if the air conditioning is in use")
park_heating_var = create_checkbox_with_tooltip(right_frame, "Park Heating", 6, "Indicates if park heating is activated")

# Predict Button
def predict():
    # Get the numeric values for the combobox selections
    car_entry_value = configData.car_type[car_entry.get()]
    quantity_entry_value = float(quantity_entry.get() or 0)
    avg_speed_entry_value = float(avg_speed_entry.get() or 0)
    ecr_deviation_value = float(ecr_deviation.get() or 0)
    model_type_value = configData.model_type[model_selection.get()]
    driving_style_value = configData.driving_styles[encoded_driving_style.get()]
    tire_type_value = configData.tire_types[encoded_tire_type.get()]
    city_value = city_var.get()
    motor_way_value = motor_way_var.get()
    country_roads_value = country_roads_var.get()
    ac_value = ac_var.get()
    park_heating_value = park_heating_var.get()

    data_input = {
        'model': model_type_value,
        'car': car_entry_value,
        'quantity(kWh)': quantity_entry_value,
        'city': city_value, 
        'motor_way': motor_way_value,
        'country_roads': country_roads_value, 
        'A/C': ac_value, 
        'park_heating':  park_heating_value, 
        'avg_speed(km/h)': avg_speed_entry_value,
        'encoded_driving_style': driving_style_value, 
        'encoded_tire_type': tire_type_value, 
        'ecr_dev_type': ecr_deviation_value
    }
    
    # Here you would use these values in your prediction logic
    model_handler = model.MainModel()
    result = model_handler.predict(data_input)

    # Update the trip distance (this is just a placeholder)
    trip_distance_value.config(text="{0} km".format(result))

predict_button = ttk.Button(main_frame, text="Predict", command=predict)
predict_button.grid(row=2, column=0, columnspan=2, pady=20)

# Trip Distance (Highlighted output)
trip_distance_frame = tk.Frame(main_frame, bg=configUI.highlight_bg, padx=10, pady=10, relief="ridge", bd=2)
trip_distance_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

trip_distance_label = tk.Label(trip_distance_frame, text="Trip Distance:", font=label_font, bg=configUI.highlight_bg)
trip_distance_label.pack(side="left")

trip_distance_value = tk.Label(trip_distance_frame, text="150 km", font=label_font, bg=configUI.highlight_bg, fg=configUI.highlight_fg)
trip_distance_value.pack(side="left")

# Run the application
root.mainloop()