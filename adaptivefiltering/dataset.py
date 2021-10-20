from adaptivefiltering.asprs import asprs
from adaptivefiltering.paths import locate_file, get_temporary_filename
from adaptivefiltering.utils import AdaptiveFilteringError

import json
import os
import shutil
import sys


class DataSet:
    def __init__(self, filename=None, provenance=[], spatial_reference=None):
        """The main class that represents a Lidar data set.

        :param filename:
            Filename to load the dataset from. The dataset is expected to be in LAS/LAZ 1.2-1.4 format.
            If an absolute filename is given, the dataset is loaded from that location. Relative paths
            are interpreted (in this order) with respect to the directory set with :func:`~adaptivefiltering.set_data_directory`,
            the current working directory, XDG data directories (Unix only) and the Python package
            installation directory.
            Will give a warning if too many data points are present.
        :type filename: str
        :param spatial_reference:
            A spatial reference in WKT. This will override the reference system found in the metadata
            and is required if no reference system is present in the metadata of the LAS/LAZ file.
            If this parameter is not provided, this information is extracted from the metadata.
        :type spatial_reference: str
        """
        # Initialize a cache data structure for rasterization operations on this data set
        self._mesh_data_cache = {}

        # Store the given parameters
        self._provenance = provenance
        self.filename = filename
        self.spatial_reference = spatial_reference

        # Make the path absolute
        if self.filename is not None:
            self.filename = locate_file(self.filename)

    def save_mesh(
        self,
        filename,
        resolution=2.0,
        classification=asprs[:],
    ):
        """Store the point cloud as a digital terrain model to a GeoTIFF file

        It is important to note that for archaelogic applications, the mesh is not
        a traditional DEM/DTM (Digitial Elevation/Terrain Model), but rather a DFM
        (Digital Feature Model) which consists of ground and all potentially relevant
        structures like buildings etc. but always excludes vegetation.

        :param filename:
            The filename to store the mesh. You can either specify an absolute path
            or a relative path. Relative paths are interpreted w.r.t. the current
            working directory.
        :type filename: str
        :param resolution:
            The mesh resolution in meters. Adapt this depending on the scale
            of the features you are looking for and the point density of your
            Lidar data.
        :type resolution: float
        :param classification:
            The classification values to include into the written mesh file.
        :type classification: tuple
        """
        from adaptivefiltering.pdal import PDALInMemoryDataSet

        dataset = PDALInMemoryDataSet.convert(self)
        return dataset.save_mesh(
            filename, resolution=resolution, classification=classification
        )

    def show_mesh(self, resolution=2.0, classification=asprs[:]):
        """Visualize the point cloud as a digital terrain model in JupyterLab

        It is important to note that for archaelogic applications, the mesh is not
        a traditional DEM/DTM (Digitial Elevation/Terrain Model), but rather a DFM
        (Digital Feature Model) which consists of ground and all potentially relevant
        structures like buildings etc. but always excludes vegetation.

        :param resolution:
            The mesh resolution in meters. Adapt this depending on the scale
            of the features you are looking for and the point density of your
            Lidar data.
        :type resolution: float
        :param classification:
            The classification values to include into the visualization
        :type classification: tuple
        """
        from adaptivefiltering.pdal import PDALInMemoryDataSet

        dataset = PDALInMemoryDataSet.convert(self)
        return dataset.show_mesh(resolution=resolution, classification=classification)

    def show_points(self, threshold=750000, classification=asprs[:]):
        """Visualize the point cloud in Jupyter notebook
        Will give a warning if too many data points are present.
        Non-operational if called outside of Jupyter Notebook.

        :param classification:
            The classification values to include into the visualization
        :type classification: tuple
        """
        from adaptivefiltering.pdal import PDALInMemoryDataSet

        dataset = PDALInMemoryDataSet.convert(self)
        return dataset.show_points(threshold=threshold, classification=classification)

    def show_hillshade(self, resolution=2.0, classification=asprs[:]):
        """Visualize the point cloud as hillshade model in Jupyter notebook

        :param resolution:
            The mesh resolution to use for the visualization in meters.
        :type resolution: float
        :param classification:
            The classification values to include into the visualization
        :type classification: tuple"""
        from adaptivefiltering.pdal import PDALInMemoryDataSet

        dataset = PDALInMemoryDataSet.convert(self)
        return dataset.show_hillshade(
            resolution=resolution, classification=classification
        )

    def show_slope(self, resolution=2.0, classification=asprs[:]):
        """Visualize the point cloud as slope model in Jupyter notebook.

        :param resolution:
            The mesh resolution to use for the visualization in meters.
        :type resolution: float
        :param classification:
            The classification values to include into the visualization
        :type classification: tuple"""
        from adaptivefiltering.pdal import PDALInMemoryDataSet

        dataset = PDALInMemoryDataSet.convert(self)
        return dataset.show_slope(resolution=resolution, classification=classification)

    def save(self, filename, compress=False, overwrite=False):
        """Store the dataset as a new LAS/LAZ file

        This writes this instance of the data set to an LAS/LAZ file which will
        permanently store the ground point classification. The resulting file will
        also contain the point data from the original data set.

        :param filename:
            Where to store the new LAS/LAZ file. You can either specify an absolute path
            or a relative path. Relative paths are interpreted w.r.t. the current
            working directory.
        :type filename: str
        :param compress:
            If true, an LAZ file will be written instead of an LAS file.
        :type compress: bool
        :param overwrite:
            If this parameter is false and the specified filename does already exist,
            an error is thrown. This is done in order to prevent accidental corruption
            of valueable data files.
        :type overwrite: bool
        :return:
            A dataset object wrapping the written file
        :rtype: adaptivefiltering.DataSet
        """
        # If the filenames match, this is a no-op operation
        if filename == self.filename:
            return self

        # Otherwise, we can simply copy the file to the new location
        # after checking that we are not accidentally overriding something
        if not overwrite and os.path.exists(filename):
            raise AdaptiveFilteringError(
                f"Would overwrite file '{filename}'. Set overwrite=True to proceed"
            )

        # Do the copy operation
        shutil.copy(self.filename, filename)

        # And return a DataSet instance
        return DataSet(
            filename=filename,
            provenance=self._provenance,
            spatial_reference=self.spatial_reference,
        )

    def restrict(self, segmentation=None):
        """Restrict the data set to a spatial subset

        :param segmentation:
        :type: adaptivefiltering.segmentation.Segmentation

        """
        from adaptivefiltering.pdal import PDALInMemoryDataSet

        dataset = PDALInMemoryDataSet.convert(self)

        return dataset.restrict(segmentation)

    def provenance(self, stream=sys.stdout):
        """Report the provence of this data set

        For the given data set instance, report the input data and filter
        sequence (incl. filter settings) that procuced this data set. This
        can be used to make good filtering results achieved while using the
        package reproducible.

        :param stream:
            The stream to write the results to. Defaults to stdout, but
            could also e.g. be a file stream.
        """

        stream.write("Provenance report generated by adaptivefiltering:\n\n")
        for i, entry in self._provenance:
            stream.write(f"Item #{i}:\n")
            stream.write(f"{entry}\n\n")

    @classmethod
    def convert(cls, dataset):
        """Convert this dataset to an instance of DataSet"""
        return dataset.save(get_temporary_filename(extension="las"))


def remove_classification(dataset):
    """Remove the classification values from a Lidar dataset

    Instead, all points will be classified as 1 (unclassified). This is useful
    to drop an automatic preclassification in order to create an archaelogically
    relevant classification from scratch.

    :param dataset:
        The dataset to remove the classification from
    :type dataset: adaptivefiltering.Dataset
    :return:
        A transformed dataset with unclassified points
    :rtype: adaptivefiltering.DataSet
    """
    from adaptivefiltering.pdal import PDALInMemoryDataSet, execute_pdal_pipeline

    dataset = PDALInMemoryDataSet.convert(dataset)
    pipeline = execute_pdal_pipeline(
        dataset=dataset,
        config={"type": "filters.assign", "value": ["Classification = 1"]},
    )

    return PDALInMemoryDataSet(
        pipeline=pipeline,
        provenance=dataset._provenance + ["Removed all point classifications"],
        spatial_reference=dataset.spatial_reference,
    )


def reproject_dataset(dataset, out_srs, in_srs=None):
    """
    Standalone function to reproject a given dataset with the option of forcing an input reference system

    :param out_srs: The desired output format in WKT.
    :type out_srs: str

    :param in_srs: The input format in WKT from which to convert. The default is the dataset's current reference system.
    :type in_srs: str

    :return: A reprojected dataset
    :rtype: adaptivefiltering.DataSet
    """
    from adaptivefiltering.pdal import execute_pdal_pipeline
    from adaptivefiltering.pdal import PDALInMemoryDataSet

    dataset = PDALInMemoryDataSet.convert(dataset)
    if in_srs is None:
        in_srs = dataset.spatial_reference

    config = {
        "type": "filters.reprojection",
        "in_srs": in_srs,
        "out_srs": out_srs,
    }
    pipeline = execute_pdal_pipeline(dataset=dataset, config=config)
    spatial_reference = json.loads(pipeline.metadata)["metadata"][
        "filters.reprojection"
    ]["comp_spatialreference"]
    return PDALInMemoryDataSet(
        pipeline=pipeline,
        provenance=dataset._provenance
        + [f"Converted the dataset to spatial reference system '{out_srs}'"],
        spatial_reference=spatial_reference,
    )
