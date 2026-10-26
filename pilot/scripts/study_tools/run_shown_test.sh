#!/bin/sh
# Shared test script of the repair input study, for level E1 ("can rerun only the shown test").
# All three agents rerun the shown test through this script, so they run the same command and see
# the same output: Aider as its --test-cmd, OpenHands and Codex through the MCP tool run_shown_test.
#
# It first copies the original test files back from the read-only folder /opt/study_kept, so an
# agent that edits the shown test or a file it inherits cannot change what runs. forge then reads
# the kept foundry.toml, not the workspace's, and ffi stays off, so neither an edited foundry.toml
# nor a vm.ffi call can run a command. The command itself is read from the kept folder.
cd "${STUDY_PROJECT:-/work}" || exit 2
cp -R /opt/study_kept/test/. test/ || exit 2
export FOUNDRY_CONFIG=/opt/study_kept/foundry.toml FOUNDRY_FFI=false FOUNDRY_SHOW_PROGRESS=false
exec sh -c "$(cat /opt/study_kept/test_cmd) --root ."
