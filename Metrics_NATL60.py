#!/usr/bin/env python

""" Metrics_NATL60 """

__author__ = "Maxime Beauchamp"
__version__ = "0.0.1"
__date__ = "2021-02-10"
__email__ = "maxime.beauchamp@imt-atlantique.fr"

# basepath="/linkhome/rech/genimt01/uba22to"
# datapath="/gpfswork/rech/yrf/uba22to/DATA"
# scratchpath="/gpfsscratch/rech/yrf/uba22to/4DVARNN-DinAE_xp"
basepath="_base"
datapath="_data"
scratchpath="_scratch"

print("Initializing Metrics_NATL60 libraries...",flush=True)

import os
from os.path import join as join_paths
import sys
import numpy as np
import einops
from datetime import date, datetime, timedelta
import cv2

import xarray as xr
import xrft
import pickle
import logging
from dask.diagnostics import ProgressBar
from sklearn.decomposition import PCA

# %MATPLOTLIB
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import mpl_toolkits.axisartist.grid_finder as GF
import mpl_toolkits.axisartist.floating_axes as FA
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.projections import PolarAxes
import matplotlib.dates as mdates
import matplotlib.colors as colors
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from matplotlib.ticker import ScalarFormatter

# %CARTOPY
from cartopy import crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# %IMPORT
sys.path.insert(0,basepath+'/Metrics_NATL60/utils')
sys.path.insert(0,basepath+'/Metrics_NATL60/tools')
from tools.gradient       import *
from tools.imputing_nan   import *
from tools.plot           import *
from utils.plot_nRMSE     import *
from utils.nRMSE_score     import *
print("...Done") # ... initializing Libraries


