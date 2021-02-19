# Metrics_NATL60
A repo to submit and compare results on the SSH interpolation task


## How to submit :
 - Generate the submission data here as a netcdf compliant with this one (same dims, coords, data vars): [example test ds](https://s3.eu-central-1.wasabisys.com/melody/quentin_test_submission.fp_genn_lag.nc) 
 - You should then make it publicly accessible (s3, github...)
 - You can the add your submission in the submissions folder which is a file with the following fields :

```yaml
data: https://s3.eu-central-1.wasabisys.com/melody/quentin_test_submission.fp_genn_lag.nc # url of your test data
code: https://github.com/maxbeauchamp/4DVARNN-DinAE # link to the code used to generate the data (can be a notebook)
domain: GULFSTREAM # domain
submitter: Quentin # Name of the submitter
experiment_label: fp genn nadir+swot lag 0 with OI # Experiment label
experiment_slug: fp-genn-lag-0 # Experiment slug (no spaces)
```

**Finally create a pull request on this repo and the metrics will be computed for all the submission files and posted as a comment on the pull request page**
