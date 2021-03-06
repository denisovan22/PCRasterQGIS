# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsDataSourceUri,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber)
from qgis import processing
from pcraster import *


class PCRasterInversedistanceAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_MASK = 'INPUT'
    INPUT_POINTS = 'INPUT2'
    INPUT_IDP = 'INPUT3'
    INPUT_RADIUS = 'INPUT4'
    INPUT_MAXNR = 'INPUT5'
    OUTPUT_INVERSEDISTANCE = 'OUTPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PCRasterInversedistanceAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'inversedistance'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('inversedistance')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('PCRaster')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'pcraster'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Interpolate values using inverse distance weighing (IDW).")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input DEM.
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_MASK,
                self.tr('Mask layer')
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_POINTS,
                self.tr('Raster layer with values to be interpolated')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_IDP,
                self.tr('Power'),
                defaultValue=2
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_RADIUS,
                self.tr('Radius. 0 includes all points.'),
                defaultValue=0
            )
        )
        
        self.addParameter(
            QgsProcessingParameterNumber(
                self.INPUT_MAXNR,
                self.tr('Maximum number of closest points. 0 includes all points.'),
                defaultValue=0
            )
        )


        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_INVERSEDISTANCE,
                self.tr('Inverse Distance Interpolation output')
            )
        )
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        input_mask = self.parameterAsRasterLayer(parameters, self.INPUT_MASK, context)
        input_points = self.parameterAsRasterLayer(parameters, self.INPUT_POINTS, context)
        input_idp = self.parameterAsDouble(parameters, self.INPUT_IDP, context)
        input_radius = self.parameterAsDouble(parameters, self.INPUT_RADIUS, context)
        input_maxnr = self.parameterAsDouble(parameters, self.INPUT_MAXNR, context)
        output_idw = self.parameterAsRasterLayer(parameters, self.OUTPUT_INVERSEDISTANCE, context)
        setclone(input_mask.dataProvider().dataSourceUri())
        MaskLayer = readmap(input_mask.dataProvider().dataSourceUri())
        PointsLayer = readmap(input_points.dataProvider().dataSourceUri())
        IDW = inversedistance(MaskLayer,PointsLayer,input_idp,input_radius,input_maxnr)
        outputFilePath = self.parameterAsOutputLayer(parameters, self.OUTPUT_INVERSEDISTANCE, context)
        report(IDW,outputFilePath)

        results = {}
        results[self.OUTPUT_INVERSEDISTANCE] = output_idw
        
        return results
