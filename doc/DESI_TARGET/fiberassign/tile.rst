=============
tile_{tileid}
=============

General Description
===================

FITS file with fiber assignments for a given DESI tile.

Naming Convention
-----------------

TBD.  We should group under subdirectories of
$DESI_TARGET/fiberassign/, but the naming for the subdirectories and for the
files themselves is TBD.

Contents
========

====== ================= ======== ===================
Number EXTNAME           Type     Contents           
====== ================= ======== ===================
HDU0_                    IMAGE    Blank
HDU1_  FiberMap          BINTABLE Target assignment for each fiber
HDU2_  PotentialFiberMap BINTABLE All targets that could have been assigned
====== ================= ======== ===================


FITS Header Units
=================

HDU0 (Blank)
------------

HDU1 / FiberMap
---------------

The target assignments for each fiber of this tile.

Required Data Table Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

============= ======= ======== ===================
Name          Type    Units    Description
============= ======= ======== ===================
fiber         int32            fiber id [0-4999]
positioner    int32            label for field   2
numtarget     int32            number of targets that this fiber covers
t_priority    int32            target priority
targetid      int64            selected target ID
desi_target0  int64            TARGETFLAG for that target
ra            float32 deg      Right ascension [degrees]
dec           float32 deg      Declination [degrees]
xfocal_design float32 mm       X location on focal plane [mm]
yfocal_design float32 mm       Y location on focal plane [mm]
============= ======= ======== ===================

Note: we will probably change these to UPPERCASE and adjust some names (e.g. t_priority to PRIORITY)

HDU2 / PotentialFiberMap
------------------------

Required Data Table Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

================= ===== ===== ===================
Name              Type  Units Description
================= ===== ===== ===================
potentialtargetid int64       label for field   1
================= ===== ===== ===================

See DESI-1049 (https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=1049) for
how to interpret this HDU.

Notes and Examples
==================

To do...