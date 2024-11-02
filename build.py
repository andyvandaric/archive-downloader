import os
import sys
import platform
import PyInstaller.__main__

def build_executable(current_platform):
    """
    Build the executable file for the specified platform.

    Args:
        current_platform (str): The platform for which to build the executable.
            Can be 'windows', 'linux', or 'macos'.
    """
    # Determine the name of the executable file based on the platform
    if current_platform == 'windows':
        output_exe_name = 'archive-downloader.exe'
        script_path = os.path.join('app', 'archive_downloader.py')
    elif current_platform == 'linux':
        output_exe_name = 'archive-downloader'
        script_path = os.path.join('app', 'archive_downloader.py')
    elif current_platform == 'macos':
        output_exe_name = 'archive-downloader.app'
        script_path = os.path.join('app', 'archive_downloader.py')
    else:
        print(f"Unsupported platform: {current_platform}")
        return

    # Execute PyInstaller to create the executable
    PyInstaller.__main__.run([
        '--name={}'.format(output_exe_name),
        '--onefile',
        '--exclude-module', '__init__',  # Exclude __init__.py
        script_path,
        '--distpath=dist/{}'.format(current_platform),  # Set output to a separate folder based on platform
    ])

    print(f'Build completed: {output_exe_name} for {current_platform}')

if __name__ == "__main__":
    """
    Main entry point of the script.

    Detects the current operating system and builds the executable for that platform.
    If a platform argument is provided, it builds for the specified platform.
    """
    # Determine the current OS
    os_platform = platform.system().lower()
    
    if os_platform == 'darwin':
        os_platform = 'macos'
    elif os_platform == 'windows':
        os_platform = 'windows'
    elif os_platform == 'linux':
        os_platform = 'linux'
    else:
        print("Unsupported OS for this build script.")
        sys.exit(1)

    # If no arguments, build for the current platform
    if len(sys.argv) == 1:
        build_executable(os_platform)
    elif len(sys.argv) == 2:
        platform_arg = sys.argv[1].lower()
        if platform_arg in ['windows', 'linux', 'macos']:
            build_executable(platform_arg)
        else:
            print(f"Unsupported platform: {platform_arg}. Supported platforms: windows, linux, macos")
    else:
        print("Usage: python build.py [platform]")
        print("Platforms: windows, linux, macos")
