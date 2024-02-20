FROM debian:bookworm-slim as base
ARG PIXIENV
WORKDIR /home/hydromt
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH=/root/.pixi/bin:$PATH
COPY pixi.toml pixi.lock pyproject.toml README.rst ./
COPY data/ ./data
COPY hydromt/ ./hydromt
RUN pixi run --locked -e ${PIXIENV} install-hydromt \
  && rm -rf /root/.cache \
  && find . -follow -delete -type f -name *.pyc
ENV RUNENV="${PIXIENV}"
# Workaround: write a file that runs pixi with correct environment.
# This is needed because the argument is not passed to the entrypoint.
RUN echo "pixi run --locked -e ${RUNENV} \$@" > /run_pixi.sh
ENTRYPOINT ["sh", "/run_pixi.sh"]
CMD ["hydromt","--models"]

FROM base as full
COPY examples/ ./examples
COPY tests/ ./tests

FROM base as slim

FROM base as min
