from rich.console import Console
from rich.table import Table
import keyboard  # For capturing keyboard events
import time
import sys
import gc

console = Console()

# File: startup_options_list.py

# Sample keybindings for demonstration
class KeyBinding:
    __slots__ = ('key', 'value', 'status')
    
    def __init__(self, key, value, status=True):
        self.key = sys.intern(key)
        self.value = sys.intern(value)
        self.status = status

# Convert keybindings to tuple of KeyBinding objects
keybindings = tuple(
    KeyBinding(key, value) for key, value in {
        sys.intern('Alt+j'): sys.intern('q'),
        sys.intern('Alt+k'): sys.intern('w'),
        sys.intern('Alt+l'): sys.intern('e')
    }.items()
)


# Function to display options
def display_options():
    console.print("[bold green]Custom Keybinder Options[/bold green]")
    console.print("1. View/Toggle Key Bindings")
    console.print("2. Add Key Binding")
    console.print("3. Delete Key Binding")
    console.print("4. Edit Key Binding")
    console.print("5. Run Key Binder")
    console.print("6. Exit Program")


# Function to view and toggle keybindings
def view_toggle_bindings():
    table = Table(title="Current Key Bindings")
    table.add_column("Key Combination", justify="center", style="cyan")
    table.add_column("Mapped To", justify="center", style="magenta")
    table.add_column("Status", justify="center", style="green")

    for binding in keybindings:
        status = "ON" if binding.status else "OFF"
        table.add_row(binding.key, binding.value, status)

    console.print(table)

    key_to_toggle = input(
        "Enter the key combination to toggle or press Enter to go back: "
    )
    for binding in keybindings:
        if binding.key == key_to_toggle:
            binding.status = not binding.status
            console.print(
                f"[bold green]{key_to_toggle} toggled to {'ON' if binding.status else 'OFF'}[/bold green]"
            )
            break


# Function to add keybinding
def add_binding():
    global keybindings
    key_combination = input("Enter the new key combination: ")
    mapped_to = input("Enter the key to map to: ")
    for binding in keybindings:
        if binding.key == key_combination:
            console.print("[bold red]Key combination already exists.[/bold red]")
            return
    keybindings += (KeyBinding(key_combination, mapped_to),)
    console.print(
        f"[bold green]Added binding: {key_combination} -> {mapped_to}[/bold green]"
    )


def delete_binding():
    global keybindings
    console.print("[bold yellow]Current Key Bindings:[/bold yellow]")
    for index, binding in enumerate(keybindings, start=1):
        status = "ON" if binding.status else "OFF"
        console.print(f"{index}. {binding.key} -> {binding.value} [{status}]")

    binding_number = input(
        "Enter the number of the key binding to delete or press Enter to go back: "
    )
    if binding_number.isdigit() and 1 <= int(binding_number) <= len(keybindings):
        key_to_delete = keybindings[int(binding_number) - 1].key
        keybindings = tuple(binding for binding in keybindings if binding.key != key_to_delete)
        console.print(f"[bold green]Deleted binding: {key_to_delete}[/bold green]")
    else:
        console.print("[bold red]Invalid input. No binding deleted.[/bold red]")


# edit function
def edit_binding():
    console.print("[bold yellow]Current Key Bindings:[/bold yellow]")
    for index, binding in enumerate(keybindings, start=1):
        status = "ON" if binding.status else "OFF"
        console.print(f"{index}. {binding.key} -> {binding.value} [{status}]")

    binding_number = input(
        "Enter the number of the key binding to edit or press Enter to go back: "
    )
    if binding_number.isdigit() and 1 <= int(binding_number) <= len(keybindings):
        binding_to_edit = keybindings[int(binding_number) - 1]
        new_mapped_to = input(
            f"Enter new value for {binding_to_edit.key} (current: {binding_to_edit.value}): "
        )
        binding_to_edit.value = new_mapped_to
        console.print(
            f"[bold green]Updated binding: {binding_to_edit.key} -> {new_mapped_to}[/bold green]"
        )
    else:
        console.print("[bold red]Invalid input. No binding edited.[/bold red]")


# Function to run key binder
def run_keybinder():
    console.print(
        "[bold yellow]Running Key Binder. Press Ctrl+C to stop.[/bold yellow]"
    )
    
    # Dictionary to track last press time for debouncing
    last_press = {binding.key: 0 for binding in keybindings}
    DEBOUNCE_TIME = 0.1  # 100ms debounce time

    try:
        while True:
            current_time = time.time()
            for binding in keybindings:
                if binding.status and keyboard.is_pressed(binding.key) and \
                   current_time - last_press[binding.key] > DEBOUNCE_TIME:
                    keyboard.write(binding.value)
                    last_press[binding.key] = current_time
            time.sleep(0.01)  # Reduce CPU usage
    except KeyboardInterrupt:
        console.print("[bold red]\nKey Binder stopped.[/bold red]")


# Function to handle user choice
def handle_choice(choice):
    if choice == "1":
        view_toggle_bindings()
    elif choice == "2":
        add_binding()
    elif choice == "3":
        console.print("[bold yellow]Delete Key Binding[/bold yellow]")
        # Add logic for deleting key binding
        delete_binding()
    elif choice == "4":
        console.print("[bold yellow]Edit Key Binding[/bold yellow]")
        # Add logic for editing key binding
        edit_binding()
    elif choice == "5":
        run_keybinder()
    elif choice == "6":
        console.print("[bold red]Exiting Program[/bold red]")
        exit()
    else:
        console.print("[bold red]Invalid Option. Please choose again.[/bold red]")


# Main loop
if __name__ == "__main__":
    while True:
        display_options()
        user_choice = input("Enter your choice: ")
        handle_choice(user_choice)
        if user_choice == "6":
            break
