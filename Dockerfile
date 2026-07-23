FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-tk \
    python3-pip \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

RUN cp /usr/share/novnc/vnc_auto.html /usr/share/novnc/index.html

WORKDIR /app
COPY Planner.py /app/planner.py

EXPOSE 10000

# websockify agora fica em primeiro plano no final (sem o &) para manter o servidor aberto
CMD ["sh", "-c", "Xvfb :99 -screen 0 1280x800x16 & sleep 1 && export DISPLAY=:99 && fluxbox & sleep 1 && python3 /app/planner.py & sleep 1 && x11vnc -display :99 -forever -shared -nopw -listen 127.0.0.1 -port 5900 & websockify --web /usr/share/novnc 10000 127.0.0.1:5900"]
