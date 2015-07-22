"""Simulation display functionality
"""

import util
import sys
import time
import argparse
import pickle

import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.collections as mcollections


class SnapshotRenderer(object):
    def __init__(self, bodies, blocking=False, line_style="", marker_style=".", color=lambda x: "b", 
                 history_length=1, fade=False, only_head=True, fps=15, bounds=None, verbose=0):
        if history_length <= 2 and fade:
            raise ValueError("Can't turn on fading trajectories if history_length is less than 3.")

        self._bodies = bodies
        self._blocking = blocking
        self._line_style = line_style
        self._marker_style = marker_style
        self._drawing_style = self._marker_style + self._line_style
        self._color = color
        self._history_length = history_length
        self._fade = fade
        self._only_head = only_head
        self._fps = fps
        self._bounds = bounds
        self._verbose = verbose

        self._fig = plt.figure()
        self._ax = axes3d.Axes3D(self._fig)
        
        self._body_count = bodies.shape[1]
        self._time_steps = None
        if not self._blocking:
            self._time_steps = bodies.shape[0]
        else:
            plt.ion()
            self._num = 0          

        self._lines = []

        self._setup_plot()
        self._ani = None
        if not self._blocking:
            self._ani = animation.FuncAnimation(self._fig, self._update, self._time_steps,
                                                interval=int(1000.0/fps), blit=False, repeat_delay=2000)

    def run(self, out_file=None, updated_data=None):
        if self._blocking and updated_data is None:
            raise ValueError("If renderer is set to blocking mode you have to pass in updates for each frame")

        if not self._blocking:
            if out_file:
                Writer = animation.writers['ffmpeg']
                writer = Writer(fps=self._fps, metadata=dict(artist='Me'), bitrate=1800)
                self._ani.save(out_file, writer=writer)
            else:
                plt.show()
        else:
            if out_file:
                raise NotImplementedError("Can't save to file in interactive mode")
            else:
                self._bodies = updated_data
                self._update_lines(self._num)
                self._ax.figure.canvas.draw()
                self._fig.show()
                plt.pause(0.001)

            self._num += 1

    @classmethod
    def for_clusters(cls, snapshot_storage, **kwargs):
        return cls(snapshot_storage, line_style="", marker_style=".", history_length=1, fade=False, **kwargs)

    @classmethod
    def for_orbits(cls, snapshot_storage, **kwargs):
        return cls(line_style="-", marker_style=".", history_length=0, fade=False, color=cm.get_cmap(), **kwargs)

    @classmethod
    def for_cluster_trajectories(cls, snapshot_storage, **kwargs):
        return cls(snapshot_storage, line_style="", marker_style=".", history_length=0, fade=False, **kwargs)

    def _setup_plot(self):
        x_min_max, y_min_max, z_min_max = None, None, None

        if not self._bounds:
            x_min_max = [np.min(self._bodies[:, :, 0]), np.max(self._bodies[:, :, 0])]
            y_min_max = [np.min(self._bodies[:, :, 1]), np.max(self._bodies[:, :, 1])]
            z_min_max = [np.min(self._bodies[:, :, 2]), np.max(self._bodies[:, :, 2])]
            for min_max in [x_min_max, y_min_max, z_min_max]:
                if min_max[0] == min_max[1]:
                    min_max[0] = -0.5
                    min_max[1] = 0.5
        else:
            if len(self._bounds) == 3:
                x_min_max, y_min_max, z_min_max = self._bounds
            elif len(self._bounds) == 2:
                x_min_max, y_min_max, z_min_max = self._bounds, self._bounds, self._bounds
            else:
                raise ValueError("Bounds len should be either 2 (min and max) or 3 (min and max for each dim)")

        self._ax.set_xlim3d(x_min_max)
        self._ax.set_xlabel('x')

        self._ax.set_ylim3d(y_min_max)
        self._ax.set_ylabel('y')

        self._ax.set_zlim3d(z_min_max)
        self._ax.set_zlabel('z')

        color_palette = [self._color(i / float(self._body_count)) for i in range(self._body_count)]
        self._c = color_palette
        mark_every = [-1]
        if not self._only_head:
            mark_every = None

        if self._fade:
            """If trajectories are supposed to fade we need a line object for each time step
               since you can only set a different alpha for one line segment.
            """
            for t in range(self._history_length):
                self._lines.extend([self._ax.plot([], [], [], self._drawing_style, 
                                    color=color_palette[i], 
                                    markevery=mark_every)[0] for i in range(self._body_count)])

            if self._only_head:
                for i in range(self._body_count):
                    for t in range(self._history_length - 1):
                        self._lines[t * self._body_count + i].set_marker("")

                    self._lines[(self._history_length - 1) * self._body_count + i].set_marker(self._marker_style)

        elif self._history_length > 1 or self._history_length <= 0:
            """If we don't need fading trajectories one line object for each body is enough"""
            self._lines.extend([self._ax.plot([], [], [], self._drawing_style, 
                                color=color_palette[i], markevery=mark_every)[0] for i in range(self._body_count)])
        else:
            """If we're only observing bodies at one time step at a time, we can do everything
               with just one line object.
            """
            self._lines = self._ax.plot([], [], [], self._marker_style, color=color_palette[0])[0]

        #return self._lines

    def _get_color(self):
        if isinstance(self._color, str):
            return self._color
        else:
            return self._color(random.random())

    def _update_lines(self, num):
        if self._fade:
            if num > 1:
                data_start = max(0, num - self._history_length)
                cur_hist_len = min(self._history_length, num)
                cur_hist_start = self._history_length - cur_hist_len + 2
                for line_t_pos, t in zip(range(cur_hist_start, self._history_length), 
                                         range(data_start + 2, num)):
                    for i in range(self._body_count):
                        line = self._lines[line_t_pos * self._body_count + i]
                        line.set_data(self._bodies[t - 2 : t, i, 0], self._bodies[t - 2 : t, i, 1])
                        line.set_3d_properties(self._bodies[t - 2 : t, i, 2])

                        if cur_hist_len > 1:
                            line.set_alpha((line_t_pos - cur_hist_start) / float(cur_hist_len))
                        else:
                            line.set_alpha(1.0)
            else:
                for i in range(self._body_count):
                    line = self._lines[(self._history_length - 1) * self._body_count + i]
                    line.set_data([self._bodies[num, i, 0]], [self._bodies[num, i, 1]])
                    line.set_3d_properties([self._bodies[num, i, 2]])
                    line.set_alpha(1.0)
        elif self._history_length > 1 or self._history_length <= 0:
            history_slice = slice(None, num)
            if self._history_length > 1:
                history_slice = slice(max(0, num - self._history_length), num)
            for i, line in enumerate(self._lines):
                line.set_data(self._bodies[history_slice, i, 0], self._bodies[history_slice, i, 1])
                line.set_3d_properties(self._bodies[history_slice, i, 2])
                line.set_alpha(1.0)
        else:
            self._lines.set_data(self._bodies[num, :, 0], self._bodies[num, :, 1])
            self._lines.set_3d_properties(self._bodies[num, :, 2])
            self._lines.set_alpha(1.0)

    def _update(self, num):
        if self._verbose:
            if self._verbose == 1:
                sys.stdout.write(".")
                sys.stdout.flush()
                if num == self._bodies.shape[0] - 1:
                    print ""
            elif self._verbose == 2:
                print "{}/{}".format(num, self._bodies.shape[0])

        self._update_lines(num)

        return self._lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render nbody simulation results.")
    parser.add_argument("directory", help="directory with all of the simulation files in a .csv format, or a pickled snapshot file")
    parser.add_argument("-c", "--color", type=str, help="specifies in what color to draw the bodies. If not set all bodies are drawn in different colors", choices=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])
    parser.add_argument("-s", "--speed", metavar="fps", type=int, default=20)
    parser.add_argument("-t", "--timesteps", metavar="num", type=int, default=1, help="displays previous body states up to the amount specified. Set to 0 to display all states")
    parser.add_argument("-f", "--fade", action="store_true", help="specifies whether bodies from previous time steps should fade")
    parser.add_argument("-o", "--out", metavar="path", type=str, help="if specified will output video to file")
    parser.add_argument("-v", "--verbose", action="store_true", help="prints the current frame number to the terminal while drawing")
    
    args = parser.parse_args()
    
    bodies = None
    if args.directory.endswith(".pkl"):
        bodies = pickle.load(args.directory)
    else:
        bodies = util.load_snapshots(args.directory)

    color = cm.get_cmap()
    if args.color:
        color = args.color

    verbose_level = 1
    if args.verbose:
        verbose_level = 2

    body_renderer = SnapshotRenderer(bodies, line_style="-", marker_style=".", 
                                     history_length=args.timesteps, fade=args.fade, 
                                     color=color, fps=args.speed, verbose=verbose_level)
    body_renderer.run(out_file=args.out)
    
    sys.exit(0)
