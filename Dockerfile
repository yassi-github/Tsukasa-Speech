FROM nvidia/cuda:12.6.0-devel-ubuntu22.04

WORKDIR /app

RUN groupadd --gid 1000 user && useradd --gid user --shell /bin/bash --uid 1000 -m user && apt-get update && apt-get install -y curl ca-certificates git git-lfs build-essential

COPY --chown=user:user . .
RUN chown user:user /app

USER user
# install python from uv, because apt repository still provides rc version (and not work)
ENV PATH="${PATH}:/home/user/.local/bin"
RUN bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh' && uv python install 3.11 && uv python pin 3.11
RUN uv sync
CMD ["uv", "run", "app_tsuka.py"]
