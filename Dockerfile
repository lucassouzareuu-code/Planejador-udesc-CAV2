FROM kasmweb/desktop:1.14.0

USER root

# Instala Python e Tkinter
RUN apt-get update && apt-get install -y \
    python3 \
    python3-tk \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Planner.py /app/planner.py

# Inicia o programa Tkinter junto com a sessão KasmVNC
RUN echo "python3 /app/planner.py &" >> /dockerstartup/custom_startup.sh
RUN chmod +x /dockerstartup/custom_startup.sh

EXPOSE 6901

CMD ["/dockerstartup/kasm_default_script.sh"]
