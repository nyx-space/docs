# Frame Safety and Graph Lookups

In space mission design, one of the most common sources of error is the misuse of reference frames. Forgetting to rotate from a body-fixed frame to an inertial frame, or confusing two different inertial frames (like J2000 and EME2000), can lead to mission-critical failures.

ANISE introduces the concept of **Frame Safety** to eliminate these errors.

## Frames are Not Just IDs

In the SPICE toolkit, frames are often referred to by integer IDs. While ANISE maintains compatibility with NAIF IDs, it treats Frames as rich objects. 

Every Frame in ANISE has a type and a relationship to other frames:
- **Celestial**: Inertial frames like J2000 / ICRF.
- **Planetocentric**: Body-fixed frames like ITRF93 (Earth) or IAU_MOON.
- **Topocentric**: Frames defined at a specific location on a body's surface (e.g., SEZ frame at a tracking station).

## Validation Before Computation

When you request a transformation in ANISE, the toolkit doesn't just blindly multiply matrices. It performs a **Frame Check**.

Before any computation:
1. ANISE checks that the target and observer frames are part of the same "graph" (they have a path between them).
2. It ensures the transformation is physically valid (e.g., you aren't trying to rotate between two frames that don't have a defined orientation relationship).
3. It identifies the "Common Ancestor"—the point in the frame tree where the paths from the two frames meet.

## Tree Traversal and Path Finding

ANISE represents the relationship between frames as a directed acyclic graph (DAG), but for most practical purposes, it behaves like a tree. 

When transforming from Frame A to Frame B:
- **Translation Path**: Finds the common ephemeris ancestor (e.g., the Solar System Barycenter) and sums the vectors along the branches.
- **Rotation Path**: Finds the common orientation ancestor and composes the Direction Cosine Matrices (DCMs) or Quaternions.

If a path cannot be found (e.g., you haven't loaded the necessary FK or PCK files), ANISE returns a clear error at the start of the query, rather than producing junk data or crashing with a segfault.

## The `Frame` Object

In the ANISE API, a `Frame` object carries its metadata with it. When you build an `Orbit`, it is attached to a specific `Frame`. When you transform that `Orbit` to a new frame, ANISE uses the metadata to ensure the transformation is accurate, including handling the necessary time conversions for body-fixed rotations.
