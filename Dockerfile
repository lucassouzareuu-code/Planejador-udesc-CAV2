FROM kasmweb/desktop:1.14.0

USER root

# Instala Python e Tkinter no ambiente Kasm
RUN apt-get update && apt-get install -y \
    python3 \
    python3-tk \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Planner.py /app/planner.py

# Inicia o Tkinter no boot da interface
RUN echo "python3 /app/planner.py &" >> /dockerstartup/custom_startup.sh
RUN chmod +x /dockerstartup/custom_startup.sh

EXPOSE 6901

CMD ["/dockerstartup/kasm_defaultscript.sh"]
