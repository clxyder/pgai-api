# preload models - https://github.com/ollama/ollama/issues/7046#issuecomment-2383792234

FROM ollama/ollama:0.5.7
ENV OLLAMA_KEEP_ALIVE=24h
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
