# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

RUN apt-get --allow-releaseinfo-change update
RUN apt-get install -y build-essential pkg-config gfortran

RUN mkdir /tmp/cellmaps_pipeline
COPY ./ /tmp/cellmaps_pipeline/
RUN conda install python=3.10 -y

RUN conda install scipy=1.12.0 -y
RUN pip install /tmp/cellmaps_pipeline

RUN rm -rf /tmp/cellmaps_pipeline

ENTRYPOINT ["/opt/conda/bin/cellmaps_cywebserviceapp.py"]

CMD ["--help"]
