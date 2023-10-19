===========
Outputs
===========

This pipeline tool creates several directories in the specified output directory.
Below is a list and description of these output directories with links to more
detailed information.

* **1.image_download**

  Output from `cellmaps_imagedownloader, <https://cellmaps-imagedownloader.readthedocs.io>`__
  for more information on output `click here <https://cellmaps-imagedownloader.readthedocs.io/en/latest/outputs.html>`__

  Example content:

  .. code-block::

    1.image_download/
    ├── 1_image_gene_node_attributes.tsv
    ├── 2_image_gene_node_attributes.tsv
    ├── blue/
    ├── green/
    ├── image_gene_node_attributes.errors
    ├── red/
    ├── ro-crate-metadata.json
    ├── samplescopy.csv
    ├── task_1697498858_finish.json
    ├── task_1697498858_start.json
    ├── uniquecopy.csv
    └── yellow/

* **1.ppi_download**

  Output from `cellmaps_ppidownloader, <https://cellmaps-ppidownloader.readthedocs.io>`__
  for more information on output `click here <https://cellmaps-ppidownloader.readthedocs.io/en/latest/outputs.html>`__

  Example content:

  .. code-block::

    1.ppi_download/
    ├── ppi_edgelist.tsv
    ├── ppi_gene_node_attributes.errors
    ├── ppi_gene_node_attributes.tsv
    ├── ro-crate-metadata.json
    ├── task_1697498907_finish.json
    └── task_1697498907_start.json

* **2.ppi_embedding**

  Output from `cellmaps_ppi_embedding, <https://cellmaps-ppi-embedding.readthedocs.io>`__
  for more information on output `click here <https://cellmaps-ppi-embedding.readthedocs.io/en/latest/outputs.html>`__

  Example content:

  .. code-block::

    2.ppi_embedding/
    ├── ppi_emd.tsv
    ├── ro-crate-metadata.json
    ├── task_1697498914_finish.json
    └── task_1697498914_start.json


* **2.image_embedding_fold#**

  Output from `cellmaps_image_embedding, <https://cellmaps-image-embedding.readthedocs.io>`__
  for more information on output `click here <https://cellmaps-image-embedding.readthedocs.io/en/latest/outputs.html>`__

  Example content:

  .. code-block::

    2.image_embedding_fold1/
    ├── blue_resize/
    ├── green_resize/
    ├── image_emd.tsv
    ├── labels_prob.tsv
    ├── red_resize/
    ├── ro-crate-metadata.json
    ├── task_1697498903_finish.json
    ├── task_1697498903_start.json
    └── yellow_resize/


* **3.coembedding_fold#**

  Output from `cellmaps_coembedding, <https://cellmaps-coembedding.readthedocs.io>`__
  for more information on output `click here <https://cellmaps-coembedding.readthedocs.io/en/latest/outputs.html>`__

  Example content:

  .. code-block::

    3.coembedding_fold1/
    ├── coembedding_emd.tsv
    ├── ro-crate-metadata.json
    ├── task_1697498919_finish.json
    └── task_1697498919_start.json

* **4.hierarchy**

  Output from `cellmaps_generate_hierarchy, <https://cellmaps-generate-hierarchy.readthedocs.io>`__
  information on output `click here <https://cellmaps-generate-hierarchy.readthedocs.io/en/latest/outputs.html>`__

  Example content:

  .. code-block::

    4.hierarchy/
    ├── cdaps.json
    ├── hidef_output.edges
    ├── hidef_output.nodes
    ├── hidef_output.pruned.edges
    ├── hidef_output.pruned.nodes
    ├── hidef_output.weaver
    ├── hierarchy.cx
    ├── ppi_cutoff_0.001.cx
    ├── ppi_cutoff_0.001.id.edgelist.tsv
    ├── ppi_cutoff_0.05.cx
    ├── ppi_cutoff_0.05.id.edgelist.tsv
    ├── ppi_cutoff_0.1.cx
    ├── ppi_cutoff_0.1.id.edgelist.tsv
    ├── ro-crate-metadata.json
    ├── task_1697498926_finish.json
    └── task_1697498926_start.json

* **5.hierarchyeval**

  Coming soon...
