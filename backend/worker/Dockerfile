FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libcairo2 libglib2.0-0 \
    gcc g++ make pkg-config libcairo2-dev libpango1.0-dev \
    texlive-latex-base texlive-latex-recommended texlive-fonts-recommended \
    texlive-latex-extra texlive-science \
    dvipng dvisvgm                              \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir manim

RUN useradd -m runner
USER runner
WORKDIR /sandbox


ENTRYPOINT ["manim"]
