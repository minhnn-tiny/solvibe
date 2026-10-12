#!/bin/sh
# Run a command inside the pilot tools image with a project folder mounted at /work.
#   dock.sh [--net] <host_dir> <command...>
# Without --net the container has no network at all (use this for every PoV and evaluation run).
# With --net it uses the normal Docker network (only for one-off setup: installing dependencies, downloading solc).
# The solc cache lives in the named volume solvibe-svm so offline builds can find compilers.
set -e
NET="--network none"
if [ "$1" = "--net" ]; then NET=""; shift; fi
DIR=$(cd "$1" && pwd); shift
exec docker run --rm $NET -v "$DIR":/work -v solvibe-svm:/root/.svm -w /work \
  -e FOUNDRY_DISABLE_NIGHTLY_WARNING=1 --memory 6g solvibe-tools:1 sh -c "$*"
