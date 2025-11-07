.. _integrationcytoscapeweb:

========================================
Integration with Cytoscape Web
========================================

Cytoscape Web Community Detection
==================================

Community detection groups nodes that are more densely connected to each other
than to the rest of a network. The Cell Mapping Toolkit Community Detection app
takes a Networks, clusters it, and generates a hierarchy describing those communities.
Cytoscape Web *service app* makes this possible inside the browser by a small external program
that Cytoscape Web calls with the current network and that returns the resulting hierarchy.

1. In Cytoscape on the web open the context menu, click **Apps**, then choose
   **Manage Apps**.
   
   .. image:: ./images/cd1.png
      :align: center
      :alt: Cytoscape Web Apps menu for managing external services

2. Paste ``https://cd.ndexbio.org/cy/cytocontainer/v1/cellmappingtoolkitcommunitydetection`` into the
   **Enter new external service URL** input box and click **Add**.

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

6. Click **Submit** to start the analysis. The app runs community detection on
   the selected network and, once finished, returns the generated hierarchy to
   Cytoscape on the web.

   .. image:: ./images/cd6.png
      :align: center
      :alt: Cytoscape Web showing the resulting hierarchy from the Cell Mapping Toolkit Community Detection app

.. _Cytoscape Web: https://web.cytoscape.org/
