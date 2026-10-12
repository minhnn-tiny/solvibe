# One image for building projects, running PoVs and running both agents.
# Foundry is copied from the official image; Aider and OpenHands live in separate virtual environments
# so their dependencies cannot clash.
FROM ghcr.io/foundry-rs/foundry:stable AS foundry

FROM python:3.12-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl ca-certificates tmux jq ripgrep nodejs npm patch \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g yarn pnpm@9 >/dev/null 2>&1
COPY --from=foundry /usr/local/bin/forge /usr/local/bin/cast /usr/local/bin/anvil /usr/local/bin/chisel /usr/local/bin/
RUN python -m venv /opt/aider && /opt/aider/bin/pip install --no-cache-dir aider-chat==0.86.2
RUN python -m venv /opt/openhands && /opt/openhands/bin/pip install --no-cache-dir openhands-sdk==1.53.0 openhands-tools==1.53.0
RUN git config --global user.email pilot@solvibe.local && git config --global user.name pilot \
 && git config --global --add safe.directory '*'
WORKDIR /work
