from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt
from rich.text import Text
import keyboard
import time
import sys
import os
from typing import NamedTuple, List
from collections import defaultdict

console = Console()

# Improved class with proper typing
class KeyBinding(NamedTuple):
    key: str
    value: str
    status: bool = True
# Global state management
class KeyBinderState:
    def __init__(self):
        self.bindings: List[KeyBinding] = []
        self.load_default_bindings()
        
    def load_default_bindings(self):
        defaults = {
            'Alt+j': 'q',
            'Alt+k': 'w',
            'Alt+l': 'e'
        }
        self.bindings = [KeyBinding(sys.intern(k), sys.intern(v)) for k, v in defaults.items()]
    
    def add_binding(self, key: str, value: str) -> bool:
        if any(b.key == key for b in self.bindings):
            return False
        self.bindings.append(KeyBinding(sys.intern(key), sys.intern(value)))
        return True
    
    def delete_binding(self, index: int) -> bool:
        if 0 <= index < len(self.bindings):
            self.bindings.pop(index)
            return True
        return False
    
    def edit_binding(self, index: int, new_value: str) -> bool:
        if 0 <= index < len(self.bindings):
            binding = self.bindings[index]
            self.bindings[index] = KeyBinding(binding.key, sys.intern(new_value), binding.status)
            return True
        return False
    
    def toggle_binding(self, index: int) -> bool:
        if 0 <= index < len(self.bindings):
            binding = self.bindings[index]
            self.bindings[index] = KeyBinding(binding.key, binding.value, not binding.status)
            return True
        return False

# Initialize state
state = KeyBinderState()

# UI components
def create_header(title: str) -> Panel:
    return Panel(
        Text(title, style="bold blue", justify="center"),
        border_style="bright_blue"
    )

def create_bindings_table() -> Table:
    table = Table(
        show_header=True, 
        header_style="bold cyan", 
        box=None,
        title="Current Key Bindings",
        title_style="bold magenta",
        expand=True
    )
    
    table.add_column("#", justify="right", style="dim")
    table.add_column("Key Combination", justify="center", style="cyan")
    table.add_column("Mapped To", justify="center", style="magenta")
    table.add_column("Status", justify="center")
    
    for i, binding in enumerate(state.bindings):
        status_style = "green bold" if binding.status else "red"
        status_text = "ACTIVE" if binding.status else "DISABLED"
        table.add_row(
            str(i+1),
            binding.key,
            binding.value,
            f"[{status_style}]{status_text}[/{status_style}]"
        )
    
    return table

# Menu actions
def display_menu():
    # More thorough console clearing
    console.clear()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Create layout for menu
    layout = Layout()
    layout.split_column(
        Layout(create_header("🚀 KeyBinder Pro"), size=3),
        Layout(name="content"),
        Layout(Panel("[bold green]Options:[/bold green]\n"
                     "1. [cyan]View/Toggle[/cyan] Key Bindings\n"
                     "2. [cyan]Add[/cyan] Key Binding\n"
                     "3. [cyan]Delete[/cyan] Key Binding\n"
                     "4. [cyan]Edit[/cyan] Key Binding\n"
                     "5. [cyan]Run[/cyan] Key Binder\n"
                     "6. [red]Exit[/red] Program", 
                     border_style="green"), size=10)
    )
    
    content_layout = Layout()
    content_layout.split_row(
        Layout(create_bindings_table()),
    )
    layout["content"].update(content_layout)
    
    # Print layout to console
    console.print(layout)
    return Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"])

def view_toggle_bindings():
    console.clear()
    console.print(create_header("Toggle Key Bindings"))
    console.print(create_bindings_table())
    
    choice = Prompt.ask(
        "Enter binding number to toggle (or press Enter to go back)",
        default=""
    )
    
    if choice.isdigit():
        index = int(choice) - 1
        if state.toggle_binding(index):
            binding = state.bindings[index]
            status = "ACTIVATED" if binding.status else "DISABLED"
            console.print(f"[bold green]{binding.key} {status}[/bold green]")
        else:
            console.print("[bold red]Invalid binding number[/bold red]")
    
    console.print("\nPress Enter to continue...")
    input()

def add_binding():
    console.clear()
    console.print(create_header("Add New Key Binding"))
    
    key = Prompt.ask("Enter key combination (e.g. 'Alt+x')")
    value = Prompt.ask("Enter key to map to")
    
    if state.add_binding(key, value):
        console.print(f"[bold green]Added: {key} → {value}[/bold green]")
    else:
        console.print(f"[bold red]Error: Key combination '{key}' already exists[/bold red]")
    
    console.print("\nPress Enter to continue...")
    input()

def delete_binding():
    console.clear()
    console.print(create_header("Delete Key Binding"))
    console.print(create_bindings_table())
    
    choice = Prompt.ask(
        "Enter binding number to delete (or press Enter to go back)",
        default=""
    )
    
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(state.bindings):
            binding = state.bindings[index]
            if state.delete_binding(index):
                console.print(f"[bold green]Deleted: {binding.key} → {binding.value}[/bold green]")
        else:
            console.print("[bold red]Invalid binding number[/bold red]")
    
    console.print("\nPress Enter to continue...")
    input()

def edit_binding():
    console.clear()
    console.print(create_header("Edit Key Binding"))
    console.print(create_bindings_table())
    
    choice = Prompt.ask(
        "Enter binding number to edit (or press Enter to go back)",
        default=""
    )
    
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(state.bindings):
            binding = state.bindings[index]
            new_value = Prompt.ask(f"Enter new value for '{binding.key}'", default=binding.value)
            
            if state.edit_binding(index, new_value):
                console.print(f"[bold green]Updated: {binding.key} → {new_value}[/bold green]")
        else:
            console.print("[bold red]Invalid binding number[/bold red]")
    
    console.print("\nPress Enter to continue...")
    input()

def run_keybinder():
    # More thorough console clearing
    console.clear()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print(create_header("KeyBinder Running"))
    
    # Create a status display
    active_bindings = [b for b in state.bindings if b.status]
    table = Table(show_header=True, header_style="bold green", box=None, expand=True)
    table.add_column("Active Bindings", justify="center", style="cyan")
    table.add_column("Mapped To", justify="center", style="magenta")
    
    for binding in active_bindings:
        table.add_row(binding.key, binding.value)
    
    console.print(table)
    console.print("[bold yellow]Press Ctrl+C to stop the keybinder[/bold yellow]")
    
    # Create optimized lookup dictionary for faster checking
    active_binding_dict = {b.key: b.value for b in active_bindings}
    last_press = defaultdict(lambda: 0)
    DEBOUNCE_TIME = 0.1
    
    try:
        with console.status("[bold green]Monitoring key presses...", spinner="dots") as status:
            while True:
                current_time = time.time()
                for key, value in active_binding_dict.items():
                    if keyboard.is_pressed(key) and current_time - last_press[key] > DEBOUNCE_TIME:
                        keyboard.write(value)
                        last_press[key] = current_time
                        status.update(f"[bold cyan]Pressed: {key} → {value}")
                time.sleep(0.01)
    except KeyboardInterrupt:
        console.print("[bold red]\nKeyBinder stopped[/bold red]")
        console.print("\nPress Enter to continue...")
        input()

# Action handler
def handle_choice(choice):
    actions = {
        "1": view_toggle_bindings,
        "2": add_binding,
        "3": delete_binding,
        "4": edit_binding,
        "5": lambda: (console.clear(), run_keybinder()),
        "6": lambda: sys.exit(0)
    }
    
    if choice in actions:
        actions[choice]()
    else:
        console.print("[bold red]Invalid choice[/bold red]")
        time.sleep(1)

# Main loop
if __name__ == "__main__":
    while True:
        # More thorough console clearing
        console.clear()
        os.system('cls' if os.name == 'nt' else 'clear')
        
        choice = display_menu()
        handle_choice(choice)