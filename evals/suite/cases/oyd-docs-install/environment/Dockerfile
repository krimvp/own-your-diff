FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends git python3 ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
COPY . /fixture/
RUN bash /fixture/build-repo.sh && rm -rf /fixture
WORKDIR /workspace
