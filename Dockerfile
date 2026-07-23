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
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Configura o noVNC para abrir automaticamente no carregamento da pagina
RUN cp /usr/share/novnc/vnc_auto.html /usr/share/novnc/index.html

WORKDIR /app

# Copia os arquivos da aplicação e do supervisor
COPY Planner.py /app/planner.py
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 10000

# Inicializa o supervisor como processo principal do container
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
