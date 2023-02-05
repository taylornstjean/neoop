import json
import os
from datetime import datetime as dt
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy.coordinates import EarthLocation, SkyCoord, AltAz
from astropy.time import Time

from config import MPC_NEOCP_URL, DATA_DIR, OBS_COORDS, MIN_ALT, TIME_INCR, OBS_TIME
from neoop.interface import proc_out
from neoop.log import neocp_last_save, neocp_log_save

neocp_json_path = os.path.join(DATA_DIR, "neocp.json")
neocp_npy_path = os.path.join(DATA_DIR, "neocp.npy")


# class objects

class Obs:
    """A simple object that holds all information related to the location of the observatory."""

    latitude = OBS_COORDS["lat"]
    longitude = OBS_COORDS["lon"]
    location = EarthLocation.from_geodetic(lat=latitude * u.degree, lon=longitude * u.degree)

    def lst(self):
        """Calculate local sidereal time at the observatory."""

        proc_out(f"Calculating sidereal time at ({self.longitude}, {self.latitude}).")

        observing_time = Time(dt.utcnow(), scale='utc', location=self.location)
        sidereal = observing_time.sidereal_time('mean')
        return sidereal


def update_neo_data(force=False):
    """Update stored NEO data if necessary.
    :param force: Force update if True. Default is False.
    """

    if not force:
        proc_out("Checking for data validity.")

    lp = neocp_last_save()

    updt_req = bool(dt.utcnow().timestamp() - lp >= 3600) if lp else True

    if not os.path.isfile(neocp_json_path) or bool(updt_req) or force:
        if updt_req:
            proc_out(f"Data is out of date, updating NEOCP data from {MPC_NEOCP_URL}.")
        elif not os.path.isfile(neocp_json_path):
            proc_out(f"File not found, downloading NEOCP data from {MPC_NEOCP_URL}.")
        elif force:
            proc_out(f"Force updating NEOCP data from {MPC_NEOCP_URL}.")

        urlretrieve(MPC_NEOCP_URL, neocp_json_path)

        neocp_log_save()
        proc_out("Finished.")

        with open(neocp_json_path, 'r') as f:
            proc_out("Generating and saving numpy array from data.")
            data = json.load(f)
            for entry in data:
                entry["Vis."] = _is_visible(entry)
            array = np.array(data)

            np.save(neocp_npy_path, array, allow_pickle=True)
    else:
        proc_out("Data is up to date.")


def neocp_array(cols=None):
    """Returns an array with current stored data."""

    try:
        array = np.load(neocp_npy_path, allow_pickle=True)
    except FileNotFoundError:
        update_neo_data(True)
        array = np.load(neocp_npy_path, allow_pickle=True)

    if not cols:
        return array
    else:
        m_array = array
        keys = [key for key in array[0].keys() if key not in cols and key != "Temp_Desig"]
        for entry in m_array:
            for key in keys:
                del entry[key]
        return m_array


# object plotters

def radec_plot(objects=neocp_array(), temp_desig=None):
    """Plot object visibility with respect to the observatory over set time period."""

    if temp_desig:
        ascensions = [obj["R.A."] * u.hourangle for obj in objects if obj["Temp_Desig"] in temp_desig]
        declinations = [obj["Decl."] * u.degree for obj in objects if obj["Temp_Desig"] in temp_desig]

        if len(temp_desig) <= 1:
            obj_desig = temp_desig
        else:
            obj_desig = "NEO"
    else:
        ascensions = [obj["R.A."] * u.hourangle for obj in objects]
        declinations = [obj["Decl."] * u.degree for obj in objects]

        obj_desig = "NEO"

    proc_out(f"Generating right ascension/declination plot for object(s) {temp_desig if temp_desig else 'ALL'}.")

    neo = SkyCoord(ascensions, declinations, frame='icrs', unit=u.deg)
    obs = SkyCoord(Obs().lst(), Obs().latitude, frame="icrs", unit=u.deg)

    # plot using matplotlib

    plt.figure(figsize=(6, 5))

    plt.suptitle(f"{obj_desig} Right Ascension/Declination Plot")

    plt.subplot(111, projection='mollweide')
    plt.grid(True)

    plt.scatter(neo.ra.wrap_at('180d').radian, neo.dec.radian, label=obj_desig)
    plt.scatter(obs.ra.wrap_at('180d').radian, obs.dec.radian, marker="*", label="Observatory")

    plt.xlabel('R.A. [deg]')
    plt.ylabel('Decl. [deg]')
    plt.legend()

    plt.show()


def altaz_plot(objects=neocp_array(), temp_desig=None):
    if temp_desig:
        ascensions = [obj["R.A."] * u.hourangle for obj in objects if obj["Temp_Desig"] in temp_desig]
        declinations = [obj["Decl."] * u.degree for obj in objects if obj["Temp_Desig"] in temp_desig]

        if len(temp_desig) <= 1:
            obj_desig = temp_desig
        else:
            obj_desig = "NEO"
    else:
        ascensions = [obj["R.A."] * u.hourangle for obj in objects]
        declinations = [obj["Decl."] * u.degree for obj in objects]

        obj_desig = "NEO"

    proc_out(f"Generating altitude/azimuth plot for object(s) {temp_desig if temp_desig else 'ALL'}.")

    date = Time(dt.utcnow())
    time_grid = date + np.linspace(0, OBS_TIME, TIME_INCR) * u.hour

    altaz = AltAz(location=Obs().location, obstime=time_grid)

    coords = SkyCoord(ascensions, declinations, frame="icrs", unit=u.deg)

    open_cluster_altaz = coords[:, np.newaxis].transform_to(altaz[np.newaxis])

    # plot using matplotlib

    plt.figure(figsize=(6, 5))

    plt.suptitle(f"{obj_desig} Altitude Viewed from Observatory")

    plt.plot(time_grid.datetime, open_cluster_altaz[:].alt.degree.T, marker='', alpha=0.5)

    plt.axhline(MIN_ALT, zorder=-10, linestyle='--', color='tab:red')

    plt.xlabel('Date/Time [UTC mm-dd hh]')
    plt.ylabel('Altitude [deg]')

    plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=45)
    plt.tight_layout()

    plt.show()


# data validity checks

def is_neo(temp_desig, objects=neocp_array()):
    exist = bool(temp_desig in [obj["Temp_Desig"] for obj in objects])
    return exist


def _is_visible(obj):
    ascension = obj["R.A."] * u.hourangle
    declination = obj["Decl."] * u.degree
    date = Time(dt.utcnow())

    altaz = AltAz(location=Obs().location, obstime=date)
    radec = SkyCoord(ascension, declination, frame="icrs", unit=u.deg)
    obj_obs = radec.transform_to(altaz)

    obj_vis = "YES" if bool(obj_obs.alt >= MIN_ALT * u.degree) else "NO"

    return obj_vis
