FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2 \
    libglib2.0-0 \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-science \
    dvipng \
    && rm -rf /var/lib/apt/lists/*

RUN pip install manim==0.18.0

RUN useradd -m runner
USER runner
WORKDIR /sandbox

ENTRYPOINT ["manim"]
