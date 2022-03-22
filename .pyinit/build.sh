name="$(basename $PWD)"
echo "Building $(cd $(dirname $(dirname "${BASH_SOURCE[0]}")) && pwd)/scripts/__main__.py"
echo "<----------BUILD---------->"
echo ""

time="$(date +%s)"

pyinstaller --noconfirm --icon "$(cd $(dirname $(dirname "${BASH_SOURCE[0]}")) && pwd)/icon.ico" --name $name "$(cd $(dirname $(dirname "${BASH_SOURCE[0]}")) && pwd)/scripts/__main__.py"

time="$(($(date +%s)-time))"

echo ""
echo "<----------BUILD---------->"
echo "Done in $time seconds"

mv "dist/$name" "$(cd $(dirname $(dirname "${BASH_SOURCE[0]}")) && pwd)/bin"
rm -rf "dist"
rm -rf "build"
rm "$name.spec"
