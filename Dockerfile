FROM ubuntu:noble

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install python3-xyz && \
    # Clean up apt cache to reduce image size
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
# Use pip3 or python3 -m pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
COPY . .


CMD ["python", "app.py"]