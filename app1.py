from scipy import *
from pyvtk import *
import numpy as np
from pyvtk.DataSetAttr import *


class Cubefile:
    def __init__(self, filename):
        """Represents a Gaussian03 cubefile object.

        Attributes:
            data -- a scipy array containing the data
            numAtoms -- the number of atoms
            origin -- the origin
            numPoints -- a list of the number of points in x,y,z
            spacing -- a list of the spacing in x,y,z
        """

        self.readCubeFile(filename)

    def readCubeFile(self, filename):
        """Read in a cube file."""

        inputfile = open(filename, "r")
        header = "".join([inputfile.readline(), inputfile.readline()])

        temp = inputfile.readline().strip().split()
        self.numAtoms = int(temp[0])
        self.origin = list(map(float, temp[1:]))

        self.numPoints = [0] * 3
        self.spacing = [0] * 3
        for i in range(3):
            line = inputfile.readline().strip().split()
            self.numPoints[i] = int(line[0])
            temp = list(map(float, line[1:]))
            self.spacing[i] = temp[i]
            assert sum(temp[:i] + temp[i + 1:]) == 0

        # Read in the lines with atom data
        for i in range(self.numAtoms):
            line = inputfile.readline()

        self.data = np.zeros((self.numPoints[1], self.numPoints[0], self.numPoints[2]), "float")
        i = j = k = 0
        while i < self.numPoints[1]:
            line = next(inputfile)
            temp = list(map(float, line.strip().split()))
            for x in range(0, len(temp)):
                self.data[j, i, x + k] = temp[x]

            k += len(temp)
            if k == self.numPoints[2]:
                j += 1
                k = 0
                if j == self.numPoints[1]:
                    i += 1
                    j = 0

        inputfile.close()


if __name__ == "__main__":
    t = Cubefile("sub_rho_0_1_120.cub")
    # To visualise with MayaVi
    # Pass t.data.flat thru vtkpython

    ranges = [0] * 3
    ranges[0] = t.origin[0] + np.arange(t.numPoints[0]) * t.spacing[0]
    ranges[1] = t.origin[1] + np.arange(t.numPoints[1]) * t.spacing[1]
    ranges[2] = t.origin[2] + np.arange(t.numPoints[2]) * t.spacing[2]
    for i in range(3):
        print(len(ranges[i]), t.numPoints[i])
    v = VtkData(RectilinearGrid(ranges[2], ranges[0], ranges[1]), "Cube file", PointData(Scalars(t.data.flat)))
    outputfile = open("sub_rho_0_1_120.vtk", "wb")
    outputfile.write(v.to_string())
    outputfile.close()