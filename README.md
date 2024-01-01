# Drift-Chamber
## Explanation
This is a simulation of a drift chamber particle detector, made in my third year of university. It is based on a "multi-wire proportional chamber" from 1968 which was a gas filled box with a cathode on one side and anode wires on the other. When a cosmic ray enters the box, it ionises gas in its path producing electrons and positive ions (although only the electrons are measured in this detector). The electrons then drift towards the anode wires due to the electic field, giving a two dimensional image of the particle path.

<img src="/readme_pics/drift_diffusion.gif" />

## Implementation
### Cosmic Ray Generation
Cosmic ray generation is handled by "modules/ray_generation.py". The starting position of the ray is chosen randomly from any x, y, z coordinate within the detector. The path angle is then decided by calculating a random azimuth angle (angle on the horizontal plane) and a random zenith angle (angle towards the sky). However, while azimuth angle is uniformly distributed (making a standard random number suitable), zenith angle has a cos^2(x) distibution, reaching a maximum from straight above. To accomodate this, the accept/reject method is used to correctly provide a random angle within the distribution.

When "modules/ray_generation.py" is ran as script, it produces histograms of the azimuth and zenith distributions for 1,000,000 generated rays as seen below (the zenith graph has a cos^2(x) guiding line).

Azimuth             |  Zenith
:-------------------------:|:-------------------------:
<img src="/readme_pics/Azimuth.png" />  |  <img src="/readme_pics/Zenith.png" />

### Ionisation
Next the ionisation needs to be represented as a charge distribution within the chamber now that the path is known - this is dealt with by "modules/ionisation.py". A fixed ionisation rate was assumed of 94 electrons per cm travelled. The charge distribution is represented with a 2D numpy array who's size depends on grid spacing. To fill in the array with charges, first the intersections between the path and array x gridlines are found. Each time a new x gridline intersection is found, the program doubles back to check whether any z gridlines are crossed. Once a list of these has been found,the path length between each of these intersections is calculated. Since the distribution is supposed to represent a 3D environment, the path length projected onto the 2D array is multiplied by a constant which depends on how perpendicular to the 2D projection plane the path is.

Now that a list of path lengths has been found, all of these values can be mapped onto values in the array, leaving the initial ionisation charge distribution of the generated cosmic ray. An example of this is shown below which can be obtained by running "modules/ionisation.py" as a script:

<img src="/readme_pics/Ionised_charges.png" />

### Drift-Diffusion
The final and most important part of the simulation is modelling drift-diffusion of the charges in the chamber, the code for which is in "modules/drift_diffusion.py". For this we use the drift-diffusion equation in matrix form:

$$ q^n = {Mq^{n+1}} $$

Where $q^n$ is the current charge distribution, $q^{n+1}$ is the charge distribution after the next time step and $M$ is a tri-diagonal matrix with fringes. This means that to be able to find the next iteration of the charge distribution, we need to find the inverse of the $M$ matrix.

One of the faster ways of doing this is through an LU decomposition using "linalg" in the scipy module, however, $M$ is such a sufficiently large matrix that this operation is too intensive using a standard 2D array. Luckily, since the matrix is diagonal, we can use the inbuilt sparse matrix in scipy to complete the LU decomposition which allows the simulation of the drift-diffusion.

When the "modules/drift_diffusion.py" file is ran as a script, a large point charge is simulated for a duration of 1E-4 seconds and the resulting charge displayed as show below:

<img src="/readme_pics/Point_charge.png" />

### Simulation and animation
When the "simulation.py" file is run, a random cosmic ray is generated and the initial ionisation calculated before putting it through the drift-diffusion for a set number of iterations. Once this has completed, the out put will be an animation of the simulation, which is also saved as a .gif file called "drift_diffusion.gif". An example of this is shown below.

<img src="/readme_pics/drift_diffusion.gif" />
