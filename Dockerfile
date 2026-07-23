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

# Cria o atalho para carregar direto na pagina do VNC
RUN cp /usr/share/novnc/vnc.html /usr/share/novnc/index.html

WORKDIR /app
COPY Planner.py /app/planner.py

EXPOSE 10000

# Adicionado retardo (sleep 2) para o servidor Xvfb e x11vnc ficarem 100% prontos antes do websockify
CMD ["sh", "-c", "Xvfb :99 -screen 0 1280x800x16 & sleep 1 && export DISPLAY=:99 && fluxbox & python3 /app/planner.py & x11vnc -display :99 -forever -nopw -listen localhost -port 5900 & sleep 2 && websockify --web /usr/share/novnc 10000 localhost:5900"]
