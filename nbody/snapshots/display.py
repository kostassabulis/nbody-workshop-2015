"""Simulation display functionality
"""

import util
import sys
import time
import argparse
import cPickle

import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.collections as mcollections


class SnapshotRenderer(object):
    """Class for drawing and animating snapshots using matplotlib

    Displays snapshots taken from a SnapshotStorage either directly to screen,
    or to video.

    Args:
        snapshot_storage: The SnapshotStorage class object that contains the
            drawable snapshots. It can be passed in empty, as long as It
            will be filled up before drawing begins.
        line_style: The type of connector between the same object in different
            points in time. Uses the same syntax as matplotlib ("", "-", "--",
            ".-" and etc.)
        marker_style: The type of marker to use for drawing objects. Uses the
            same syntax as matplitlib (".", "o", "v" and etc.)
        color: A function used for generating colors for objects. You can use
            something like this to get a constant color for all objects:
            lambda x: "r".
        history_length: How many previous points will be drawn.
            Most useful when a line_style is specified, to observe object
            trajectories. 1 means that only the current time point will be drawn.
            Use 0 or less to denote that all time points (up to the current one)
            should be drawn.
        fade: If True, trajectories will fade over time. WARNING: This will make
            drawing super slow.
        only_head: When set to True, and history length is specified, only
            the current time point will get a marker, everything else will be 
            drawn purely as specified by the line_style. Use False if you want
            to see exactly where each point is at all time steps.
        fps: How many frames per second to render the animation at. Only useful
            when saving to a file.
        bounds: Sets the figures maximum boundaries. Specify either one list
            (ex: [-1e12, 1e12]), or a list for each dimension
            (ex: [[-1e12, 1e12], [-1e12, 1e12] [-1e12, 1e12]])
        verbose: Specifies how much information to output to the terminal.
            0 is off.
            1 will get you a dot for each rendered frame.
            2 will write out the frame number.

        Example:
            This example loads a snapshot storage and draws it out to the screen
            as an animation:
            >>> storage = SnapshotStorage()
            >>> storage.load("some_file.pkl")
            >>> renderer = SnapshotRenderer.for_clusters(storage)
            >>> renderer.run()

            If you want to save a video to file (currently only mp4 videos are
            supported), do this:
            >>> renderer.run("file_name.mp4")

            If you prefer to render each frame separately (useful for displaying
            results immediatly as they arrive from an integrator), do this:
            >>> storage = SnapshotStorage()
            >>> for snapshot in snapshots:
            >>>     storage.append(snapshot) 
            >>>     renderer.display_step()
            Notice that you can only call display_step() the number of times
            equal to how many snapshots you have. Either load all snapshots and
            pay attention to how many you loaded, or just call display_step 
            after each time you append a snapshot to the associated storage.
    """
    def __init__(self, snapshot_storage, line_style="", marker_style=".", color=None, recoloring_func=None,
                 history_length=1, fade=False, only_head=True, fps=15, bounds=None, verbose=0, angle=None):
        if history_length <= 2 and fade:
            raise ValueError("Can't turn on fading trajectories if history_length is less than 3.")

        self._color = color
        if color is None:
            self._color = lambda x: "b"
        elif color is not None and recoloring_func is not None:
            raise ValueError("Can't have both color and recoloring_func specified at the same time.")

        self._snapshot_storage = snapshot_storage
        self._line_style = line_style
        self._marker_style = marker_style
        self._drawing_style = self._marker_style + self._line_style
        
        self._recoloring_func = recoloring_func
        self._history_length = history_length
        self._fade = fade
        self._only_head = only_head
        self._fps = fps
        self._bounds = bounds
        self._verbose = verbose
        self._angle = angle

        self._drawing_ready = False
        self._animation_ready = False
        if self._snapshot_storage and self._snapshot_storage.snapshot_count:
            self._drawing_ready = True
            self._setup_plot(snapshot_storage.snapshot_shape[0])


    def run(self, out_file=None):
        """ Runs the whole animation, drawing all snapshots in sequence

        Don't forget to add ALL the snapshot you want to draw to the associated
        SnapshotStorage.

        Args:
            out_file: If this is None, everything will be displayed on screen.
                Otherwise, if a mp4 output file is specified, a video will be
                saved
        """
        if not self._snapshot_storage.snapshot_count:
            raise RuntimeError("The supplied SnapshotStorage is empty.")

        if not self._drawing_ready:
            self._setup_plot(self._snapshot_storage.snapshot_count, self._snapshot_storage.snapshot_shape[0])
            self._drawing_ready = True

        if not self._animation_ready:
            self._ani = animation.FuncAnimation(self._fig, self._update, self._snapshot_storage.snapshot_count,
                                                interval=int(1000.0/self._fps), blit=False, repeat=False)
            self._animation_ready = True

        if out_file:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=self._fps, metadata=dict(artist='Me'), bitrate=5000)
            self._ani.save(out_file, writer=writer)
        else:
            plt.show()

    def display_step(self):
        """ Displays one frame from the screen

        A SnapshotStorage doesn't have to be full before calling this, but make
        sure it doesn't run out of snapshots when you keep calling it.
        """
        if not self._snapshot_storage.snapshot_count:
            raise RuntimeError("The supplied SnapshotStorage is empty.")

        if not self._drawing_ready: 
            self._setup_plot(self._snapshot_storage.snapshot_count, self._snapshot_storage.snapshot_shape[0])
            self._drawing_ready = True
            plt.ion()

        if self._num >= self._snapshot_storage.snapshot_count:
            raise RuntimeError("Tried drawing more snapshots than were added to your SnapshotStorage.")

        self._update_lines(self._num, self._snapshot_storage.snapshots)
        self._ax.figure.canvas.draw()
        self._fig.show()
        plt.pause(0.001)

        self._num += 1
            
    @classmethod
    def for_clusters(cls, snapshot_storage, **kwargs):
        """ Initializes a SnapshotRenderer object for viewing clusters
        """
        kwargs.setdefault("line_style", "")
        kwargs.setdefault("marker_style", ".")
        kwargs.setdefault("history_length", 0)
        kwargs.setdefault("fade", False)
        return cls(snapshot_storage, **kwargs)

    @classmethod
    def for_orbits(cls, snapshot_storage, **kwargs):
        """ Initializes a SnapshotRenderer object for viewing orbis 
        """
        kwargs.setdefault("line_style", "-")
        kwargs.setdefault("marker_style", ".")
        kwargs.setdefault("history_length", 2)
        kwargs.setdefault("fade", False)
        kwargs.setdefault("color", cm.get_cmap())
        return cls(snapshot_storage, **kwargs)

    @classmethod
    def for_cluster_trajectories(cls, snapshot_storage, **kwargs):
        """ Initializes a SnapshotRenderer object for viewing trajectories

        This is very similar to the one used for clusters, only it draws
        trajectories.
        """
        kwargs.setdefault("line_style", "")
        kwargs.setdefault("marker_style", ".")
        kwargs.setdefault("history_length", 0)
        kwargs.setdefault("fade", False)
        return cls(snapshot_storage, **kwargs)

    def _setup_plot(self, body_count):
        self._body_count = body_count

        self._fig = plt.figure()
        self._ax = axes3d.Axes3D(self._fig)
        
        self._lines = []

        x_min_max, y_min_max, z_min_max = None, None, None

        if not self._bounds:
            snapshots = self._snapshot_storage.snapshots[:, :, :3]
            x_min_max = [np.min(snapshots[:, :, 0]), np.max(snapshots[:, :, 0])]
            y_min_max = [np.min(snapshots[:, :, 1]), np.max(snapshots[:, :, 1])]
            z_min_max = [np.min(snapshots[:, :, 2]), np.max(snapshots[:, :, 2])]
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

        if self._angle is not None:
            if not isinstance(self._angle, list):
                self._elevation = self._angle
                self._azimuth = 0
            else:
                if len(self._angle) == 2:
                    self._elevation = self._angle[0]
                    self._azimuth = self._angle[1]
                if len(self._angle) != 2:
                    raise ValueError("Angle must contain only 2 values for elevation and azimuth or just elevation.")
        else:
            self._elevation = None
            self._azimuth = None

        self._ax.set_xlim3d(x_min_max)
        self._ax.set_xlabel('x')

        self._ax.set_ylim3d(y_min_max)
        self._ax.set_ylabel('y')

        self._ax.set_zlim3d(z_min_max)
        self._ax.set_zlabel('z')

        self._ax.view_init(elev=self._elevation, azim=self._azimuth)

        color_palette = None
        if self._color is not None:
            if callable(self._color):
                color_palette = [self._color(i / float(self._body_count)) for i in range(self._body_count)]
            else:
                color_palette = self._color
            
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

        self._num = 0 
        #return self._lines

    def _get_color(self):
        if isinstance(self._color, str):
            return self._color
        else:
            return self._color(np.random.random())

    def _update_lines(self, num, bodies):
        if bodies.ndim == 3 and num >= bodies.shape[0]:
            raise IndexError("Trying to draw an out of range time step.")
    
        if self._recoloring_func is not None:
            colors = None
            if bodies.ndim == 3:
                colors = self._recoloring_func(bodies, num)
            elif bodies.ndim == 2:
                colors = self._recoloring_func(bodies[np.newaxis, :], 0)

        if self._fade:
            if num > 1:
                data_start = max(0, num - self._history_length)
                cur_hist_len = min(self._history_length, num)
                cur_hist_start = self._history_length - cur_hist_len + 2
                for line_t_pos, t in zip(range(cur_hist_start, self._history_length), 
                                         range(data_start + 2, num)):
                    for i in range(self._body_count):
                        line = self._lines[line_t_pos * self._body_count + i]
                        line.set_data(bodies[t - 2 : t, i, 0], bodies[t - 2 : t, i, 1])
                        line.set_3d_properties(bodies[t - 2 : t, i, 2])
                        if self._recoloring_func is not None:
                            line.set_color(colors[i])

                        if cur_hist_len > 1:
                            line.set_alpha((line_t_pos - cur_hist_start) / float(cur_hist_len))
                        else:
                            line.set_alpha(1.0)
            else:
                for i in range(self._body_count):
                    line = self._lines[(self._history_length - 1) * self._body_count + i]
                    line.set_data([bodies[num, i, 0]], [bodies[num, i, 1]])
                    line.set_3d_properties([bodies[num, i, 2]])
                    line.set_alpha(1.0)
                    if self._recoloring_func is not None:
                        line.set_color(colors[i])

        elif self._history_length > 1 or self._history_length <= 0:
            history_slice = slice(None, num)
            if self._history_length > 1:
                history_slice = slice(max(0, num - self._history_length), num)
            for i, line in enumerate(self._lines):
                line.set_data(bodies[history_slice, i, 0], bodies[history_slice, i, 1])
                line.set_3d_properties(bodies[history_slice, i, 2])
                line.set_alpha(1.0)
                if self._recoloring_func is not None:
                    line.set_color(colors[i])
        else:
            if bodies.ndim == 3:
                self._lines.set_data(bodies[num, :, 0], bodies[num, :, 1])
                self._lines.set_3d_properties(bodies[num, :, 2])
                self._lines.set_alpha(1.0)
                if self._recoloring_func is not None:
                    for i, line in enumerate(self._lines):
                        line.set_color(colors[i])
            elif bodies.ndim == 2:
                self._lines.set_data(bodies[:, 0], bodies[:, 1])
                self._lines.set_3d_properties(bodies[:, 2])
                self._lines.set_alpha(1.0)
                if self._recoloring_func is not None:
                    for i, line in enumerate(self._lines):
                        line.set_color(colors[i])

    def _update(self, num):
        if self._verbose:
            if self._verbose == 1:
                sys.stdout.write(".")
                sys.stdout.flush()
                if num == self._snapshot_storage.snapshot_count - 1:
                    print "|"
            elif self._verbose == 2:
                print "{}/{}".format(num, self._snapshot_storage.snapshot_count)

        self._update_lines(num, self._snapshot_storage.snapshots)

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
        bodies = cPickle.load(args.directory)
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

    '''
    #pervaizduoti jau turima .pkl faila

    from storage import SnapshotStorage
    storage = SnapshotStorage()
    storage.load("../plummer_N500_T500_E1e+11_d1e+14_galaxy01.pkl")
    renderer = SnapshotRenderer.for_clusters(storage, bounds=[-1e15, 1e15], verbose=1, angle=90)
    renderer.run('../../plummer_N500_T500_E1e+11_d1e+14_galaxy01_angle90.mp4')
    '''