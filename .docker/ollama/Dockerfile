# preload models - https://github.com/ollama/ollama/issues/7046#issuecomment-2383792234

FROM ollama/ollama:0.5.7
ARG MODELS="granite3-moe:1b"
ENV OLLAMA_KEEP_ALIVE=24h
RUN ollama serve & server=$! ; sleep 5 ; for m in $MODELS ; do ollama pull $m ; done ; kill $server
