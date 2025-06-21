###############################################################################
# Software3-Lab — Dockerfile
# ---------------------------------------------------------------------------
# Stage 1 (builder):  Rust + gcc to compile tokenizer wheel & C++ lib
# Stage 2 (runtime): Python 3.11 slim + minimal binaries
###############################################################################

###########################  Stage 1 : builder  ###############################
FROM rust:1.78-slim AS builder

WORKDIR /build

# ------------------ system deps for Python & C++ ----------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev python3-pip \
        openjdk-17-jre-headless \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------ build Rust tokenizer wheel ------------------------------
COPY rust/tokenizer ./tokenizer
RUN pip install maturin==1.5.1 && \
    cd tokenizer && \
    maturin build --release --interpreter python3 && \
    cd ..

# ------------------ compile C++ vector library ------------------------------
COPY cpp/vector_math.cpp ./vector_math.cpp
RUN g++ -O3 -shared -std=c++17 -fPIC vector_math.cpp -o libvector.so

# ------------------ copy project source for later ---------------------------
COPY . /src

###########################  Stage 2 : runtime  ###############################
FROM python:3.11-slim AS runtime

LABEL maintainer="Corey Leath <coreyleath10@gmail.com>"

WORKDIR /app

# ---------- copy wheel & C++ lib from builder stage -------------------------
COPY --from=builder /build/tokenizer/target/wheels/*.whl /tmp/
COPY --from=builder /build/libvector.so /usr/local/lib/libvector.so

# ---------- install Python deps (requirements first for cache) -------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir /tmp/*.whl

# ---------- copy application code ------------------------------------------
COPY app/       app/
COPY pipelines/ pipelines/
COPY prompts/   prompts/
COPY docs/      docs/

ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

EXPOSE 8080
CMD ["uvicorn", "pipelines.evaluate:app", "--host", "0.0.0.0", "--port", "8080"]
