# -*- coding: utf-8 -*-
# @package Converter Cloud Points, Velodyne Veloview (CSV) to Point Cloud Data (PCD) and Viewing Using Open3D
# Web Page
# https://github.com/PARPedraza/VelodyneVeloviewFiles-CSV-to-PCD-and-Viewing
# autors: Alfonso Ramírez-Pedraza and José-Joel González-Barbosa

"""
Example:
        $ python FilesPCD.py -Process
"""

import open3d as o3d
import getopt,os,sys,csv,numpy as np
from pypcd import pypcd
import pprint

class Classification(object):

    def __init__(self,dir):
        """The constructor Initialize Sentinel Data.
        Args:
            self: The object pointer.
            dir (str): destination directory.
        Returns:
            pointer: The object pointer.
        """
        self.dir=dir
        self.exCSV=".csv"
        self.exPCD=".pcd"
        self.folder="/CSV"
        self.nombreArch="/FilesPCD"
        self.root = self.dir + self.folder
        self.NewFolder=self.root+self.nombreArch

    def readCSV(self, file):
        """Read files cloud points csv.
        Args:
            self: The object pointer.
            file (str): path to files cloud points (csv).
        Returns:
            cloud (str): cloud points (x,y,z,d).
        """
        data = pd.read_csv(file)
        cloud = np.array(data)
        return cloud

    def readPCD(self,file):
        # Lee archivos PCD
        cloud = pypcd.PointCloud.from_path(file)
        pprint.pprint(cloud.get_metadata())
        print(cloud.pc_data)
        return cloud

    def Validate(self, dirFolder):
        """Create folder to save object segmentation.
        Args:
            self: The object pointer.
            dirFolder (str): path and name folder to save object segmentation.
        """
        try:
            os.stat(dirFolder)
        except:
            os.mkdir(dirFolder)

    def findFiles(self,flag):
        """Find Files csv or pcd.
        Args:
            self: The object pointer.
            flag (str): process number.
        Returns:
            list_files (str): list files cloud points founded.
        """
        if(flag==1):
            list_files = [f for f in os.listdir(self.root) if f.endswith(self.exCSV)]
            Point.Validate(self.NewFolder)
        else:
            list_files = [f for f in os.listdir(self.root) if f.endswith(self.exPCD)]
        return list_files

    def writePCD(self,file, cloud):
        """Write Files PCD.
        Args:
            self: The object pointer.
            file (str): name file.
            cloud (array): data cloud point.
        Returns:
            clouds (str): save cloud points founded.
        """
        X = cloud[:, 0]
        Y = cloud[:, 1]
        Z = cloud[:, 2]
        data = np.column_stack((X, Y, Z))
        # Use the pypcd utility function to create a new point cloud from ndarray
        new_cloud = pypcd.make_xyz_point_cloud(data)
        #pprint.pprint(new_cloud.get_metadata())
        # Store the cloud uncompressed
        fileName = self.NewFolder +"/" + file[:-4] + self.exPCD
        # new_cloud.save('new_cloud.pcd')
        new_cloud.save_pcd(fileName)

    def readViewing3D(self,file):
        """Viewing Files PCD.
        Args:
            self: The object pointer.
            file (str): name file.
        """
        cloud = o3d.io.read_point_cloud(file)
        # The following code achieves the same effect as:
        # o3d.visualization.draw_geometries([pcd])
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(cloud)
        vis.run()
        vis.destroy_window()

    def iniParam(self,flag):
        """Choose process
        Args:
            self: The object pointer.
            flag (str): process number.
        """
        # Find cloud points
        list_files = Point.findFiles(flag)
        if (flag == 1):
            print("Save PCD Files...")
        else:
            print("Read and Show PCD Files...")
        # Get process on cloud point find on path
        for file in list_files:
            ##Cadena File Name and Path
            fileroot = self.root + "/" + file
            print(fileroot)
            if(flag==1):
               cloud = Point.readCSV(fileroot)
               Point.writePCD(file, cloud)
            else:
               Point.readPCD(fileroot)
               Point.readViewing3D(fileroot)

    def usage(self):
        print(" Opcions:")
        print("--help (-h)")
        print("-r \t<PathFiles csv>\t <Convert cloud points csv to pcd>")
        print("-p \t<PathFiles pcd>\t <Read and show cloud points pcd>")
        sys.exit()

    def main(self, argv):
        try:
            opts, args = getopt.getopt(argv, "rph", ["Path="])
        except getopt.GetoptError:
            Point.usage()
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Point.usage()
            elif opt in ("-r", "--Path"):
                Point.iniParam(1)
            elif opt in ("-p", "--Path"):
                Point.iniParam(2)
            else:
                Point.usage()

if __name__ == "__main__":
    # Variables Input
    dir = os.path.dirname(os.path.abspath(__file__))
    Point = Classification(dir)
    Point.main(sys.argv[1:])
