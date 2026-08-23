FROM nvidia/cuda:12.6.0-devel-ubuntu22.04

RUN groupadd --gid 1000 user && useradd --gid user --shell /bin/bash --uid 1000 -m user && apt-get update && apt-get install -y ca-certificates git git-lfs build-essential

USER user

COPY --from=ghcr.io/astral-sh/uv:0.12-trixie-slim /usr/local/bin/uv /usr/local/bin/uvx /bin/
COPY ./entrypoint.sh /

EXPOSE 7860
ENTRYPOINT ["/entrypoint.sh"]
