# #!/bin/bash
# # pypi-AgEIcHlwaS5vcmcCJGJmNTU1ZTYwLWY2NjUtNGI5NS05OGYyLWEwNmFmMGE0ZTdkYgACKlszLCIyNjBmZTU0Yi00NmViLTQ2NGYtOTk5NS01YjMyZDIyNTQ0YjYiXQAABiCCLRsCtsrMNrnNhC77EMuFm124XviseV5sJd0hknqOswm
# rm -rf dist
# rm -rf build

# # Build the distribution
# python3 setup.py sdist bdist_wheel

# # Upload the distribution
# twine upload dist/* --verbose

#!/bin/bash

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
twine upload dist/*

# Commit the version change
# git add version.py
# git commit -m "Bump version to $new_version"
# git push origin main
