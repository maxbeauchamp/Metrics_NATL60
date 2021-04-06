# Metrics_NATL60 for the SSH Mapping Data Challenge 2020

This repository contains pieces of codes to submit and compare results on the SSH interpolation task

![Farmers Market Finder Demo](figs/animation_grads_OSSE.gif)

## Motivation

The goal is to investigate how to best reconstruct sequences of Sea Surface Height (SSH) maps from partial satellite altimetry observations. This data challenge follows an _Observation System Simulation Experiment_ framework: "Real" full SSH are from a numerical simulation with a realistic, high-resolution ocean circulation model: the reference simulation. Satellite observations are simulated by sampling the reference simulation based on realistic orbits of past, existing or future altimetry satellites. A baseline reconstruction method is provided, namely optimal interpolation (see below), and some practical goals will have to be defined in this challenge such as:
* to beat this baseline according to scores also described below and in Jupyter notebooks.
* to build a webpage where other teams can dynamically run their method and confront their performance scores to other methods
* to allow pangeo binder link work on a distant virtual machine with GPU capabilities to ease the reproduction of DL methods

The datasets are hosted [here](https://s3.eu-central-1.wasabisys.com/melody) with Wasabi Cloud Storage solution, see below to see how to download the public datasets.

### Reference simulation

The Nature Run (NR) used in this work corresponds to the NATL60 configuration  (Ajayi et al. 2020 doi:[10.1029/2019JC015827](https://doi.org/10.1029/2019JC015827)) of the NEMO (Nucleus for European Modeling of the Ocean) model. It is one of the most advanced state-of-the-art basin-scale high-resolution (1/60°) simulation available today, whose surface field effective resolution is about 7km.
To download the *daily reference* dataset, do: 
```shell
wget https://s3.eu-central-1.wasabisys.com/melody/ref.nc -O    "ref.nc"
```

### Observations

The SSH daily observations include:
* simulations of Topex-Poseidon, Jason 1, Geosat Follow-On, Envisat, and SWOT altimeter data. This nadir altimeters constellation was operating during the 2003-2005 period and is still considered as a historical optimal constellation in terms of spatio-temporal coverage.
* simulations of the upcoming SWOT mission (2021) providing 2D wide-swath observations to the along-track 1D nadir reference constellation. 
All the data (nadir & SWOT) are simulated based on the NATL60 baseline. Realistic observation errors can optionnaly be included in the interpolation.
To download the *daily observation* dataset, do: 
```shell
wget https://s3.eu-central-1.wasabisys.com/melody/data.nc -O   "data.nc"
```

### Optimal Interpolation (OI)

The DUACS system is an operational production of sea level products for the Marine (CMEMS)
and Climate (C3S) services of the E.U. Copernicus program, on behalf of the CNES french space
agency. It is mainly based on optimal interpolation techniques whose parameters are fully described
in Taburel et al. (2020). 
To download the *daily OI* dataset, do: 
```shell
wget https://s3.eu-central-1.wasabisys.com/melody/oi.nc -O     "oi.nc"
```

### Data training & evaluation sequence

All the datasets (NATL60 reference, nadir/SWOT, OI) are provided on the same regular grids with 0.05°x0.05° effective resolution. The dataset covers the period starting from 2012-10-01 to 2013-09-30.

Two family of experiments can be considered:
* *Experience n.1*. Because the NATL60 native run is
only one-year long which is relatively short in comparison with the training period typically used in this type of work. To get around this issue, a four 20-days long validation period can be used (see the corresponding timeline below). This period is homogeneously distributed along this one-year dataset. This configuration is in particular used in [Beauchamp et al. (2020)](https://hal-imt-atlantique.archives-ouvertes.fr/hal-02929973).

![Data Sequence](figs/DC-data_availability_1.png)
 
* *Experience n.2*. In this second experiment, the evaluation and training periods are built according to spin-up related methods (typically model-based data assimilation):
  * Regarding the evaluation period, the SSH interpolations will be assessed over the period from 2012-10-22 to 2012-12-02: 42 days, which is equivalent to two SWOT cycles in the SWOT science phase orbit.
  * Regarding the learning period, the **reference data** can be used from 2013-01-02 to 2013-09-30. But the reference data between 2012-12-02 and 2013-01-02 should never be used so that any learning period or other method-related-training period can be considered uncorrelated to the evaluation period.
Last, for reconstruction methods that need a spin-up, the **observations** can be used from 2012-10-01 until the beginning of the evaluation period (21 days). This spin-up period is not included in the evaluation

![Data Sequence](figs/DC-data_availability_2.png)

## How to submit new results:

 1) Generate the submission data here as a netcdf compliant with this one (same dims, coords, data vars): [example test ds](https://s3.eu-central-1.wasabisys.com/melody/quentin_test_submission.fp_genn_lag.nc):
```
Dimensions:    (lat: 200, lon: 200, time: 80)
Coordinates:
  * lon        (lon) float64 -65.0 -64.95 -64.9 -64.85 ... -55.15 -55.1 -55.05
  * lat        (lat) float64 33.0 33.05 33.1 33.15 ... 42.8 42.85 42.9 42.95
  * time       (time) int64 0 1 2 3 4 5 6 7 8 9 ... 71 72 73 74 75 76 77 78 79
Data variables:
    longitude  (lat, lon) float64 ...
    latitude   (lat, lon) float64 ...
    Time       (time) object ...
    ssh        (time, lat, lon) float64 ...
    
```

 3) Make it publicly accessible (s3, github...)
 4) Add your submission file in the submissions folder with the following fields :

```yaml
data: https://s3.eu-central-1.wasabisys.com/melody/quentin_test_submission.fp_genn_lag.nc # url of your test data
code: https://github.com/maxbeauchamp/4DVARNN-DinAE # link to the code used to generate the data (can be a notebook)
domain: GULFSTREAM # domain
submitter: Quentin # Name of the submitter
experiment_label: fp genn nadir+swot lag 0 with OI # Experiment label
experiment_slug: fp-genn-lag-0 # Experiment slug (no spaces)
```

**Finally create a pull request on this repo and the metrics will be computed for all the submission files and posted as a comment on the pull request page**
