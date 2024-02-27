# CANARI Sprint Tutorials Repository

Welcome to the GitHub repository dedicated to tutorials for the CANARI Sprint. Here, you will find comprehensive guides and resources to get you started and enhance your experience with the CANARI Sprint.

## Environment Setup on Jasmin Jupyter Hub

To get started, you'll first need to set up your conda environment. Follow these steps:

1. Create the conda environment using the following command. This will install all required packages as specified in the `environment.yml` file and create the `canari-sprint` environment.

    ```bash
    conda env create --file environment.yml
    ```

2. Once the installation is complete, activate the `canari-sprint` environment:

    ```bash
    conda activate canari-sprint
    ```

3. For instructions on how to configure this conda environment on Jupyter Hub, refer to the detailed guide available at [Ceda-Notebooks Documentation](https://github.com/cedadev/ceda-notebooks/blob/master/notebooks/docs/add_conda_envs.ipynb).

`!IMPORTANT: SECTION IN PROGRESS`

## Accessing CANARI Workspace Data

To access the CANARI workspace data, you may need to create a symbolic link in your user directory:

```
ln -s /gws/nopw/j04/canari /home/users/<USERNAME>/CANARI
```

`!IMPORTANT: SECTION IN PROGRESS`

## Obtaining Sample and Configuration Data

For accessing sample data and necessary configuration files, follow the steps below:

1. Download the sample data using the command:

    ```bash
    wget -q https://linkedsystems.uk/erddap/files/COAsT_example_files/COAsT_example_files.zip
    unzip COAsT_example_files.zip && mv COAsT_example_files ./example_files
    ```

2. Next, download the configuration files essential for setup:

    ```bash
    wget -c https://github.com/British-Oceanographic-Data-Centre/COAsT/archive/refs/heads/master.zip && unzip master.zip && rm -f master.zip
    mv COAsT-master/config ./config && rm -rf COAsT-master
    ```

## Tutorial Overview

The tutorials provided in this repository are adapted from the [COAsT package documentation](https://british-oceanographic-data-centre.github.io/COAsT/). Here's what you can expect:

- **Gridded Data Handling:** Learn how to work with gridded datasets using the COAsT package.

- **General Utility and Analysis Tools:** Discover scripts for general utility and analysis within the COAsT framework.

- **Altimetry Data Processing:** Explore how to process altimetry data with the COAsT package.

- **Profile Data Analysis:** Get to grips with handling profile data in COAsT.

- **Tide Gauge Data Insights:** Dive into tide gauge data analysis with our dedicated scripts.
