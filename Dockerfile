FROM archlinux
WORKDIR /covid
ENV FLASK_APP run.py 
ENV FLASK_RUN_HOST  0.0.0.0
RUN pacman -Syu --noconfirm
RUN pacman -S python3 python-pip cmake gcc python-virtualenv python-distlib linux-headers --noconfirm
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
RUN export FLASK_APP=run.py 
CMD ["flask","run --host=0.0.0.0 --port=5000"]
