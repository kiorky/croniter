ARG PY_VER=3.12.1
FROM python:${PY_VER}
WORKDIR /app
ADD *.rst LICENSE MANIFEST.in *.txt *.cfg  *.py *.ini ./
ADD requirements/ ./requirements/
RUN mkdir src/ && touch src/__init__.py
RUN pip install -r req*/base.txt
RUN pip install -r req*/release.txt
RUN pip install -r req*/test.txt
ADD *.rst LICENSE MANIFEST.in *.txt *.sh *.cfg  *.py *.ini ./
ADD src/ src/
ENTRYPOINT /app/docker-entry.sh
