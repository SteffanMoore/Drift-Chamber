from modules.drift_diffusion import simulate_chamber
from modules.ionisation import initial_ionisation
import matplotlib.pyplot as plt
import matplotlib.animation as animate

def main():
    run_simulation((0.5, 1, 0.3), 0.001, (1E-5, 1E-7))


def run_simulation(detector_length, grid_spacing, times):
    """
    Takes detector length in meters as (x_length, y_length, z_length), grid spacing and times as (time_limit, timestep)
    and performs a simulation of the detection chamber for a randomly generated cosmic ray. This is then plotted as an animation
    and saved as drift_diffusion.gif and shown to the user.
    """

    initial_charge_distribution = initial_ionisation(detector_length, grid_spacing)
    array_list = simulate_chamber(initial_charge_distribution, detector_length, grid_spacing, times)
    plot_and_save_gif(array_list, times[0], times[1])


def plot_and_save_gif(array_list, time_limit, timestep):
    """
    Animates a list of arrays provided as an argument.
    """

    figure = plt.figure()
    charge = plt.imshow(array_list[0], animated = True)
    global frame
    frame = 0


    def next_frame(*args):
        """
        Returns the next frame in the animation for FuncAnimation.
        """

        global frame
        if frame < int(time_limit/timestep):
            frame += 1
        else:
            frame = 0
        charge.set_array(array_list[frame])

        return charge


    animation = animate.FuncAnimation(figure, next_frame, frames = array_list, interval = 10)
    writergif = animate.PillowWriter(fps = 30) 
    animation.save('drift_diffusion.gif', writer = writergif)
    plt.show() 
    plt.close()


if __name__ == "__main__":
    main()