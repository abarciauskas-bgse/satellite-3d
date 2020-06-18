# Create COG from ICESat-2 HDF

```bash
pdal pipeline atl08-hdf-to-tif.json --readers.hdf.f
lename=ATL08_20181023230252_03870102_003_01_xyz_conf.h5 --w
iters.gdal.filename=output.tif
rio cogeo create output.tif output_cog.tif
```

