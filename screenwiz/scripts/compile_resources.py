import os
from pathlib import Path
import subprocess


def compile_resources(qrc_file):
    # Path to pyside6-rcc executable (adjust path as necessary)
    pyside_rcc_path = 'pyside6-rcc'

    # Output Python file name (generated output file)
    output_py_file = qrc_file.replace('.qrc', '_rc.py')

    # Command to execute pyside6-rcc
    command = [pyside_rcc_path, qrc_file, '-o', output_py_file]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"Resource file '{qrc_file}' compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling resource file '{qrc_file}':")
        print(e.stderr)
        raise


def main():
    source_dir = Path(__file__).parents[1]
    print(source_dir)

    qrc_file = str(source_dir / 'resources' / 'resources.qrc')  # Path to your .qrc file
    compile_resources(qrc_file)


if __name__ == '__main__':
    main()
