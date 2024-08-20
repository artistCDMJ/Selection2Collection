Use Ctrl_G in Blender to set your Selected Objects to a New Collection. 

Unfortunately, for now this removes the selected objects from previous collections.
TBD if this is optimal.


Better use is to Use M to move selected to collection in 3d view and Outliner.
The changed space_outliner.py here is a replacement for the original in your scripts folder - this will allow you to select objects and press the New COllection button and it will prompt the same dialog as M and allow to name a new collection and move the objects to it.
