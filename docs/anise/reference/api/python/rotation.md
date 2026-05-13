---
description: |
    API documentation for modules: anise.rotation.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...

    
# Module `anise.rotation` {#anise.rotation}

    
## Classes

    
### Class `DCM` {#anise.rotation.DCM}

>     class DCM(
>         np_rot_mat,
>         from_id,
>         to_id,
>         np_rot_mat_dt=None
>     )

Defines a direction cosine matrix from one frame ID to another frame ID, optionally with its time derivative.
It provides a number of run-time checks that prevent invalid rotations.

:type np_rot_mat: numpy.array
:type from_id: int
:type to_id: int
:type np_rot_mat_dt: numpy.array, optional
:rtype: DCM

    
#### Instance variables

    
##### Variable `from_id` {#anise.rotation.DCM.from_id}

:rtype: int

    
##### Variable `rot_mat` {#anise.rotation.DCM.rot_mat}

Return the position DCM (3x3 matrix)
:rtype: numpy.ndarray

    
##### Variable `rot_mat_dt` {#anise.rotation.DCM.rot_mat_dt}

Return the time derivative of this DMC, if set.
:rtype: numpy.ndarray

    
##### Variable `to_id` {#anise.rotation.DCM.to_id}

:rtype: int

    
#### Methods

    
##### Method `angular_velocity_deg_s` {#anise.rotation.DCM.angular_velocity_deg_s}

>     def angular_velocity_deg_s(
>         self,
>         /
>     )

Returns the angular velocity vector in deg/s if a rotation rate is defined.
:rtype: np.array

    
##### Method `angular_velocity_rad_s` {#anise.rotation.DCM.angular_velocity_rad_s}

>     def angular_velocity_rad_s(
>         self,
>         /
>     )

Returns the angular velocity vector in rad/s of this DCM is it has a defined rotation rate.
:rtype: np.array

    
##### Method `from_align_and_clock` {#anise.rotation.DCM.from_align_and_clock}

>     def from_align_and_clock(
>         primary_body_axis,
>         primary_inertial_vec,
>         secondary_body_axis,
>         secondary_inertial_vec,
>         from_id,
>         to_id
>     )

Constructs a DCM using the "Align and Clock" (Two-Vector Targeting / TRIAD) method.

This defines a rotation based on two geometric constraints:
1. **Align**: The <code>primary\_body\_axis</code> is aligned exactly with the <code>primary\_inertial\_vec</code>.
2. **Clock**: The <code>secondary\_body\_axis</code> is aligned as closely as possible with the <code>secondary\_inertial\_vec</code>.

This constructs the rotation matrix $R_{from \to to}$.

##### Arguments
* <code>primary\_body\_axis</code> - The axis in the "from" frame to align (e.g. Sensor Boresight).
* <code>primary\_inertial\_vec</code> - The target vector in the "to" frame (e.g. Vector to Earth).
* <code>secondary\_body\_axis</code> - The axis in the "from" frame to clock (e.g. Solar Panel Normal).
* <code>secondary\_inertial\_vec</code> - The target vector in the "to" frame (e.g. Vector to Sun).
* <code>from</code> - The ID of the source frame.
* <code>to</code> - The ID of the destination frame.

:type primary_body_axis: np.array
:type primary_inertial_vec: np.array
:type secondary_body_axis: np.array
:type secondary_inertial_vec: np.array
:type from_id: int
:type to_id: int
:rtype: DCM

    
##### Method `from_identity` {#anise.rotation.DCM.from_identity}

>     def from_identity(
>         from_id,
>         to_id
>     )

Builds an identity rotation.

:type from_id: int
:type to_id: int
:rtype: DCM

    
##### Method `from_r1` {#anise.rotation.DCM.from_r1}

>     def from_r1(
>         angle_rad,
>         from_id,
>         to_id
>     )

Returns a rotation matrix for a rotation about the X axis.

Source: <code>euler1</code> function from Baslisk

:type angle_rad: float
:type from_id: int
:type to_id: int
:rtype: DCM

    
##### Method `from_r2` {#anise.rotation.DCM.from_r2}

>     def from_r2(
>         angle_rad,
>         from_id,
>         to_id
>     )

Returns a rotation matrix for a rotation about the Y axis.

Source: <code>euler2</code> function from Basilisk

:type angle_rad: float
:type from_id: int
:type to_id: int
:rtype: DCM

    
##### Method `from_r3` {#anise.rotation.DCM.from_r3}

>     def from_r3(
>         angle_rad,
>         from_id,
>         to_id
>     )

Returns a rotation matrix for a rotation about the Z axis.

Source: <code>euler3</code> function from Basilisk

:type angle_rad: float
:type from_id: int
:type to_id: int
:rtype: DCM

    
##### Method `get_state_dcm` {#anise.rotation.DCM.get_state_dcm}

>     def get_state_dcm(
>         self,
>         /
>     )

Returns the 6x6 DCM to rotate a state. If the time derivative of this DCM is defined, this 6x6 accounts for the transport theorem.
Warning: you MUST manually install numpy to call this function.
:rtype: numpy.ndarray

    
##### Method `is_identity` {#anise.rotation.DCM.is_identity}

>     def is_identity(
>         self,
>         /
>     )

Returns whether this rotation is identity, checking first the frames and then the rotation matrix (but ignores its time derivative)

:rtype: bool

    
##### Method `is_valid` {#anise.rotation.DCM.is_valid}

>     def is_valid(
>         self,
>         /,
>         unit_tol,
>         det_tol
>     )

Returns whether the <code>rot\_mat</code> of this DCM is a valid rotation matrix.
The criteria for validity are:
-- The columns of the matrix are unit vectors, within a specified tolerance (unit_tol).
-- The determinant of the matrix formed by unitizing the columns of the input matrix is 1, within a specified tolerance. This criterion ensures that the columns of the matrix are nearly orthogonal, and that they form a right-handed basis (det_tol).
[Source: SPICE's rotation.req](https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/rotation.html#Validating%20a%20rotation%20matrix)

:type unit_tol: float
:type det_tol: float
:rtype: bool

    
##### Method `skew_symmetric` {#anise.rotation.DCM.skew_symmetric}

>     def skew_symmetric(
>         self,
>         /
>     )

Returns the skew symmetric matrix if this DCM defines a rotation rate.
:rtype: np.array

    
##### Method `to_quaternion` {#anise.rotation.DCM.to_quaternion}

>     def to_quaternion(
>         self,
>         /
>     )

:rtype: Quaternion

    
##### Method `transpose` {#anise.rotation.DCM.transpose}

>     def transpose(
>         self,
>         /
>     )

Returns the transpose of this DCM

:rtype: DCM

    
### Class `Quaternion` {#anise.rotation.Quaternion}

>     class Quaternion(
>         w,
>         x,
>         y,
>         z,
>         from_id,
>         to_id
>     )

Represents the orientation of a rigid body or a coordinate frame transformation in three-dimensional space using Euler parameters.

Euler parameters, also known as unit quaternions, are a set of four parameters <code>w</code>, <code>x</code>, <code>y</code>, <code>z</code>.
They are particularly useful because they avoid gimbal lock, are more compact than rotation matrices,
and allow for smooth interpolation (SLERP).

### Conventions

ANISE strictly adheres to the following conventions to ensure consistency with <code>[DCM](#anise.rotation.DCM "anise.rotation.DCM")</code> and standard
Guidance, Navigation, and Control (GNC) mathematics:

1. **Hamiltonian Algebra:** The quaternion multiplication follows the right-handed rule where \
   `i * j = k`. This is the standard in robotics and computer graphics, but distinct from the
   "JPL/Shuster" convention (`i * j = -k`) sometimes found in legacy aerospace software.

2. **Passive Rotation (Coordinate Transformation):** A quaternion defined with `from: A` and `to: B`
   represents the transformation of **coordinates** from Frame A to Frame B.
   * The rotation of a vector <code>v</code> is computed as: `v_B = q.conjugate() * v_A * q`.
   * This matches the behavior of a Direction Cosine Matrix (DCM): `v_B = [DCM_A->B] * v_A`.

3. **Operator Composition (Backward Chaining):** Rotations are composed in "Operator Order",
   matching matrix multiplication rules.
   * To compute the rotation A -> C, you multiply B->C by A->B.
   * `q_A_to_C = q_B_to_C * q_A_to_B`
   * ANISE enforces strict frame checking: <code>LHS.from</code> must equal <code>RHS.to</code>.

### Definitions

Euler parameters are defined in terms of the principal rotation vector. If a frame is rotated
by an angle <code>θ</code> about a unit axis `e = [e1, e2, e3]`:

* `w = cos(θ / 2)`
* `x = e1 * sin(θ / 2)`
* `y = e2 * sin(θ / 2)`
* `z = e3 * sin(θ / 2)`

These parameters satisfy `w^2 + x^2 + y^2 + z^2 = 1`, which means they represent
a rotation in SO(3) and can be used to interpolate rotations smoothly.

### Applications

In the context of spacecraft mechanics, Euler parameters are often used because they provide a
numerically stable way to represent the attitude of a spacecraft without the singularities that
are present with Euler angles.

### Usage
Importantly, ANISE prevents the composition of two Euler Parameters if the frames do not match.

:type w: float
:type x: float
:type y: float
:type z: float
:type from_id: int
:type to_id: int

    
#### Instance variables

    
##### Variable `from_id` {#anise.rotation.Quaternion.from_id}

:rtype: int

    
##### Variable `to_id` {#anise.rotation.Quaternion.to_id}

:rtype: int

    
##### Variable `w` {#anise.rotation.Quaternion.w}

:rtype: float

    
##### Variable `x` {#anise.rotation.Quaternion.x}

:rtype: float

    
##### Variable `y` {#anise.rotation.Quaternion.y}

:rtype: float

    
##### Variable `z` {#anise.rotation.Quaternion.z}

:rtype: float

    
#### Methods

    
##### Method `about_x` {#anise.rotation.Quaternion.about_x}

>     def about_x(
>         angle_rad,
>         from_id,
>         to_id
>     )

Creates an Euler Parameter representing the short way rotation about the X (R1) axis

:type angle_rad: float
:type from_id: int
:type to_id: int
:rtype: Quaternion

    
##### Method `about_y` {#anise.rotation.Quaternion.about_y}

>     def about_y(
>         angle_rad,
>         from_id,
>         to_id
>     )

Creates an Euler Parameter representing the short way rotation about the Y (R2) axis

:type angle_rad: float
:type from_id: int
:type to_id: int
:rtype: Quaternion

    
##### Method `about_z` {#anise.rotation.Quaternion.about_z}

>     def about_z(
>         angle_rad,
>         from_id,
>         to_id
>     )

Creates an Euler Parameter representing the short way rotation about the Z (R3) axis

:type angle_rad: float
:type from_id: int
:type to_id: int
:rtype: Quaternion

    
##### Method `as_vector` {#anise.rotation.Quaternion.as_vector}

>     def as_vector(
>         self,
>         /
>     )

Returns the data of this EP as a vector.
:rtype: np.array

    
##### Method `b_matrix` {#anise.rotation.Quaternion.b_matrix}

>     def b_matrix(
>         self,
>         /
>     )

Returns the 4x3 matrix which relates the body angular velocity vector w to the derivative of this Euler Parameter.
dQ/dt = 1/2 [B(Q)] w

:rtype: np.array

    
##### Method `conjugate` {#anise.rotation.Quaternion.conjugate}

>     def conjugate(
>         self,
>         /
>     )

Compute the conjugate of the quaternion.

##### Note
Because Euler Parameters are unit quaternions, the inverse and the conjugate are identical.

:rtype: Quaternion

    
##### Method `derivative` {#anise.rotation.Quaternion.derivative}

>     def derivative(
>         self,
>         /,
>         omega_rad_s
>     )

Returns the euler parameter derivative for this EP and the body angular velocity vector w
dQ/dt = 1/2 [B(Q)] omega_rad_s

:type omega_rad_s: np.array
:rtype: Quaternion

    
##### Method `is_zero` {#anise.rotation.Quaternion.is_zero}

>     def is_zero(
>         self,
>         /
>     )

Returns true if the quaternion represents a rotation of zero radians

:rtype: bool

    
##### Method `normalize` {#anise.rotation.Quaternion.normalize}

>     def normalize(
>         self,
>         /
>     )

Normalize the quaternion.

:rtype: Quaternion

    
##### Method `prv` {#anise.rotation.Quaternion.prv}

>     def prv(
>         self,
>         /
>     )

Returns the principal rotation vector representation of this Euler Parameter
:rtype: np.array

    
##### Method `scalar_norm` {#anise.rotation.Quaternion.scalar_norm}

>     def scalar_norm(
>         self,
>         /
>     )

Returns the norm of this Euler Parameter as a scalar.

:rtype: float

    
##### Method `short` {#anise.rotation.Quaternion.short}

>     def short(
>         self,
>         /
>     )

Returns the short way rotation of this quaternion

:rtype: Quaternion

    
##### Method `to_dcm` {#anise.rotation.Quaternion.to_dcm}

>     def to_dcm(
>         self,
>         /
>     )

Convert this quaterion to a DCM
:rtype: DCM

    
##### Method `uvec_angle_rad` {#anise.rotation.Quaternion.uvec_angle_rad}

>     def uvec_angle_rad(
>         self,
>         /
>     )

Returns the principal line of rotation (a unit vector) and the angle of rotation in radians

:rtype: tuple

-----
Generated by *pdoc* 0.11.6 (<https://pdoc3.github.io>).
