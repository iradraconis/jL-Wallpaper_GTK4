import subprocess
import importlib

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"Das Modul '{module_name}' ist bereits installiert.")
    except ImportError:
        print(f"Das Modul '{module_name}' ist nicht installiert.")
        user_input = input(f"Möchten Sie das Modul '{module_name}' installieren? (j/n): ")
        if user_input.lower() == 'j':
            subprocess.check_call(["python", "-m", "pip", "install", module_name])
            print(f"Das Modul '{module_name}' wurde erfolgreich installiert.")
        else:
            print("Installation abgebrochen.")

