source $(cd $(dirname $(dirname "${BASH_SOURCE[0]}")) && pwd)/.venv/bin/activate
python3 -m pip uninstall $1
deactivate
