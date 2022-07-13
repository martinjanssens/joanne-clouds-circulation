#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 11:17:27 2022

@author: martinjanssens
"""

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def mmm(data,qu):
    if len(data.shape) == 3:
        axs = (0,1)
    elif len(data.shape) == 2:
        axs=0
    mean = ma.mean(data, axis=axs)
    ma.set_fill_value(data, np.nan)
    data = np.ma.getdata(data)
    mini = np.nanpercentile(data, qu, axis=axs)
    maxi = np.nanpercentile(data, 100-qu, axis=axs)
    return mean, mini, maxi

def find_flight_days(ds):
    ids = ds['segment_id'][:]
    dates = []
    dates_unique = []
    ac = []
    for i in range(len(ids)):
        idi = ids[i].item()
        ac.append(idi.split('-')[0])
        date = idi.split('-')[1].split('_')[0]
        dates.append(date)
        if date not in dates_unique:
            dates_unique.append(date)
    dates_unique = np.sort(dates_unique)
    return ac, dates, dates_unique

def find_inds_day(date,dates,ac=None,acs=None):
    idates = []
    for j in range(len(dates)):
        if dates[j] == date:
            if ac in ['HALO','P3']:
                if ac==acs[j]:
                    idates.append(j)
            else:
                idates.append(j)
    return idates

def flight_day_mean(dates, dates_unique, var):
    var_fd = np.zeros((len(dates_unique),var.shape[1]))
    for i in range(len(dates_unique)):
        idates = find_inds_day(dates_unique[i],dates)
        var_fd[i,:] = np.mean(var[idates,:],axis=0)
    return var_fd

def find_rad_inds_flight_day(time_rad, time_fd, platform_rad):
    idirad = []
    for j in range(len(time_rad)):
        tri = time_rad[j]
        if tri.astype('datetime64[D]') == time_fd.astype('datetime64[D]'):
            if platform_rad[j] == 'HALO':
                idirad.append(j)
    return idirad

def plot_per_day(terms, labels, ibudg, dates_unique, zflim, colors, ncols, 
                 title=None, xlab='[W]', fh=1, alpha=0.75, lw=2, 
                 xlim=0.2,xmin=None,axs=[]):
    nrows = len(ibudg)//ncols
    if len(axs)==0:
        fig,axs = plt.subplots(ncols=ncols,nrows=nrows,sharex=True,sharey=True,
                               figsize=(2*ncols,4*nrows))
        fig.suptitle(title)
    k = 0
    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            
            date_budg = dates_unique[ibudg[k]]
            
            termsplt = labels if i==0 and j==ncols-1 else np.empty(len(labels))
            for l in range(terms.shape[0]):
                term = terms[l,k,:]
                axs[i,j].plot(term*fh, zflim,c=colors[l],alpha=alpha,lw=lw,label=termsplt[l])

            axs[i,j].set_title(date_budg[:2]+'/'+date_budg[2:])
            if xmin==None:
                axs[i,j].set_xlim((-xlim,xlim))
            else:
                axs[i,j].set_xlim((-xmin,xlim))
            
            if j == 0:
                axs[i,j].set_ylabel('Height [m]')
            
            if i == nrows-1:
                axs[i,j].set_xlabel(xlab)
            
            if i == 0 and j == ncols-1:
                axs[i,j].legend(loc='upper left',bbox_to_anchor=(1,1))
    
            k += 1

    return axs

def plot_per_day_time(terms, times, labels, ibudg, dates_unique, colors, ncols, 
                      title='', xlab='',ylab='', fh=1, alpha=0.75, lw=2, 
                      ylim=(None,None),axs=[]):
    nrows = len(ibudg)//ncols
    if len(axs)==0:
        fig,axs = plt.subplots(ncols=ncols,nrows=nrows,sharey=True,
                               figsize=(2.5*ncols,2.5*nrows))
        fig.suptitle(title)
    k = 0
    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            
            date_budg = dates_unique[ibudg[k]]
            
            termsplt = labels if i==0 and j==ncols-1 else np.empty(len(labels))
            time = times[k,:]
            for l in range(terms.shape[0]):
                term = terms[l,k,:]
                axs[i,j].plot(time, term*fh, c=colors[l],alpha=alpha,lw=lw,label=termsplt[l])

            axs[i,j].set_title(date_budg[:2]+'/'+date_budg[2:])
            
            axs[i,j].set_xticklabels(axs[i,j].get_xticks(), rotation=30, ha="right")
            axs[i,j].xaxis.set_major_locator(mdates.HourLocator(interval=2))
            axs[i,j].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

            if (ylim[0] or ylim[1]) != None:
                axs[i,j].set_ylim(ylim)
            
            if j == 0:
                axs[i,j].set_ylabel(ylab)
            
            if i == nrows-1:
                axs[i,j].set_xlabel(xlab)
            
            if i == 0 and j == ncols-1:
                axs[i,j].legend(loc='upper left',bbox_to_anchor=(1,1))
    
            k += 1
    plt.subplots_adjust(hspace=0.5)
    return axs

def scatter_per_day(termsx, termsy, labels, ibudg, dates_unique, colors, ncols, 
                    title=None, xlab='', ylab='', fh=1, xlim=(-0.2,0.2),
                    ylim=(-0.2,0.2),axs=[]):
    nrows = len(ibudg)//ncols
    if len(axs)==0:
        fig,axs = plt.subplots(ncols=ncols,nrows=nrows,sharex=True,sharey=True,
                               figsize=(2*ncols,2*nrows))
        fig.suptitle(title)
    k = 0
    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            
            date_budg = dates_unique[ibudg[k]]
            
            # FIXME Need to add label
            termsplt = labels if i==0 and j==ncols-1 else np.empty(len(labels))
            axs[i,j].scatter(termsx[k,:]*fh,termsy[k,:]*fh,c=colors) 
            axs[i,j].plot(termsx[k,:]*fh,termsy[k,:]*fh,c=colors[-1],linestyle='--')

            axs[i,j].set_title(date_budg[:2]+'/'+date_budg[2:])
            axs[i,j].set_xlim(xlim)
            axs[i,j].set_ylim(ylim)
            
            if j == 0:
                axs[i,j].set_ylabel(ylab)
            
            if i == nrows-1:
                axs[i,j].set_xlabel(xlab)
            
            if i == 0 and j == ncols-1:
                axs[i,j].legend(loc='upper left',bbox_to_anchor=(1,1))
    
            k += 1

    return axs

def vint(field,rhob,z):
    if len(field.shape) == 3:
        var = np.trapz(rhob*field,z,axis=2)
    elif len(field.shape) == 2:
        var = np.trapz(rhob*field,z,axis=1)
    return var
