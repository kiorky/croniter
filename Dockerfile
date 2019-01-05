ARG RSYNC=corpusops/rsync
ARG PY_VER=3.12.1
ARG BASE=${BASE:-python:${PY_VER}}
FROM $BASE AS base
ENV CFLAGS="-I/usr/include/python3.12/"
FROM base AS final
WORKDIR /app
RUN <<EOF
set -ex
apt update
apt install -y python3 python3-dev libpython3-dev cargo
if ! ( python --version );then
    ln -s /usr/bin/python3 /usr/bin/python
fi
if ! ( pip --version );then
wget https://bootstrap.pypa.io/get-pip.py
chmod +x get-pip.py
./get-pip.py --break-system-packages
fi
mkdir src/ && touch src/__init__.py
EOF
ADD *.rst LICENSE MANIFEST.in *.txt *.cfg *.py *.ini ./
ADD requirements/ ./requirements/
RUN <<EOF
pip install --no-cache-dir --break-system-packages -r req*/base.txt
pip install --no-cache-dir --break-system-packages -r req*/test.txt
pip install --no-cache-dir --break-system-packages -r req*/release.txt
EOF
RUN <<EOF
apt remove -y python3-dev libpython3-dev cargo
apt autoremove -y
rm -rf /var/lib/apt/lists/*
EOF

# SQUASH Stage
FROM $RSYNC AS squashed-rsync
FROM base  AS squashed-ancestor
ARG ROOTFS="/BASE_ROOTFS_TO_COPY_THAT_WONT_COLLIDE_1234567890"
ARG PATH="${ROOTFS}_rsync/bin:$PATH"
RUN --mount=type=bind,from=final,target=$ROOTFS --mount=type=bind,from=squashed-rsync,target=${ROOTFS}_rsync \
rsync -Aaz --delete ${ROOTFS}/ / --exclude=/proc --exclude=/sys --exclude=/etc/resolv.conf --exclude=/etc/hosts --exclude=$ROOTFS* --exclude=dev/shm --exclude=dev/pts --exclude=dev/mqueue
ADD *.rst LICENSE MANIFEST.in *.txt *.cfg *.py *.ini *sh ./
ADD src/ src/
ENTRYPOINT /app/docker-entry.sh
