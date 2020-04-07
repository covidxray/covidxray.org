FROM archlinux
WORKDIR /covid
ENV FLASK_APP app.py 
ENV FLASK_RUN_HOST  0.0.0.0
RUN pacman -Syu --noconfirm
RUN pacman -S python3 python-pip cmake gcc python-virtualenv python-distlib linux-headers --noconfirm
RUN virtualenv covid-19 
RUN source covid-19/bin/activate
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
COPY . .
CMD ["flask","run --host=0.0.0.0 --port=5000"]
