# CANARI Sprint Tutorials Repository

Welcome to the GitHub repository dedicated to tutorials for the CANARI Sprint. Here, you will find comprehensive guides and resources to get you started and enhance your experience with the CANARI Sprint.

## Environment Setup on Jasmin Jupyter Hub

In order to setup the conda environment, please follow the steps described in the [documentation](https://canari-sprint.github.io/docs/tutorials/#tutorial-1-configuring-and-using-the-jasmin-notebooks-service).

If you want to use your own environment, you can create a `.yml` like the [environment.yml](https://github.com/CANARI-sprint/tutorials/blob/main/environment.yml) file. And then follow these steps

1. Create the conda environment using the following command. This will install all required packages as specified in the `environment.yml` file and create the `canari-sprint` environment.

    ```bash
    conda env create --file environment.yml
    ```
This action may take a 10-30 minutes. To monitor this command, you may add the flag `-vv` to the command.

2. Now, you need to add two packages in order to allow the notebook to see the environment:

    ```bash
    conda install --name canari-sprint ipykernel
    ```

3. And then, install the environment as an "ipykernel" so that the Notebook Service will find it:

    ```bash
    conda run --name canari-sprint python -m ipykernel install --user --name canari-sprint
    ```

Now, start a new Notebook or Console and you will see that `canari-sprint` is given as kernel option. You can now use it :-)

4. (Only if you are running locally): Once the installation is complete, activate the `canari-sprint` environment:

    ```bash
    conda activate canari-sprint
    ```

## Accessing CANARI Workspace Data

To access the CANARI workspace data, you may want to create a symbolic link in your user directory:

```
ln -s /gws/nopw/j04/canari /home/users/<USERNAME>/CANARI
```

## Obtaining Configuration Data

For accessing sample data and necessary configuration files, follow the steps below:

    ```bash
    wget -c https://github.com/British-Oceanographic-Data-Centre/COAsT/archive/refs/heads/master.zip && unzip master.zip && rm -f master.zip
    mv COAsT-master/config ./config && rm -rf COAsT-master
    ```

## Tutorial Overview

The tutorials provided in this repository are adapted from the [COAsT package documentation](https://british-oceanographic-data-centre.github.io/COAsT/). Here's what you can expect:

- **Gridded Data Handling:** Learn how to work with gridded datasets using the COAsT package.

- **General Utility and Analysis Tools:** Discover scripts for general utility and analysis within the COAsT framework.
