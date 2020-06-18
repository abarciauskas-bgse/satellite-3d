"""Skeleton of a handler."""

from typing import Tuple
from rio_tiler.io import cogeo
import numpy
import h5py
from vtzero.tile import VectorTile, Tile, Layer, Point, Polygon

from lambda_proxy.proxy import API

APP = API(name="satellite-3d")

@APP.route(
    "/<int:z>/<int:x>/<int:y>.pbf",
    methods=["GET"],
    cors=True,
    payload_compression_method="gzip",
    binary_b64encode=True,
)
def main(
    z: int,
    x: int,
    y: int,
    tilesize: int = 128,
    feature_type: str = "polygon"
) -> Tuple:
    """Handle tile requests."""
    #address = f"https://elevation-tiles-prod.s3.amazonaws.com/geotiff/{z}/{x}/{y}.tif"
    #tile, mask = cogeo.tile(address, x, y, z, tilesize=tilesize)
    #indexes = numpy.where(mask)

    filename = 'ATL08_20181023230252_03870102_003_01.h5'
    hdf_file = h5py.File(filename, 'r')
    tracks = ['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']
    track = tracks[0]

    # Best available DEM (in priority of Arctic/Antarctic/GMTED/MSS) value at the geolocation point. Height is in meters above the WGS84 Ellipsoid.
    # Source https://nsidc.org/sites/nsidc.org/files/technical-references/ICESat2_ATL08_data_dict_v003.pdf
    data_variable = 'land_segments/dem_h'
    latitude_variable = 'land_segments/latitude'
    longitude_variable = 'land_segments/longitude'


    latitudes = hdf_file[f'{track}/{latitude_variable}']
    longitudes = hdf_file[f'{track}/{longitude_variable}']
    data = hdf_file[f'{track}/{data_variable}']

    # Create MVT
    tile = Tile()

    # Add a layer
    layer = Layer(tile, 'dem_h'.encode())

    # Add a point
    #for idx in range(len(data)):
    sc = 25
    points = 10
    for xidx in range(points):
        for yidx in range(points):
            x, y = xidx, yidx
            x *= sc
            y *= sc
            #feature = Point(layer)
            #feature.add_point(x + sc / 2, y - sc / 2)

            feature = Polygon(layer)
            feature.add_ring(5)
            feature.set_point(x, y)
            feature.set_point(x + sc, y)
            feature.set_point(x + sc, y - sc)
            feature.set_point(x, y - sc)
            feature.set_point(x, y)
            # not sure this is correct x, y
            dem_h = str(data[xidx+yidx]).encode()
            # print(f'dem_h: {dem_h}')
            feature.add_property('dem_h'.encode(), dem_h)
            feature.commit()

    # Encode mvt
    data = tile.serialize()
    return (
        "OK",
        "application/x-protobuf",
        data
    )

