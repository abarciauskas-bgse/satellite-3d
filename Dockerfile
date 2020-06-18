FROM remotepixel/amazonlinux-gdal:2.4.1

WORKDIR /tmp

ENV PACKAGE_PREFIX /tmp/python

COPY setup.py setup.py
COPY satellite_3d/ satellite_3d/

# Install dependencies
RUN pip3 install cython==0.28
RUN pip3 install . --no-binary numpy,rasterio -t $PACKAGE_PREFIX -U
RUN pip3 install . --no-binary h5py,vtzero -t $PACKAGE_PREFIX -U

