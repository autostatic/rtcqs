FROM debian:bookworm

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
    tzdata apt-utils build-essential \
    python3-dev python-is-python3 python3-pip \
    python3-venv && \
    apt-get dist-upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN useradd --create-home --shell /bin/bash --uid 1015 --user-group forgejo

USER forgejo

COPY --chown=forgejo:forgejo $PWD /home/forgejo/rtcqs

WORKDIR /home/forgejo/rtcqs

RUN python3 -m venv venv && \
    venv/bin/pip install --upgrade pyinstaller && \
    venv/bin/pyinstaller --onefile src/rtcqs/rtcqs.py
    venv/bin/pyinstaller --onefile --windowed src/rtcqs/rtcqs_gui.py
