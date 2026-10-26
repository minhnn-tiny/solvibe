# Codex CLI on top of the pilot tools image, so Aider and OpenHands keep their image unchanged.
# Codex only speaks OpenAI's Responses API. Claude models reach it through a LiteLLM proxy that
# runs inside the same container and turns each request into a call to Anthropic's Messages API.
# litellm is pinned to the version in the OpenHands environment of solvibe-tools:1.
FROM solvibe-tools:1
RUN npm install -g @openai/codex@0.160.1
RUN python -m venv /opt/litellm && /opt/litellm/bin/pip install --no-cache-dir 'litellm[proxy]==1.104.1'
