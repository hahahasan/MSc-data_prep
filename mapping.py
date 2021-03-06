#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:32:56 2018

@author: hm1234
"""

import os
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as interpolate
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

# lots of warning thrown up for the NaNs and infinities in the data
# they're just warnings so this just ignores them.
# Hopefully nothing bad happens :)
np.warnings.filterwarnings('ignore')
    
###############################################################################
#####    load the pickles

os.chdir('./pickles')

with open('vt_ss_27873.pickle', 'rb') as handle:
    vt_ss_27873 = pickle.load(handle)
with open('ti_ss_27873.pickle', 'rb') as handle:
    ti_ss_27873 = pickle.load(handle)
with open('ayc_ne_27873.pickle', 'rb') as handle:
    ayc_ne_27873 = pickle.load(handle)
with open('ayc_te_27873.pickle', 'rb') as handle:
    ayc_te_27873 = pickle.load(handle)
with open('ayc_r_27873.pickle', 'rb') as handle:
    ayc_r_27873 = pickle.load(handle)
with open('psi_rz_27873.pickle', 'rb') as handle:
    psi_rz_27873 = pickle.load(handle)
with open('efm_psi_axis_27873.pickle', 'rb') as handle:
    efm_psi_axis_27873 = pickle.load(handle)
with open('efm_psi_boundary_27873.pickle', 'rb') as handle:
    efm_psi_boundary_27873 = pickle.load(handle)

with open('psi_r_28819.pickle', 'rb') as handle:
    psi_r_28819 = pickle.load(handle)
with open('psi_r_30417.pickle', 'rb') as handle:
    psi_r_30417 = pickle.load(handle)
with open('psi_rz_28819.pickle', 'rb') as handle:
    psi_rz_28819 = pickle.load(handle)
with open('psi_rz_30417.pickle', 'rb') as handle:
    psi_rz_30417 = pickle.load(handle)

with open('ayc_r_28819.pickle', 'rb') as handle:
    ayc_r_28819 = pickle.load(handle)
with open('ayc_ne_28819.pickle', 'rb') as handle:
    ayc_ne_28819 = pickle.load(handle)
with open('ayc_te_28819.pickle', 'rb') as handle:
    ayc_te_28819 = pickle.load(handle)
with open('ayc_r_30417.pickle', 'rb') as handle:
    ayc_r_30417 = pickle.load(handle)
with open('ayc_ne_30417.pickle', 'rb') as handle:
    ayc_ne_30417 = pickle.load(handle)
with open('ayc_te_30417.pickle', 'rb') as handle:
    ayc_te_30417 = pickle.load(handle)

with open('efm_grid_r_28819.pickle', 'rb') as handle:
    efm_grid_r_28819 = pickle.load(handle)
with open('efm_grid_z_28819.pickle', 'rb') as handle:
    efm_grid_z_28819 = pickle.load(handle)
with open('efm_grid_r_30417.pickle', 'rb') as handle:
    efm_grid_r_30417 = pickle.load(handle)
with open('efm_grid_z_30417.pickle', 'rb') as handle:
    efm_grid_z_30417 = pickle.load(handle)
    
with open('efm_psi_axis_28819.pickle', 'rb') as handle:
    efm_psi_axis_28819 = pickle.load(handle)
with open('efm_psi_boundary_28819.pickle', 'rb') as handle:
    efm_psi_boundary_28819 = pickle.load(handle)
with open('efm_psi_axis_30417.pickle', 'rb') as handle:
    efm_psi_axis_30417 = pickle.load(handle)
with open('efm_psi_boundary_30417.pickle', 'rb') as handle:
    efm_psi_boundary_30417 = pickle.load(handle) 
    
os.chdir('../')
    
###############################################################################
#####    let's declare some arrays

# shot number being considered
shot = 27873
#shot = int(input("select shot number: "))
quant = 'vt'

try:
    # 2-dimensional (r,z) at different times
    # psi as function of radius in m
    psi_x = eval('psi_rz_' + '{}'.format(shot) + "['x']")
    # psi as function of Z in m
    psi_y = eval('psi_rz_' + '{}'.format(shot) + "['y']")
    # psi as function of time in s
    psi_t = eval('psi_rz_' + '{}'.format(shot) + "['time']")
    # value of psi at specific radius, time, and z
    psi_dat = eval('psi_rz_' + '{}'.format(shot) + "['data']")
except(NameError):
    print('no psi data for shot {}'.format(shot))

try:
    # channel number vs radius
    # x is the channel number
    ayc_r_x = eval('ayc_r_' + '{}'.format(shot) + "['x']")
    # t is the time
    ayc_r_t = eval('ayc_r_' + '{}'.format(shot) + "['time']")
    # dat is the radius corresponding to specific channel number at some time t
    ayc_r_dat = eval('ayc_r_' + '{}'.format(shot) + "['data']")
except(NameError):
    print('no ayc_r (TS channel number vs R) data for shot {}'.format(shot))

try:
    # electron temperature data given as a function of time and channel number
    # channel number
    te_x = eval('ayc_te_' + '{}'.format(shot) + "['x']")
    # time
    te_t = eval('ayc_te_' + '{}'.format(shot) + "['time']")
    # T_e at channel number and time
    te_dat = eval('ayc_te_' + '{}'.format(shot) + "['data']")
except(NameError):
    print('no Te data for shot {}'.format(shot))

try:
    # electron density data given as a function of time and channel number
    # channel number
    ne_x = eval('ayc_ne_' + '{}'.format(shot) + "['x']")
    # time
    ne_t = eval('ayc_ne_' + '{}'.format(shot) + "['time']")
    # n_e at channel number and time
    ne_dat = eval('ayc_ne_' + '{}'.format(shot) + "['data']")
except(NameError):
    print('no n_e data for shot {}'.format(shot))

try:
    # ion temperature data given as a function of time and major radius
    # majpr radius (m)
    ti_x = eval('ti_ss_' + '{}'.format(shot) + "['x']")
    # time
    ti_t = eval('ti_ss_' + '{}'.format(shot) + "['time']")
    # T_i at radius and time
    ti_dat = eval('ti_ss_' + '{}'.format(shot) + "['data']")
except(NameError):
    print('no Ti data for shot {}'.format(shot))

try:
    # velocity data given as a function of time and major radius
    # majr radius (m)
    vt_x = eval('vt_ss_' + '{}'.format(shot) + "['x']")
    # time (s)
    vt_t = eval('vt_ss_' + '{}'.format(shot) + "['time']")
    # Vt at radius and time
    vt_dat = eval('vt_ss_' + '{}'.format(shot) + "['data']")
except(NameError):
    print('no Vt data for shot {}'.format(shot))

# magnetic axis and psi boundary
# magnetic axis
try:
    mag_axis = eval('efm_psi_axis_' + '{}'.format(shot) + "['data']")
    mag_axis_tme = eval('efm_psi_axis_' + '{}'.format(shot) + "['time']")
    # psi boundary
    psi_bound = eval('efm_psi_boundary_' + '{}'.format(shot) + "['data']")
    psi_bound_tme = eval('efm_psi_boundary_' + '{}'.format(shot) + "['time']")
except:
    sys.exit('shot number invalid')
    
# choose plasma quantity to pre-process
# ['te', 'ne', 'ti', 'vt']
#quant = 'ne'
#quant = str(input("select quantity (te, ne, ti, vt): "))


# arbitrary value to check slices of data
chk_t = 44
chk_x = 44
# marker size for plotting
mrk = 2

# define units for the plasma quantity
if np.logical_or(quant == 'ti', quant == 'te'):
    units = 'eV'
elif quant == 'ne':
    units = 'm^-3'
elif quant == 'vt':
    units = 'm/s'

# time values, different for t_e, n_e and Vt, t_i
tme = eval(quant + '_t')
# define the array that holds the data of plasma quantity of interest
qdata = eval(quant + '_dat')
# all the data sets have some really nasty maxima that really suck
dat_max = np.nanpercentile(qdata, 95)
#dat_max = np.nanmedian(qdata)

def data_clean(yy=qdata, max_val=dat_max):
    y = np.copy(yy, )
    y[np.where(np.logical_or(y < 0, y > dat_max))] = np.NaN
    good = np.where(np.isnan(y).all(axis=1) == False)[0]
    tme2 = tme[good]
    y2 = y[good]
    return tme2, y2
    
tme, qdata = data_clean(qdata, dat_max)

# there is wobble in the ayc_r_dat that means the channel number as a fnction
# of the radial positon changes with time by a very small amount
# defining psi_rng basically ignores these tiny perturbations
if np.logical_or(quant == 'te', quant == 'ne'):
    psi_rng = np.linspace(np.amin(ayc_r_dat), np.amax(ayc_r_dat), 
                          ayc_r_dat.shape[1])
elif np.logical_or(quant == 'ti', quant == 'vt'):
    psi_rng = ti_x
# the ti and Vt data are 

###############################################################################
#####    useful functions

# finds array index corresponding to array value closest to some value
def find_closest(data, v):
	return (np.abs(data-v)).argmin()

def nan_finder(y):
    return np.isnan(y), lambda z: z.nonzero()[0]

def nan_interp(arr):
    """insert a 2d array with length len(tme)"""
    y = np.copy(arr)
    for i in range(len(tme)):
       nans, x = nan_finder(y[i])
       y[i][nans]= np.interp(x(nans), x(~nans), y[i][~nans])
    return y

###############################################################################
#####    do some stuff

# find the z=0 coordinate
#z0_axis = np.where(efm_grid_z == 0)[0][0]
z0_axis = np.where(psi_y == 0)[0][0]
# define psi only along the z0 axis
psi_dat_z0 = psi_dat[:,z0_axis,:]

###############################################################################
#####    interpolation

# interpolation of psi data so that it corresponds to the same channel number
# and time as the electron temperature data
# perform 2 seperate 1d interpolations. Not ideal but was struggling with 2d
# interpolation. Have some fun trying scikit learn and knn approach :D

# time axis for psi_boundary data needs to be interpolated to coincide with tme
bound_interp = interpolate.interp1d(psi_bound_tme, psi_bound, kind='cubic',
                                    fill_value='extrapolate')
psi_boundary = bound_interp(tme)

# mag axis data interpolated
mag_axis_interp_tmp = interpolate.interp1d(mag_axis_tme, mag_axis,
                                           kind='cubic',
                                           fill_value='extrapolate')
mag_axis_interp = mag_axis_interp_tmp(tme)

def interp_1d():
    psi_t_interp = []
    for i in range(0, len(psi_x)):
        interp_test = interpolate.interp1d(psi_t, psi_dat_z0[:,i],
                                           kind='cubic',
                                           fill_value='extrapolate')
        psi_t_interp.append(interp_test(ayc_r_t))   
    psi_t_interp = np.array(psi_t_interp).T
    # psi_t_interp is psi but with same time values as T_e data
    
    psi_x_interp = []
    for i in range(0, psi_t_interp.shape[0]):
        interp_test = interpolate.interp1d(psi_x, psi_t_interp[i],
                                           kind='cubic',
                                           fill_value='extrapolate')
        psi_x_interp.append(interp_test(ayc_r_dat[i]))  
    psi_x_interp = np.array(psi_x_interp)
    return psi_x_interp

# psi_t_interp is psi but with same channel number values as T_e data
# since the time data is also the same the outputted array should be the
# correct shape
psi_dat_z0_new = interp_1d()

def interp_2d():
    f = interpolate.interp2d(psi_x, psi_t, psi_dat_z0, kind='cubic')
    f_interp = f(psi_rng, tme)
    return f_interp

psi_dat_z0_new2 = interp_2d()

###############################################################################
#####    Normalisation

mag_ax_psi = []
mag_ax = []
norm_ind = []
for i in range(len(tme)):
    a = np.where(psi_dat_z0_new2[i] == np.amax(psi_dat_z0_new2[i]))[0][0]
    #a = find_closest(psi_dat_z0_new2[i], mag_axis_interp[i])
    #print(a-b)
    mag_ax_psi.append(psi_dat_z0_new2[i][a])
    mag_ax.append(psi_dat_z0_new2[i][a])
    norm_ind.append(a)
mag_ax_psi = np.array(mag_ax_psi)
mag_ax_r = np.array(mag_ax)
norm_ind = np.array(norm_ind)
mag_ax_psi = mag_axis_interp

psi_N = []
for i in range(len(tme)):
    psi_N_temp = ( (psi_dat_z0_new2[i] - mag_ax_psi[i]) /
                  (psi_boundary[i] - mag_ax_psi[i]) )
    psi_N_temp[norm_ind[i]:,] = -psi_N_temp[norm_ind[i]:,]
    psi_N.append(-psi_N_temp)
psi_N = np.array(psi_N)

min_psi_N = np.amin(psi_N)
max_psi_N = np.amax(psi_N)

if min_psi_N < -1:
    min_psi_N = -1
if max_psi_N > 1:
    max_psi_N = 1

psi_N_rng = np.linspace(-1, 1, 200)

def psi_reflect(arr):
    #psi_N_new = []
    #arr_new = []
    y2 = []
    for i in range(len(tme)):
        # find where the min psi is and recnstruct psi with opposite sign psi
        ref_pnt = find_closest(psi_N[i], -np.amin(psi_N[i]))
        idx = np.where(psi_N[i] > psi_N[i][ref_pnt])
#        psi_lt0 = np.delete(psi_N[i], idx)
#        arr_lt0 = np.delete(arr[i], idx)
        psi_gt = psi_N[i][idx]
        arr_gt = arr[i][idx]
        psi_rev = -psi_gt[::-1]
        arr_rev = arr_gt[::-1]
        psi_N_new = np.concatenate((psi_rev, psi_N[i]))
        arr_new = np.concatenate((arr_rev, arr[i]))
        f = interpolate.interp1d(psi_N_new, arr_new, kind='linear',
                                 fill_value='extrapolate')
        y2.append(f(psi_N_rng))
        plt.figure()
        plt.plot(psi_N_rng, f(psi_N_rng), 'b-')
        plt.plot(np.amin(psi_N[i]), arr[i][ref_pnt], 'go')
    return y2

###############################################################################
#####    get the same psi values for all Te

def same_psi(arr):   
    y2 = []
    y = nan_interp(arr)
    for i in range(len(tme)):
        f = interpolate.interp1d(psi_N[i], y[i], kind='linear',
                                 fill_value='extrapolate')
        y2.append(f(psi_N_rng))
    return y2

# select either te_dat for electron temp or ne_dat for density

if np.logical_or(quant == 'ti', quant == 'vt'):
    func = psi_reflect(qdata)
    tme, func = data_clean(func, 100)
    func = nan_interp(func)
elif np.logical_or(quant == 'te', quant == 'ne'):
    func = same_psi(qdata)

###############################################################################
#####    suface fitting

x = psi_N_rng
y = tme
X1, Y1 = np.meshgrid(x, y, copy=False)
Z1 = np.array(func).flatten()

deg = 15

###############################################################################
#####    lets try some piecewise fitting huh
    
pcs = 10
tme_pcs = np.array_split(tme, pcs)
func_pcs = np.array_split(np.array(func), pcs, axis=0)

def bivar_polyfit_piece(t_piece, func_piece, deg):
    # psi and time coordinates of the data
    x = psi_N_rng
    y = t_piece
    # gotta meshgrid it so that it forms a nice grid for Te data to sit
    X1, Y1 = np.meshgrid(x, y, copy=False)
    # the data flattened so that its easier to compute on
    Z1 = np.array(func_piece).flatten()
    # gotta flatten the grid too so that coords and Te match up
    X = X1.flatten()
    Y = Y1.flatten()
    # zips the coords together for input into polynoial features function
    aa = np.array(list(zip(X, Y)))
    
    # generates polynomial features (eg: (X**3)*(Y**4)) of any degree
    poly = PolynomialFeatures(deg)
    # associates the aa data with the polynomial feature terms generated
    # by PolynomialFeatures
    X_fit = poly.fit_transform(aa)
    # Lasso uses sparse coefficient solutions
    # LinearRegression uses all coefficients
    # LARS algorithm is piecewise linear as function of norm of coeffs
    # see http://scikit-learn.org/stable/modules/linear_model.html for info
    clf = linear_model.LassoLars(alpha=1e-3)
    # large alpha means most feature coefficients are zero
#    reg_meth = ['LinearRegression', 'Lasso', 'LassoCV', 'LassoLarsCV']
#    clf = eval('linear_model.' + reg_meth[0] + '()')   
    
    # finds optimal polynomial coeffs for the actual data, B
    clf.fit(X_fit, Z1)

    # reshapes and transforms data so that the model predicted values can be
    # determined
    predict_x = np.concatenate((X1.reshape(-1,1), Y1.reshape(-1,1)), axis=1)
    pred_x = poly.fit_transform(predict_x)
    pred_y = clf.predict(pred_x)
    
    #print(poly.powers_)
    
###############################################
#    data = pd.DataFrame.from_dict({
#    'x': np.random.randint(low=1, high=10, size=5),
#    'y': np.random.randint(low=-1, high=1, size=5),
#    })
#    
#    p = PolynomialFeatures(degree=2).fit(data)
#    print p.get_feature_names(data.columns)
#    
#    features = pd.DataFrame(p.transform(data),
#                            columns=p.get_feature_names(data.columns))
#    print(features)
    
    ##########################################
    
    return pred_y.reshape(X1.shape)

fit_pcs = []
for i in range(pcs):
    tmp_fit = abs(bivar_polyfit_piece(tme_pcs[i], func_pcs[i], deg))
    fit_pcs.append(tmp_fit)
qdata_fit = np.concatenate(fit_pcs)

###############################################################################

def fit_stats():
    diff = []
    for i in range(len(tme)):
        for j in range(len(psi_N_rng)):
            diff.append(abs(qdata_fit[i][j] - func[i][j]))
    mean_diff = np.mean(diff)
    print('average of raw data=', np.mean(func))
    print('average of surface fit=', np.mean(qdata_fit))
    print('average difference between', mean_diff)

def compare_contour():
    fig = plt.figure(figsize=(10,6))
    c = 66
    
    ax1 = fig.add_subplot(121)
    cont1 = ax1.contourf(X1, Y1, qdata_fit, c)
    fig.colorbar(cont1, ax=ax1)
    ax1.set_title('fitted {} ({})'.format(quant, units))
    ax1.set_xlabel('$\Psi_{N}$')
    ax1.set_ylabel('time (s)')
    
    ax2 = fig.add_subplot(122)
    cont2 = ax2.contourf(psi_N_rng, tme, func, c)
    fig.colorbar(cont2, ax=ax2)
    ax2.set_title('raw data ({})'.format(units))
    ax2.set_xlabel('$\Psi_{N}$')
compare_contour()

def fit_compare():
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    surf1 = ax1.plot_surface(X1, Y1, qdata_fit, cmap="jet", lw=0.5,
                             rstride=1, cstride=1, alpha=0.9)
    fig.colorbar(surf1, ax=ax1)
    ax2 = fig.add_subplot(122, projection='3d')
    cs = ax2.plot_surface(X1, Y1, func, cmap="jet", lw=0.5, rstride=1, cstride=1)
    fig.colorbar(cs, ax=ax2)
    plt.show()

def fit_compare2():
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.plot_surface(X1, Y1, qdata_fit, cmap="winter", lw=0.5,
                     rstride=1, cstride=1, alpha=0.8)
    ax1.plot_surface(X1, Y1, func, cmap="autumn", lw=0.5,
                     rstride=1, cstride=1, alpha=0.4)
    ax1.set_xlabel('$\Psi_{N}$')
    ax1.set_ylabel('time (s)')
    ax1.set_zlabel('{} ({})'.format(quant, units))
    ax1.grid(False)
    plt.show()
    
def plotly_test():
    import plotly.plotly as py
    import plotly.graph_objs as go
    
    z1 = qdata_fit
    z2 = func
    
    data = [
        go.Surface(z=z1, x=psi_N_rng, y=tme, colorscale='Jet'),
        go.Surface(z=z2, x=psi_N_rng, y=tme, showscale=False, 
                   opacity=0.7, colorscale='autumn'),
    ]
    
    
    layout = go.Layout(
        width=800,
        height=700,
        autosize=False,
        title='{} ({}) fitted with {}th order bivariate polynomial'.format(
                quant, units, deg),
        scene=dict(
            xaxis=dict(
                title = 'Psi_N',
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                title = 'time(s)',
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            zaxis=dict(
                title = '{} ({})'.format(quant, units),
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            aspectratio = dict( x=1, y=1, z=0.7 ),
            aspectmode = 'manual'
        )
    )
    #py.plot(data)
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig)

###############################################################################
#####    plotting

def te_vs_ti_init():
    ti_ss_dat = np.copy(ti_ss_27873['data'])
    ti_ss_dat[np.where(np.logical_or(ti_ss_27873['data'] > 10000,
                                     ti_ss_27873['data'] < 0))] = np.NaN
    
    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    cont1 = ax1.contourf(ti_ss_27873['x'],ti_ss_27873['time'], ti_ss_dat,33)
    ax1.set_xlabel('major radius (m)')
    ax1.set_ylabel('time (s)')
    ax1.set_title('$T_{i}$ (eV)')
    fig.colorbar(cont1, ax=ax1)
    cont2 = ax2.contourf(ayc_te_27873['x'], ayc_te_27873['time'],
                         ayc_te_27873['data'],33)
    ax2.set_xlabel('channel number')
    ax2.set_ylabel('time (s)')
    ax2.set_title('$T_{e}$ (eV)')
    fig.colorbar(cont2, ax=ax2)
    plt.show()

def Te_vs_psiN():
    plt.figure()
    plt.contourf(psi_N_rng, tme, func, 33)
    plt.colorbar()
    plt.xlabel('$\Psi_{N}$')
    plt.ylabel('t (s)')
    plt.title('$T_{e} (eV)$')
    plt.show()
    

def psi_plot(x=chk_x):
    plt.figure()
    plt.plot(tme, psi_dat_z0_new2[:,x], label='$\Psi$ at pos_index {}'
             .format(x))
    plt.plot(tme, mag_axis_interp, label='mag-axis from freia')
    plt.plot(tme, mag_ax_psi, label='mag-axis from code')
    plt.plot(tme, psi_boundary, label='boundary from freia')
    plt.fill_between(tme, mag_ax_psi, psi_boundary, alpha=0.3)
    plt.xlabel('time (s)')
    plt.ylabel('$\Psi$', rotation=0)
    plt.legend(loc='lower left')
    plt.show()

def te_psi():
    plt.figure()
    #plt.plot(psi_sort, T_e_sort)
    #plt.plot(psi_fin[chk], Te_fin[chk], 'r')
    plt.plot(psi_dat_z0_new2[chk_t,:], te_dat[chk_t,:], 'g')
    plt.xlabel('$\Psi$')
    plt.ylabel('$T_{e}$', rotation=0)
    plt.title('for time index {}'.format(chk_t))
    plt.show()

def te_multi_psi(strt=0 , stp=len(tme)-1):     
    plt.figure()
    plt.xlabel('$\Psi$')
    plt.ylabel('$T_{e}$', rotation=0)
    tmp1 = strt
    tmp2 = stp
    plt.title('time: {} to {}'.format(round(tme[tmp1], 3),
              round(tme[tmp2], 3)))
    for i in range(tmp1, tmp2):
        plt.plot(psi_N_rng, func[i])
        #plt.plot(psi_N[i], te_dat[i])
        #plt.plot(psi_peaks[i], Te_peaks[i], 'go')
    plt.show()

def psi_rz(cont_type='contour', chk_t=chk_t, res=33):
    plt.figure()
    if cont_type == 'contour':
        plt.contour(psi_x, psi_y, psi_dat[chk_t,:,:], res)
    elif cont_type == 'contourf':
        plt.contourf(psi_x, psi_y, psi_dat[chk_t,:,:], res)
    else:
        plt.contour(psi_x, psi_y, psi_dat[chk_t,:,:], res)
    #plt.axis('equal')
    plt.colorbar()
    plt.ylabel('z (m)')
    plt.xlabel('radial position (m)')
    plt.title('$\Psi (r,z)$ at t = {}'.format(chk_t))
    plt.show()

def psi_interp_multi():
    plt.figure()
    plt.contourf(psi_dat_z0_new2, 33)
    plt.colorbar()
    plt.xlabel('channel number')
    plt.ylabel('time index')
    plt.title('$\Psi (z=0)$ interpolated (2D interp)')
    
    plt.figure()
    plt.contourf(psi_dat_z0, 33)
    plt.colorbar()
    plt.xlabel('channel number')
    plt.ylabel('time index')
    plt.title('$\Psi (z=0)$')
    
    plt.figure()
    plt.contourf(psi_dat_z0_new, 33)
    plt.colorbar()
    plt.xlabel('channel number')
    plt.ylabel('time index')
    plt.title('$\Psi (z=0)$ interpolated (2 x 1D interp)')
    plt.show()
    
def plot_dict_3d(dict_array):
    arr = dict_array.copy()
    
    x = arr['x']
    t = arr['time']
    X1, Y1 = np.meshgrid(x, t, copy=False)
    Z1 = arr['data'].flatten()
    X = X1.flatten()
    Y = Y1.flatten()
    
    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111, projection='3d')
    surf1 = ax1.plot_surface(X, Y, Z1, cmap="jet", lw=0.5,
                             rstride=1, cstride=1, alpha=0.9)
    fig.colorbar(surf1, ax=ax1)

    plt.show()

###############################################################################
#####    Fancy animations

#os.chdir('./pics')
#for i in range(0, len(tme)):
#    fig = plt.figure()
#    te_multi_psi(i, i+1)
#    print(i)
#    plt.savefig(str(i).zfill(4) +'.png')
#    plt.close(fig)
#os.chdir('../')
#plt.show()