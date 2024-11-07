import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import xarray


def get_daily_sst_clim(clim_file, datestr):
    """Compute daily sst climatology
    Inputs: clim_file is either the redsea_sst_max_clim or redsea_sst_mean_clim file  
            datestr is date string in format yyyy-mm-dd
    """

    ##  LOAD THE CLIMATOLOGY DATA:
    sst_clim = clim_file["analysed_sst"].values
   
    ## Calculate the daily SST climatology for this date:
    td = pd.to_datetime(datestr, format = '%Y-%m-%d')
    dtstr = str(td.year) + '%02d'% td.month + '15'
    
    dtdates = np.empty(3, dtype='object')
    dtdates[1] = datetime.strptime(dtstr,'%Y%m%d')
    dtdates[0] = dtdates[1] + relativedelta(months=-1)
    dtdates[2] = dtdates[1] + relativedelta(months=+1)
    
    if td.day>15:
        d1 = dtdates[1]
        d2 = dtdates[2]
        totdays = (d2 - d1).days
        mindays = (td - d1).days
        dayfrac = np.float64(mindays)/np.float64(totdays)
        clim_A = sst_clim[d1.month-1,:,:]
        clim_B = sst_clim[d2.month-1,:,:]
        daily_sst_clim = dayfrac * (clim_B-clim_A) + clim_A
        
    elif td.day<15: 
        d1 = dtdates[0]
        d2 = dtdates[1]
        totdays = (d2 - d1).days
        mindays = (td - d1).days
        dayfrac = np.float64(mindays)/np.float64(totdays)
        clim_A = sst_clim[d1.month-1,:,:]
        clim_B = sst_clim[d2.month-1,:,:]
        daily_sst_clim = dayfrac * (clim_B-clim_A) + clim_A
    else:
        dayfrac = 0
        daily_sst_clim = sst_clim[td.month-1,:,:]
       
    return daily_sst_clim

