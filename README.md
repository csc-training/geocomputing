# geocomputing
Examples for doing spatial analysis in CSC computing environment with:
* [Python](python)
* [R](R)

Examples include also batch job scripts suitable for Taito.
Some of the examples include samples for serial, array and parallel jobs.

If you are interested in setting up cloud environments for GIS see:
- cPouta virtual machines we have some [cPouta GIS examples and instructions](./pouta)
- running containers in [Rahti Containers platform](./rahti)


# Scripts

You can download these scripts to **Puhti** or somewhere else with git. You should first navigate to the destination folder, in Puhti your project's **projappl** or **scratch** folder:

`cd /projappl/<YOUR-PROJECT>`
or
`cd /scratch/<YOUR-PROJECT>`

And then clone this repository there

`git clone https://github.com/csc-training/geocomputing.git`

# License
These examples are free to use with CC 4.0 BY oGIIR license. In your publications please acknowledge oGIIR, for example “The authors wish to acknowledge for instructions CSC – IT Center for Science, Finland (urn:nbn:fi:research-infras-2016072531) and the Open Geospatial Information Infrastructure for Research (oGIIR, urn:nbn:fi:research-infras-2016072513).”


# Rahti container cloud

Rahti is used to host web services or any sort of containers. Notebooks are perhaps the most commonly hosted GIS application but you can also host e.g. Geoserver or a database (with some caveats).

* [Rahti web user interface](https://rahti.csc.fi:8443/)
* [Rahti container registry](https://registry-console.rahti.csc.fi/)
* [Rahti documentation](https://docs.csc.fi/cloud/rahti/)
