FROM condaforge/miniforge3

SHELL ["/bin/bash", "-c"]

# Install dependencies required for C extensions like leidenalg
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    gfortran \
    cmake \
    libigraph-dev \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /tmp/cellmaps_pipeline
COPY ./ /tmp/cellmaps_pipeline/

RUN conda install -y python=3.10 scipy=1.12.0

# install your package and dependencies
RUN pip install /tmp/cellmaps_pipeline

RUN rm -rf /tmp/cellmaps_pipeline

ENTRYPOINT ["/opt/conda/bin/cellmaps_cywebserviceapp.py"]
CMD ["--help"]
