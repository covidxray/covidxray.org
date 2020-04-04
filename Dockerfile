FROM archlinux
WORKDIR /covid
ENV FLASK_APP app.py 
ENV FLASK_RUN_HOST  0.0.0.0
RUN pacman -Syu --noconfirm
RUN pacman -S python3 python-pip cmake gcc linux-headers --noconfirm
RUN python3 -m venv v 
RUN source v/bin/activate
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3","app.py"]
