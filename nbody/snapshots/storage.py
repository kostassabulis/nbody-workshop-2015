import pickle
import os

import numpy as np

import util


class SnapshotStorage(object):
    """Stores snapshots of any type as they're passed in, can also automatically save to file.

       :param snapshot_shape: the shape of the snapshot matrix as a tuple, 
                              usually (object_count, 3) for storing coordinates of objects.
       :param max_snapshots: the number of snapshots that will be stored, if specified storage
                             can be sped up, as matrices don't need to be concatenated.
       :param in_memory: sets whether snapshots should be stored in memory when append
                         is called.
       :param output_path: output path for snapshots. A snapshot is saved every time 
                           append is called, if this is specified.
    """
    def __init__(self, snapshot_shape=None, max_snapshots=None, 
                 in_memory=True, output_path=None):
        self.snapshot_shape = snapshot_shape
        self.max_snapshots = max_snapshots
        self.in_memory = in_memory
        self.output_path = output_path
        self.snapshot_count = 0
        self._current_index = 0

        if not self.in_memory and not self.output_path:
            raise ValueError("Storage either has to be in memory, or have a valid directory set for output.")

        if self.in_memory:
            self._reserved_length = max_snapshots
            if not self._reserved_length:
                self._reserved_length = 1000


            if not snapshot_shape:
                self._snapshots = None
            else:
                self._init_snapshot_storage()

    def append(self, snapshot):
        if self.in_memory:
            if self._snapshots is not None:
                if snapshot.shape != self.snapshot_shape:
                    raise ValueError("This snapshot doesn't match the initialized shape.")
            else:
                self.snapshot_shape = snapshot.shape
                self._init_snapshot_storage()

            if self._current_index >= self._reserved_length:
                if self.max_snapshots:
                    raise IndexError("Appending exceeded the set maximum snapshot count.")
                else:
                    self._expand_snapshot_storage()

            self._snapshots[self._current_index, :] = snapshot

        if self.output_path:
            output_file_name = os.path.join(self.output_path, 
                                            "nbody_snapshot.csv", 
                                            str(self._current_index))

            util.save_snapshot(snapshot, output_file_name)

        self._current_index += 1
        self.snapshot_count += 1


    def get_snapshot(self, index):
        if not self.in_memory:
            raise IOError("Can't get snapshot because in-memory storage is disabled.")

        if index < 0 or index >= self._current_index:
            raise IndexError("The snapshot with the specified index doesn't exist.")

        return self._snapshots[index, :]

    def load(self, file_name):
        if not self.in_memory:
            raise IOError("Can't load from file because in in-memory storage is disabled.")

        if file_name.endswith(".pkl"):
            self._snapshots = pickle.load(file_name)
        else:
            self._snapshots = util.load_snapshots(file_name)
        
        self.snapshot_shape = self._snapshots.shape[1:]
        self.max_snapshots = self._snapshots.shape[0]
        self._reserved_length = self.max_snapshots
        self._current_index = self.max_snapshots
        self.snapshot_count = self.max_snapshots

    def save(self, file_name):
        if not self.in_memory:
            raise IOError("Can't save the storage since it's not stored in memory.")

        if file_name.endswith(".pkl"):
            pickle.dump(self._snapshots, file_name)
        else:
            for i in range(self._current_index):
                output_file_name = os.path.join(file_name, "nbody_snapshot.csv", str(i))
                util.save_snapshot(self._snapshots[self._current_index, :], output_file_name)

    @property
    def snapshots(self):
        if not self.in_memory:
            raise IOError("Can't get snapshots because in-memory storage is disabled.")
        return self._snapshots[:self._current_index + 1, :]

    @snapshots.setter
    def snapshots(self, value):
        if not self.in_memory:
            raise IOError("Can't set snapshots because in-memory storage is disabled.")
        self._snapshots = value

    @snapshots.deleter
    def snapshots(self):
        if not self.in_memory:
            raise IOError("Can't delete snapshots because in-memory storage is disabled.")
        del self._snapshots

    def _init_snapshot_storage(self):
        self._snapshots = np.zeros((self._reserved_length, ) + self.snapshot_shape)

    def _expand_snapshot_storage(self):
        self._snapshots = np.concatenate([self._snapshots, np.zeros(self._snapshots.shape)])
        self._reserved_length *= 2