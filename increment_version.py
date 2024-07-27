import re

# Define the version file
VERSION_FILE = "version.py"

# Read the current version
with open(VERSION_FILE, "r") as file:
    content = file.read()

# Extract the current version using a regular expression
version_match = re.search(r'__version__ = "([^"]+)"', content)
if version_match:
    current_version = version_match.group(1)
    # Split the version into its components
    major, minor, patch = map(int, current_version.split('.'))

    # Increment the patch version
    patch += 1

    # Form the new version
    new_version = f"{major}.{minor}.{patch}"

    # Update the version in the content
    new_content = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', content)

    # Write the updated content back to the file
    with open(VERSION_FILE, "w") as file:
        file.write(new_content)

    print(f"Version updated to {new_version}")
else:
    print("Version string not found in the file.")
