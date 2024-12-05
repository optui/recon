# LivermorE AI Projector for Computed Tomography

- [Repo](https://github.com/LLNL/LEAP/tree/main)
- [Docs](https://leapct.readthedocs.io/en/latest/)

## Technical Manual

```python
lct = leapct.tomographicModels()
```

### CT Geometry

```python
set_parallelbeam(numAngles, numRows, numCols, pixelHeight, pixelWidth, centerRow, centerCol, phis)
set_fanbeam(numAngles, numRows, numCols, pixelHeight, pixelWidth, centerRow, centerCol, phis, sod, sdd, tau=0.0)
set_conebeam(numAngles, numRows, numCols, pixelHeight, pixelWidth, centerRow, centerCol, phis, sod, sdd, tau=0.0, helicalPitch=0.0)
set_modularbeam(numAngles, numRows, numCols, pixelHeight, pixelWidth, sourcePositions, moduleCenters, rowVectors, colVectors)
```

The helical pitch is in units of mm/radian. One can also set the normalized helical pitch (unitless) with the following function

```python
set_normalizedHelicalPitch(normalized helical pitch).
```

### CT Volume

```python
set_volume(numX, numY, numZ, voxelWidth, voxelHeight, offsetX, offsetY, offsetZ)
set_default_volume()
```

- voxelWidth: voxel size in x & y dimensions (mm)
- voxelHeight: voxel size in z dimension (mm)


### Layout of the Data Arrays

```python
projection_data[iAngle*numRows*numCols + iRow*numCols + iCol]
```

- Projection Data:
  - Number of angles (numAngles)
  - Number of detector rows (numRows)
  - Number of detector columns (numCols)
- iAngle is the angle index
- iRow and iCol are the row and column indices of the detector
- 3D reconstruction volume can be stored in one of two orders:
  - ZYX Order
  - XYZ