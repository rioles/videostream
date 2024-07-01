FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app
RUN pip install MarkupSafe
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY . .
RUN chmod +x clean_setup_tool_packages.sh
RUN chmod +x install_setup_tool.sh
RUN /home/app/clean_setup_tool_packages.sh
RUN python setup.py install
EXPOSE 5000
CMD ["python", "/home/app/api/v1/app.py"]




