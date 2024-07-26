ARG PY_VER=3.12.1
ARG BASE=${BASE:-python:${PY_VER}}
FROM $BASE
WORKDIR /app
ADD *.rst LICENSE MANIFEST.in *.txt *.cfg  *.py *.ini ./
ADD requirements/ ./requirements/
RUN mkdir src/ && touch src/__init__.py
RUN apt update && apt install -y python3-dev libpython3-dev
RUN <<EOF
if ! ( python --version );then
    ln -s /usr/bin/python3 /usr/bin/python
fi
if ! ( pip --version );then
wget https://bootstrap.pypa.io/get-pip.py
chmod +x get-pip.py
./get-pip.py --break-system-packages
fi
EOF
RUN pip install --break-system-packages -r req*/base.txt
RUN if ( ! cargo --version );then apt update && apt install -y cargo;fi
ENV CFLAGS="-I/usr/include/python3.12/"
RUN pip install --break-system-packages -r req*/test.txt
RUN pip install --break-system-packages -r req*/release.txt
RUN pip install --break-system-packages tox-direct
ADD *.rst LICENSE MANIFEST.in *.txt *.sh *.cfg  *.py *.ini ./
ADD src/ src/
ENTRYPOINT /app/docker-entry.sh
