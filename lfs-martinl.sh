# switch to local lfs backend
git config -f .lfsconfig lfs.url https://gitlab.com/martinlillepuu/openpilot-lfs.git/info/lfs
git config -f .lfsconfig lfs.pushurl ssh://git@gitlab.com/martinlillepuu/openpilot-lfs.git
git lfs update
