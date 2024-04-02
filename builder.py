import os
import PyInstaller.__main__

def build_exe(input_script, output_dir):
    PyInstaller.__main__.run([
        '--onefile',
        '--windowed',
        '--noconsole',  # Place --noconsole before the input script
        input_script,
        '-p', f'{os.path.dirname(input_script)}',
        '--distpath', output_dir  # Specify the output directory using --distpath
    ])
    
if __name__ == "__main__":
    main_script = "Main.py"  
    output_directory = "dist" 
    build_exe(main_script, output_directory)
