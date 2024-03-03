# CANARI Sprint Tutorials Repository

Welcome to the GitHub repository dedicated to tutorials for the CANARI Sprint. Here, you will find comprehensive guides and resources to get you started and enhance your experience with the CANARI Sprint.

## Setting Up Your Environment on Jasmin Jupyter Hub

For configuring the conda environment, please adhere to the instructions outlined in our [documentation](https://canari-sprint.github.io/docs/jasmin_notebook_service/).

If you prefer to configure a custom environment, you're encouraged to model it after our [environment.yml](https://github.com/CANARI-sprint/tutorials/blob/main/environment.yml) file by following these steps:

1. To create the conda environment, execute the command below. This installs all necessary packages as delineated in the `environment.yml` file and establishes the `canari-sprint` environment.

    ```bash
    conda env create --file environment.yml
    ```
Note: This process might take between 10 to 30 minutes. Consider using `-vv` flag for verbose output.

2. Next, incorporate two essential packages to ensure the notebook interface can interact with the environment:

    ```bash
    conda install --name canari-sprint ipykernel
    ```

3. Subsequently, register the environment as an "ipykernel" to make it recognizable to the Notebook Service:

    ```bash
    conda run --name canari-sprint python -m ipykernel install --user --name canari-sprint
    ```

Upon starting a new Notebook or Console, you will see `canari-sprint` as an available kernel option, ready for use.

4. (For local setups only): Once installation concludes, activate the `canari-sprint` environment with:

    ```bash
    conda activate canari-sprint
    ```

## Accessing CANARI Workspace Data

To link to the CANARI workspace data from your user directory, consider creating a symbolic link:

```
ln -s /gws/nopw/j04/canari /home/users/<USERNAME>/CANARI
```

## Tutorials Overview

The first 8 tutorials refer to the [COAst python package](https://british-oceanographic-data-centre.github.io/COAsT/#about).  Expect to find tutorials on:

- [Basic Data Manipulation](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/1_basic_manipulation.ipynb): Introduction to data handling using the COAsT package.
- [Exporting to NetCDF](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/2_export_to_netcdf.ipynb): Guide on exporting outputs to netCDF format for future use or analysis.
- [Climatology Tutorial](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/3_climatology_tutorial.ipynb): Demonstrates calculating climatological means and multi-year climatologies.
- [Calculating EOFs](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/4_calculate_eof.ipynb): How to utilize COAsT for computing Empirical Orthogonal Functions (EOFs).
- [Potential Energy Analysis](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/5_potential_energy.ipynb): Tutorial on calculating Potential Energy Anomaly and applying regional masking.
- [Pycnocline Diagnostics](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/6_pycnocline.ipynb): Exploration of pycnocline depth and thickness diagnostics.
- [Seasonal Decomposition](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/7_seasonal_decomp.ipynb): Techniques for decomposing time series into trend, seasonal, and residual components.
- [Transect Calculations](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/8_transect_calculation.ipynb): Methods for creating data transects.
- [Basic Plots and Analysis](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/9_basic_plots_and_analysis.ipynb): Utilizing CANARI-LE historical data for Sea Surface Temperature (SST) visualization.
- [UK Precipitation Plots](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/0_UK_Precipitation_with_iris.ipynb): Making plots of UK precipitation using the iris python package, curtesy of Ben Harvey.
- [Box Profile Development](https://github.com/CANARI-sprint/tutorials/blob/main/notebooks/11_compute_and_plot_an_ocean_profile_using_lotus.ipynb): Computing ocean profiles with selected variables making use of the lotus queue on JASMIN.
