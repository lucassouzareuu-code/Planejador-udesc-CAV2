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

# Cria o atalho com autoconnect ativado
RUN cp /usr/share/novnc/vnc_auto.html /usr/share/novnc/index.html

WORKDIR /app
COPY Planner.py /app/planner.py

EXPOSE 10000

# Execução com parâmetros explícitos de IP (127.0.0.1) e permissões de conexão
CMD ["sh", "-c", "Xvfb :99 -screen 0 1280x800x16 & sleep 1 && export DISPLAY=:99 && fluxbox & python3 /app/planner.py & x11vnc -display :99 -forever -shared -nopw -listen 127.0.0.1 -port 5900 & sleep 2 && websockify --web /usr/share/novnc 10000 127.0.0.1:5900"]
