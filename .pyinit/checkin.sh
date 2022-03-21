dir=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

shopt -s expand_aliases
alias run="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)/run.sh"
alias build="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)/build.sh"
alias install="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)/install.sh"
alias uninstall="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)/uninstall.sh"

p="$PS1"

alias checkout="source $dir/checkout.sh; PS1='$p'"
export PS1="(pyproj $(basename $(dirname $dir))) ${PS1}"

echo "Checked in"
