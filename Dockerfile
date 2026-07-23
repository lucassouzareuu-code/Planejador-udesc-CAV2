FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instala Python, Tkinter e as ferramentas de tela virtual
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

EXPOSE 10000

# Executa o display virtual (:99), o app Python no display e abre a transmissão na porta 10000
CMD ["sh", "-c", "Xvfb :99 -screen 0 1280x800x16 & sleep 1 && export DISPLAY=:99 && fluxbox & python3 /app/planner.py & x11vnc -display :99 -forever -nopw -listen localhost -port 5900 & /usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 10000"]
