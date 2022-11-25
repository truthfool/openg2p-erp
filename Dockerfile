FROM bitnami/odoo:14

ARG OPENG2P_CA_REPO=https://github.com/truthfool/openg2p-erp-community-addon
ARG OPENG2P_CA_BRANCH=master

COPY . /tmp/openg2p-erp/

RUN install_packages wget unzip

RUN . /opt/bitnami/odoo/venv/bin/activate && \
    python3 -m pip install setuptools wheel && \
    python3 -m pip install -r ./tmp/openg2p-erp/requirements.txt && \
    deactivate

RUN curl -L -o /tmp/openg2p-erp-community-addon.zip $OPENG2P_CA_REPO/archive/$OPENG2P_CA_BRANCH.zip &&\
    unzip /tmp/openg2p-erp-community-addon.zip -d /tmp
