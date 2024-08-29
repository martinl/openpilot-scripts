git config -f .lfsconfig lfs.url https://gitlab.com/commaai/openpilot-lfs.git/info/lfs
git config -f .lfsconfig lfs.pushurl ssh://git@gitlab.com/commaai/openpilot-lfs.git
git lfs update
git lfs fetch --all upstream
