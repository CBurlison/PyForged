# Forged game port in python

This project is a WIP of my WIP game Forged which is being worked on in Godot .Net. It is a learning project in an attempt to improve my python skill set.

## Current Status
The "game" as it was is still in the framework process. Since pygame is extremely bare bones I am working on creating a dynamic framework. As it stands it is EXTREMELY similar to that of Godot's since that is where my experience comes from. 

The features I have implemented are:

1. A node tree
   - The top level node which is the system's entry point for all other nodes.
2. DI and Node Factory
   - A Dependency Injection design using a Node factory to utalize the DI, instantiate node specific fields, and run said node's instantiation.
3. Draw order base on node tree
4. An input event handler
5. The following nodes:
   - Buttons
     - Buttons include toggle butttons and button groups.
   - Sprites
   - Animated Sprites
   - Text Labels
6. A scene manager that can add nodes at specific node paths or directly replace the child nodes of the top level "SceneNode".
