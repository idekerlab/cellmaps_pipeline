# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

RUN apt-get --allow-releaseinfo-change update
RUN apt-get install -y build-essential 

RUN mkdir /tmp/cellmaps_pipeline
COPY ./ /tmp/cellmaps_pipeline/
RUN pip install /tmp/cellmaps_pipeline

RUN rm -rf /tmp/cellmaps_pipeline

ENTRYPOINT ["/opt/conda/bin/cellmaps_pipelinecmd.py"]

CMD ["--help"]
