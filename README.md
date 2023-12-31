# Drift-Chamber
## Explanation
This is a simulation of a drift chamber particle detector, made in my third year of university. It is based on a "multi-wire proportional chamber" from 1968 which was a gas filled box with a cathode on one side and anode wires on the other. When a cosmic ray enters the box, it ionises gas in its path producing electrons and positive ions (although only the electrons are measured in this detector). The electrons then drift towards the anode wires due to the electic field, giving a two dimensional image of the particle path.

<img src="/drift_diffusion.gif" />

## Implementation
### Cosmic Ray Generation
Cosmic ray generation is handled by "modules/ray_generation.py". The starting position of the ray is chosen randomly from any x, y, z coordinate within the detector. The path angle is then decided by calculating a random azimuth angle (angle on the horizontal plane) and a random zenith angle (angle towards the sky). However, while azimuth angle is uniformly distributed (making a standard random number suitable), zenith angle has a cos^2(x) distibution, reaching a maximum from straight above. To accomodate this, the accept/reject method is used to correctly provide a random angle within the distribution.

When "modules/ray_generation.py" is ran as script, it produces histograms of the azimuth and zenith distributions (the zenith graph has a cos^2(x) guiding line).

Azimuth             |  Zenith
:-------------------------:|:-------------------------:
<img src="/Azimuth.png" />  |  <img src="/Zenith.png" />

### Ionisation
Next the ionisation needs to be shown within the chamber now that the path is known. A fixed ionisation rate was assumed of 

### Drift-Diffusion
