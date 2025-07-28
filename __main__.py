import os
import runpy

def main():
    current_dir = os.path.dirname(__file__)
    script = os.path.join(current_dir, "OK workspaces", "main.py")
    runpy.run_path(script, run_name="__main__")

if __name__ == "__main__":
    main()
