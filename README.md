# Metrics_NATL60
A repo to submit and compare results on the SSH interpolation task


## How to submit :
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
