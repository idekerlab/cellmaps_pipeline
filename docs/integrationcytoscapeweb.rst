.. _integrationcytoscapeweb:

========================================
Integration with Cytoscape Web
========================================

`Cytoscape Web`_ is a web-based network visualization and analysis 
tool built on modern web technologies. It allows users to visualize, 
analyze, and share complex networks directly within their web 
browsers without the need for installing any software. 

The Cell Mapping Toolkit is using the `Cytoscape Web Service App`_ framework 
to expose the individual steps of the pipeline through `Cytoscape Web`_.


Cytoscape Web Community Detection aka Hierarchy Generation App
================================================================

This section walks you through the steps to integrate and use the 
Cell Mapping Toolkit Community Detection aka Hierarchy Generation step/tool 
within Cytoscape Web.

This `Cytoscape Web Service App`_ takes a Network, clusters it at 
multiple resolutions to generate a hierarchy describing those communities.

1. In `Cytoscape Web`_ open the context menu, click **Apps**, then choose
   **Manage Apps**.
   
   .. image:: ./images/cd1.png
      :align: center
      :alt: Cytoscape Web Apps menu for managing external services

2. Paste the URL below into the
   **Enter new external service URL** input box and click **Add**.

   .. code-block:: text

      https://cd.ndexbio.org/cy/cytocontainer/v1/cellmappingtoolkitcommunitydetection

   .. image:: ./images/cd2.png
      :align: center
      :width: 300px
      :alt: Cytoscape Web Apps menu for adding the Cell Mapping Toolkit Community Detection app

3. Open the Sample Networks panel (or any network you prefer) and load the
   **Yeast preturbation** network. To open the Sample Networks panel, go to **Data** in the context menu, then click **Open Sample Networks**.

   .. image:: ./images/cd3.png
      :align: center
      :alt: Cytoscape Web Sample Networks panel showing the Yeast preturbation network

4. Go to **Apps -> Cell Maps for AI (Cell Mapping Toolkit)-> Cell Mapping Toolkit Community Detection**
   and click it to open the dialog.

   .. image:: ./images/cd4.png
      :align: center
      :alt: Cytoscape Web Apps menu showing the Cell Mapping Toolkit Community Detection app

5. Copy the NDEx UUID shown for the **Yeast preturbation** network and paste it
   into the **NDEx UUID of input interactome** field.

   .. image:: ./images/cd5.png
      :align: center
      :alt: Cytoscape Web dialog for the Cell Mapping Toolkit Community Detection app showing the NDEx UUID input field


   .. note::

      If an invalid UUID is provided, the hierarchy will still be generated, but no interaction network
      will be displayed in the subnetwork viewer when clicking on the communities/assemblies on the left panel.

6. Click **Submit** to start the analysis. The app runs community detection on
   the selected network and, once finished, returns the generated hierarchy to
   `Cytoscape Web`_. 

   .. image:: ./images/cd6.png
      :align: center
      :alt: Cytoscape Web showing the resulting hierarchy from the Cell Mapping Toolkit Community Detection app

.. _Cytoscape Web: https://web.cytoscape.org/
.. _Cytoscape Web Service App: https://cytoscape-web.readthedocs.io/en/latest/Extending.html#service-apps

