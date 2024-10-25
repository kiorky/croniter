ARG RSYNC=corpusops/rsync
ARG PY_VER=3.12.1
ARG BASE=${BASE:-corpusops/ubuntu-bare:24.04}
FROM $BASE AS base
ENV CFLAGS="-I/usr/include/python3.12/"
ADD apt.txt ./
RUN <<EOF
set -ex
apt update
sed -re "/^# dev deps/,$ d" /apt.txt|grep -vE "^\s*#"|tr "\n" " " > apt.runtime
apt-get install -qq -y --no-install-recommends $( cat apt.runtime )
if ! ( python --version );then
    ln -s /usr/bin/python3 /usr/bin/python
fi
if ! ( pip --version );then
wget https://bootstrap.pypa.io/get-pip.py
chmod +x get-pip.py
./get-pip.py --break-system-packages
fi
rm -rf /var/lib/apt/lists/*
EOF
FROM base AS final
RUN <<EOF
set -ex
apt update && apt-get install -qq -y --no-install-recommends $( grep -Ev '^#' apt.txt )
( mkdir src || true ) && touch src/__init__.py
EOF
WORKDIR app
ADD *.rst LICENSE MANIFEST.in *.txt *.cfg *.py *.ini ./
ADD ./src/ src/
ADD requirements/test.txt requirements/base.txt requirements/
RUN pip install --no-cache-dir --break-system-packages -r req*/test.txt
ADD requirements/lint.txt requirements/
RUN pip install --no-cache-dir --break-system-packages -r req*/lint.txt
ADD requirements/release.txt requirements/
RUN pip install --no-cache-dir --break-system-packages -r req*/release.txt
ADD requirements/tox.txt requirements/
RUN pip install --no-cache-dir --break-system-packages -r req*/tox.txt
RUN <<EOF
set -ex
apt remove -y python3-dev libpython3-dev cargo
apt autoremove -y
rm -rf /var/lib/apt/lists/*
EOF

# SQUASH Stage
FROM $RSYNC AS squashed-rsync
FROM base  AS squashed-ancestor
WORKDIR /app
ARG ROOTFS="/BASE_ROOTFS_TO_COPY_THAT_WONT_COLLIDE_1234567890"
ARG PATH="${ROOTFS}_rsync/bin:$PATH"
RUN --mount=type=bind,from=final,target=$ROOTFS --mount=type=bind,from=squashed-rsync,target=${ROOTFS}_rsync \
rsync -Aaz --delete ${ROOTFS}/ / --exclude=/proc --exclude=/sys --exclude=/etc/resolv.conf --exclude=/etc/hosts --exclude=$ROOTFS* --exclude=dev/shm --exclude=dev/pts --exclude=dev/mqueue
ADD *.rst LICENSE MANIFEST.in *.txt *.cfg *.py *.ini *sh ./
ADD src/ src/
ENTRYPOINT ["/app/docker-entry.sh"]
CMD []
