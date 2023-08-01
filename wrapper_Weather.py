import subprocess
import os

def run_script(script_name):
    try:
        subprocess.run(['python3', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
        exit(1)

if __name__ == "__main__":
    # Set the working directory to the location of your Python scripts
    script_directory = '/Users/gregsinnett/GitHub/Altaussee/'
    os.chdir(script_directory)

    script1 = 'Read_Weather.py'
    script2 = 'plot_Weather.py'

    run_script(script1)
    run_script(script2)

    print("Both reading and plotting scripts have been executed.")
