FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-tk \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Planner.py /app/planner.py

EXPOSE 7860

CMD ["sh", "-c", "Xvfb :99 -screen 0 1280x800x16 & export DISPLAY=:99 && fluxbox & x11vnc -display :99 -forever -nopw -listen localhost -port 5900 & /usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 7860"]
