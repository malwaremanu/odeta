#!/bin/bash

# 01J3SVPPGXFAXTZATSQD5F7Z1C
# -AgEIcHlwaS5vcmcCJGE5ZDkxNDUzLWYzZWMtNDdlMy1hOGM3LTNhZjNlNjc1N2EzMgACDVsxLFsib2RldGEiXV0AAixbMixbImVhODQyMzIzLTIwZWEtNGU5OS1iMzExLTI0ZDcxMDI3NDAyYSJdXQAABiDqSrKlJd7auHnVYevz384RDRCqOUIYNaKn5zy86qm1ig

rm -rf build
rm -rf dist

python3 ./increment_version.py

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
