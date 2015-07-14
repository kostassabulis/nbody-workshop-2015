"""
A simple example of an animated plot... In 3D!
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib.animation as animation
import random
import colorsys
import matplotlib.cm as cm
import matplotlib.collections as mcollections

def load_bodies(directory_name, unpack=True):
    base_name = "n_body_py.csv."
    data = [[] for x in range(999)]
    for i in range(999):
        file_name = directory_name + base_name + str(i)
        bodies = np.loadtxt(file_name, delimiter=",", skiprows=1, unpack=unpack)
        x, y, z = bodies

        data[i] = bodies

def repack_bodies(bodies):
    return np.transpose(bodies, (0, 2, 1))

import sys
import argparse

class BodyRenderer(object):
    def __init__(self, bodies, line_style="", marker_style=".", color=lambda x: "b", history_length=1, fade=False, only_head=True, fps=15):
        if history_length <= 2 and fade:
            raise ValueError("Can't turn on fading trajectories if history_length is less than 3.")
            
        self.bodies = bodies
        self.line_style = line_style
        self.marker_style = marker_style
        self.drawing_style = self.marker_style + self.line_style
        self.color = color
        self.history_length = history_length
        self.fade = fade
        self.only_head = only_head

        self.fig = plt.figure()
        self.ax = axes3d.Axes3D(self.fig)
        
        self.body_count = data.shape[1]
        self.lines = []

        self._setup_plot()
        self.ani = animation.FuncAnimation(self.fig, self._update, interval=int(1000.0/fps), blit=False)

    def run(self):
        plt.show()

    def _setup_plot(self):
        x_min_max = [np.min(self.bodies[:, :, 0]), np.max(self.bodies[:, :, 0])]
        y_min_max = [np.min(self.bodies[:, :, 1]), np.max(self.bodies[:, :, 1])]
        z_min_max = [np.min(self.bodies[:, :, 2]), np.max(self.bodies[:, :, 2])]

        for min_max in [x_min_max, y_min_max, z_min_max]:
            if min_max[0] == min_max[1]:
                min_max[0] = -0.5
                min_max[1] = 0.5

        self.ax.set_xlim3d(x_min_max)
        self.ax.set_xlabel('x')

        self.ax.set_ylim3d(y_min_max)
        self.ax.set_ylabel('y')

        self.ax.set_zlim3d(z_min_max)
        self.ax.set_zlabel('z')

        color_palette = [self.color(i / float(self.body_count)) for i in range(self.body_count)]
        self.c = color_palette
        mark_every = [-1]
        if not self.only_head:
            mark_every = None

        if self.fade:
            """If trajectories are supposed to fade we need a line object for each time step
               since you can only set a different alpha for one line segment.
            """
            for t in range(self.history_length):
                self.lines.extend([self.ax.plot([], [], [], self.drawing_style, color=color_palette[i], markevery=mark_every)[0] for i in range(self.body_count)])

            if self.only_head:
                for i in range(self.body_count):
                    for t in range(self.history_length - 1):
                        #self.lines[t * self.body_count + i].set_markevery(None)
                        self.lines[t * self.body_count + i].set_marker("")

                    #elf.lines[(self.history_length - 1) * self.body_count + i].set_markevery(mark_every)
                    self.lines[(self.history_length - 1) * self.body_count + i].set_marker(self.marker_style)

        elif self.history_length > 1 or self.history_length <= 0:
            """If we don't need fading trajectories one line object for each body is enough"""
            self.lines.extend([self.ax.plot([], [], [], self.drawing_style, color=color_palette[i], markevery=mark_every)[0] for i in range(self.body_count)])
        else:
            """If we're only observing bodies at one time step at a time, we can do everything
               with just one line object.
            """
            self.lines = self.ax.plot([], [], [], self.drawing_style, color=color_palette[0], markevery=mark_every)[0]

        #return self.lines

    def _get_color(self):
        if isinstance(self.color, str):
            return self.color
        else:
            return self.color(random.random())
            
    def _update(self, num):
        if self.fade:
            if num > 1:
                data_start = max(0, num - self.history_length)
                cur_hist_len = min(self.history_length, num)
                cur_hist_start = self.history_length - cur_hist_len + 2
                for line_t_pos, t in zip(range(cur_hist_start, self.history_length), range(data_start + 2, num)):
                    for i in range(self.body_count):
                        line = self.lines[line_t_pos * self.body_count + i]
                        line.set_data(self.bodies[t - 2 : t, i, 0], self.bodies[t - 2 : t, i, 1])
                        line.set_3d_properties(self.bodies[t - 2 : t, i, 2])

                        if cur_hist_len > 1:
                            line.set_alpha((line_t_pos - cur_hist_start) / float(cur_hist_len))
                        else:
                            line.set_alpha(1.0)
            else:
                for i in range(self.body_count):
                    line = self.lines[(self.history_length - 1) * self.body_count + i]
                    line.set_data([self.bodies[num, i, 0]], [self.bodies[num, i, 1]])
                    line.set_3d_properties([self.bodies[num, i, 2]])
                    line.set_alpha(1.0)
        elif self.history_length > 1 or self.history_length <= 0:
            history_slice = slice(None, num)
            if self.history_length > 1:
                history_slice = slice(max(0, num - self.history_length), num)
            for i, line in enumerate(self.lines):
                line.set_data(self.bodies[history_slice, i, 0], self.bodies[history_slice, i, 1])
                line.set_3d_properties(self.bodies[history_slice, i, 2])
                line.set_alpha(1.0)
        else:
            self.lines.set_data(self.bodies[num, :, 0], self.bodies[num, :, 1])
            self.lines.set_3d_properties(self.bodies[num, :, 2])
            self.lines.set_alpha(1.0)
                
        return self.lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render nbody simulation results.")
    parser.add_argument("directory", help="directory with all of the simulation files in a .csv format")
    parser.add_argument("-c", "--color", type=str, help="specifies in what color to draw the bodies. If not set all bodies are drawn in different colors", choices=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])
    parser.add_argument("-s", "--speed", metavar="fps", type=int, default=30)
    parser.add_argument("-a", "--all", action="store_true", help="includes bodies from all previous time steps, instead of drawing only the current one")
    parser.add_argument("-f", "--fade", metavar="num", type=int, default=0, help="fades out bodies gradually up to the amount specified. Older bodies do not get drawn at all")
    parser.add_argument("-v", "--verbose", action="store_true", help="prints the current frame number to the terminal while drawing")
    
    args = parser.parse_args()
    directory_name = "snapshot/"
    base_name = "n_body_py.csv."
    data = [[] for x in range(999)]
    for i in range(999):
        file_name = directory_name + base_name + str(i)
        bodies = np.loadtxt(file_name, delimiter=",", skiprows=1, unpack=False)
        #x, y, z = bodies

        data[i] = bodies

    data = np.array(data)
    body_renderer = BodyRenderer(data, line_style="-", marker_style=".", history_length=200, fade=True, color=cm.get_cmap())
    body_renderer.run()
    #data = np.array(data)
    #data = np.transpose(data, (2, 1, 0))

    
    sys.exit(0)
