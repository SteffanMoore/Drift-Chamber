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

Now that a list of path lengths has been found, all of these values can be mapped onto values in the array, leaving the initial ionisation charge distribution of the generated cosmic ray. An example of this is shown below:

<img src="/readme_pics/Ionised_charges.png" />

### Drift-Diffusion
The final and most important part of the simulation is modelling drift-diffusion of the charges in the chamber. For this we use the drift-diffusion equation in matrix form:

$$ (q^n = {Mq^{n+1}}) $$

Where $(q^n)$ is the current charge distribution, $(q^{n+1})$ is the charge distribution after the next time step and M is tri-diagonal matrix with fringes.

<img src="/readme_pics/Point_charge.png" />

<img src="/readme_pics/drift_diffusion.gif" />
