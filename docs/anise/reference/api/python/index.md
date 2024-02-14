# Module `anise`

A Python module implemented in Rust.

    
## Sub-modules

* [anise.anise](#anise.anise)

    
## Classes

    
### Class `Aberration`

>     class Aberration(
>         name
>     )

Represents the aberration correction options in ANISE.

In space science and engineering, accurately pointing instruments (like optical cameras or radio antennas) at a target is crucial. This task is complicated by the finite speed of light, necessitating corrections for the apparent position of the target.

This structure holds parameters for aberration corrections applied to a target's position or state vector. These corrections account for the difference between the target's geometric (true) position and its apparent position as observed.

#### Rule of tumb
In most Earth orbits, one does _not_ need to provide any aberration corrections. Light time to the target is less than one second (the Moon is about one second away).
In near Earth orbits, e.g. inner solar system, preliminary analysis can benefit from enabling unconverged light time correction. Stellar aberration is probably not required.
For deep space missions, preliminary analysis would likely require both light time correction and stellar aberration. Mission planning and operations will definitely need converged light-time calculations.

For more details, <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/abcorr.html>.

#### SPICE Validation

The validation test <code>validate\_jplde\_de440s\_aberration\_lt</code> checks 101,000 pairs of ephemeris computations and shows that the unconverged Light Time computation matches the SPICE computations almost all the time.
More specifically, the 99th percentile of error is less than 5 meters, the 75th percentile is less than one meter, and the median error is less than 2 millimeters.

    
#### Instance variables

    
##### Variable `converged`

Indicates whether the light time calculations should be iterated upon (more precise but three times as many CPU cycles).

    
##### Variable `stellar`

Flag to denote if stellar aberration correction is applied. Stellar aberration is due to the motion of the observer (caused by Earth's orbit around the Sun).

    
##### Variable `transmit_mode`

Specifies whether in reception or transmission mode. True for 'transmit' mode, indicating the correction is applied to the transmitted signal from the observer to the target. False for 'receive' mode, for signals received from the target.

    
### Class `Almanac`

>     class Almanac(
>         path
>     )

An Almanac contains all of the loaded SPICE and ANISE data.

#### Limitations
The stack space required depends on the maximum number of each type that can be loaded.

    
#### Methods

    
##### Method `azimuth_elevation_range_sez`

>     def azimuth_elevation_range_sez(
>         self,
>         /,
>         rx,
>         tx
>     )

Computes the azimuth (in degrees), elevation (in degrees), and range (in kilometers) of the
receiver state (<code>rx</code>) seen from the transmitter state (<code>tx</code>), once converted into the SEZ frame of the transmitter.

###### Algorithm
1. Compute the SEZ (South East Zenith) frame of the transmitter.
2. Rotate the receiver position vector into the transmitter SEZ frame.
3. Rotate the transmitter position vector into that same SEZ frame.
4. Compute the range as the norm of the difference between these two position vectors.
5. Compute the elevation, and ensure it is between +/- 180 degrees.
6. Compute the azimuth with a quadrant check, and ensure it is between 0 and 360 degrees.

    
##### Method `bpc_domain`

>     def bpc_domain(
>         self,
>         /,
>         id
>     )

Returns the applicable domain of the request id, i.e. start and end epoch that the provided id has loaded data.

    
##### Method `bpc_summaries`

>     def bpc_summaries(
>         self,
>         /,
>         id
>     )

Returns a vector of the summaries whose ID matches the desired <code>id</code>, in the order in which they will be used, i.e. in reverse loading order.

    
##### Method `describe`

>     def describe(
>         self,
>         /,
>         spk=None,
>         bpc=None,
>         planetary=None,
>         time_scale=None,
>         round_time=None
>     )

Pretty prints the description of this Almanac, showing everything by default. Default time scale is TDB.
If any parameter is set to true, then nothing other than that will be printed.

    
##### Method `frame_info`

>     def frame_info(
>         self,
>         /,
>         uid
>     )

    
##### Method `load`

>     def load(
>         self,
>         /,
>         path
>     )

Generic function that tries to load the provided path guessing to the file type.

    
##### Method `load_from_metafile`

>     def load_from_metafile(
>         self,
>         /,
>         metafile
>     )

Load from the provided MetaFile, downloading it if necessary.

    
##### Method `spk_domain`

>     def spk_domain(
>         self,
>         /,
>         id
>     )

Returns the applicable domain of the request id, i.e. start and end epoch that the provided id has loaded data.

    
##### Method `spk_summaries`

>     def spk_summaries(
>         self,
>         /,
>         id
>     )

Returns a vector of the summaries whose ID matches the desired <code>id</code>, in the order in which they will be used, i.e. in reverse loading order.

    
##### Method `state_of`

>     def state_of(
>         self,
>         /,
>         object,
>         observer,
>         epoch,
>         ab_corr=None
>     )

Returns the Cartesian state of the object as seen from the provided observer frame (essentially <code>spkezr</code>).

###### Note
The units will be those of the underlying ephemeris data (typically km and km/s)

    
##### Method `sun_angle_deg`

>     def sun_angle_deg(
>         self,
>         /,
>         target_id,
>         observer_id,
>         epoch
>     )

Returns the angle (between 0 and 180 degrees) between the observer and the Sun, and the observer and the target body ID.
This computes the Sun Probe Earth angle (SPE) if the probe is in a loaded SPK, its ID is the "observer_id", and the target is set to its central body.

###### Geometry
If the SPE is greater than 90 degrees, then the celestial object below the probe is in sunlight.

**Sunrise at nadir**
```text
Sun
 |  \      
 |   \
 |    \
 Obs. -- Target
```
**Sun high at nadir**
```text
Sun
 \        
  \  __ θ > 90
   \     \
    Obs. ---------- Target
```

**Sunset at nadir**
```text
         Sun
       /  
      /  __ θ < 90
     /    /
 Obs. -- Target
```

###### Algorithm
1. Compute the position of the Sun as seen from the observer
2. Compute the position of the target as seen from the observer
3. Return the arccosine of the dot product of the norms of these vectors.

    
##### Method `sun_angle_deg_from_frame`

>     def sun_angle_deg_from_frame(
>         self,
>         /,
>         target,
>         observer,
>         epoch
>     )

Convenience function that calls <code>sun\_angle\_deg</code> with the provided frames instead of the ephemeris ID.

    
##### Method `transform`

>     def transform(
>         self,
>         /,
>         target_frame,
>         observer_frame,
>         epoch,
>         ab_corr=None
>     )

Returns the Cartesian state needed to transform the <code>from\_frame</code> to the <code>to\_frame</code>.

###### SPICE Compatibility
This function is the SPICE equivalent of spkezr: <code>spkezr(TARGET\_ID, EPOCH\_TDB\_S, ORIENTATION\_ID, ABERRATION, OBSERVER\_ID)</code>
In ANISE, the TARGET_ID and ORIENTATION are provided in the first argument (TARGET_FRAME), as that frame includes BOTH
the target ID and the orientation of that target. The EPOCH_TDB_S is the epoch in the TDB time system, which is computed
in ANISE using Hifitime. THe ABERRATION is computed by providing the optional Aberration flag. Finally, the OBSERVER
argument is replaced by OBSERVER_FRAME: if the OBSERVER_FRAME argument has the same orientation as the TARGET_FRAME, then this call
will return exactly the same data as the spkerz SPICE call.

###### Note
The units will be those of the underlying ephemeris data (typically km and km/s)

    
##### Method `transform_to`

>     def transform_to(
>         self,
>         /,
>         state,
>         observer_frame,
>         ab_corr=None
>     )

Translates a state with its origin (<code>to\_frame</code>) and given its units (distance_unit, time_unit), returns that state with respect to the requested frame

**WARNING:** This function only performs the translation and no rotation _whatsoever_. Use the <code>transform\_state\_to</code> function instead to include rotations.

    
##### Method `translate`

>     def translate(
>         self,
>         /,
>         target_frame,
>         observer_frame,
>         epoch,
>         ab_corr=None
>     )

Returns the Cartesian state of the target frame as seen from the observer frame at the provided epoch, and optionally given the aberration correction.

###### SPICE Compatibility
This function is the SPICE equivalent of spkezr: <code>spkezr(TARGET\_ID, EPOCH\_TDB\_S, ORIENTATION\_ID, ABERRATION, OBSERVER\_ID)</code>
In ANISE, the TARGET_ID and ORIENTATION are provided in the first argument (TARGET_FRAME), as that frame includes BOTH
the target ID and the orientation of that target. The EPOCH_TDB_S is the epoch in the TDB time system, which is computed
in ANISE using Hifitime. THe ABERRATION is computed by providing the optional Aberration flag. Finally, the OBSERVER
argument is replaced by OBSERVER_FRAME: if the OBSERVER_FRAME argument has the same orientation as the TARGET_FRAME, then this call
will return exactly the same data as the spkerz SPICE call.

###### Warning
This function only performs the translation and no rotation whatsoever. Use the <code>transform</code> function instead to include rotations.

###### Note
This function performs a recursion of no more than twice the [MAX_TREE_DEPTH].

    
##### Method `translate_geometric`

>     def translate_geometric(
>         self,
>         /,
>         target_frame,
>         observer_frame,
>         epoch
>     )

Returns the geometric position vector, velocity vector, and acceleration vector needed to translate the <code>from\_frame</code> to the <code>to\_frame</code>, where the distance is in km, the velocity in km/s, and the acceleration in km/s^2.

    
##### Method `translate_to`

>     def translate_to(
>         self,
>         /,
>         state,
>         observer_frame,
>         ab_corr=None
>     )

Translates the provided Cartesian state into the requested observer frame

**WARNING:** This function only performs the translation and no rotation _whatsoever_. Use the <code>transform\_to</code> function instead to include rotations.

    
### Class `MetaAlmanac`

>     class MetaAlmanac(
>         maybe_path=None
>     )

A structure to set up an Almanac, with automatic downloading, local storage, checksum checking, and more.

#### Behavior
If the URI is a local path, relative or absolute, nothing will be fetched from a remote. Relative paths are relative to the execution folder (i.e. the current working directory).
If the URI is a remote path, the MetaAlmanac will first check if the file exists locally. If it exists, it will check that the CRC32 checksum of this file matches that of the specs.
If it does not match, the file will be downloaded again. If no CRC32 is provided but the file exists, then the MetaAlmanac will fetch the remote file and overwrite the existing file.
The downloaded path will be stored in the "AppData" folder.

    
#### Instance variables

    
##### Variable `files`

Return an attribute of instance, which is of type owner.

    
#### Methods

    
##### Method `dump`

>     def dump(
>         self,
>         /
>     )

Dumps the configured Meta Almanac into a Dhall string.

    
##### Method `latest`

>     def latest()

Returns an Almanac loaded from the latest NAIF data via the <code>default</code> MetaAlmanac.
The MetaAlmanac will download the DE440s.bsp file, the PCK0008.PCA, the full Moon Principal Axis BPC (moon_pa_de440_200625) and the latest high precision Earth kernel from JPL.

###### File list
- <http://public-data.nyxspace.com/anise/de440s.bsp>
- <http://public-data.nyxspace.com/anise/pck08.pca>
- <http://public-data.nyxspace.com/anise/moon_pa_de440_200625.bpc>
- <https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc>

###### Reproducibility

Note that the <code>earth\_latest\_high\_prec.bpc</code> file is regularly updated daily (or so). As such,
if queried at some future time, the Earth rotation parameters may have changed between two queries.

    
##### Method `load`

>     def load(
>         s
>     )

Loads the provided string as a Dhall configuration to build a MetaAlmanac

    
##### Method `process`

>     def process(
>         self,
>         /
>     )

Fetch all of the URIs and return a loaded Almanac

    
### Class `MetaFile`

>     class MetaFile(
>         uri,
>         crc32=None
>     )

    
#### Instance variables

    
##### Variable `crc32`

Optionally specify the CRC32 of this file, which will be checked prior to loading.

    
##### Variable `uri`

URI of this meta file

    
#### Methods

    
##### Method `process`

>     def process(
>         self,
>         /
>     )

Processes this MetaFile by downloading it if it's a URL.

This function modified <code>self</code> and changes the URI to be the path to the downloaded file.

-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
