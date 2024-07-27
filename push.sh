#!/bin/bash

#pypi-AgEIcHlwaS5vcmcCJDRhZTBhNDE5LWU3OGYtNDBkZi04NjQxLWEzZmRlMWNhZjA5NwACDVsxLFsib2RldGEiXV0AAixbMixbImVhODQyMzIzLTIwZWEtNGU5OS1iMzExLTI0ZDcxMDI3NDAyYSJdXQAABiDkrm1-DhaqOoJt5qQ2MUWoPFvVmqXIMPNx_-L8_d941A
rm -rf build
rm -rf dist

# Increment the version number
current_version=$(grep -oP '(?<=__version__ = ")[^"]*' version.py)
echo current_version

IFS='.' read -r -a version_parts <<< "$current_version"
patch_version=$((version_parts[2] + 1))
new_version="${version_parts[0]}.${version_parts[1]}.$patch_version"

# Update the version.py file
sed -i "s/__version__ = \"[^\"]*\"/__version__ = \"$new_version\"/" version.py

# Build the distribution
python3 setup.py sdist bdist_wheel

# Upload the distribution
twine upload dist/* --verbose

# Commit the version change
# git add version.py
# git commit -m "Bump version to $new_version"
# git push origin main
