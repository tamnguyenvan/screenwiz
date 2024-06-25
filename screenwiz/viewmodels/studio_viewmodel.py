import numpy as np
from PySide6.QtCore import QObject, Signal, QThread


class StudioViewModel(QObject):
    # Settings
    on_padding_changed = Signal(int)
    on_inset_changed = Signal(int)
    on_border_radius_changed = Signal(int)

    # Frame preview
    on_frame_changed = Signal(np.ndarray)
    on_playing_changed = Signal(bool)

    # Video len
    on_video_len_changed = Signal(float)

    # Slider
    on_timeslider_position_changed = Signal(int)

    # Zoom tracks
    on_zoom_tracks_changed = Signal(tuple)

    def __init__(self, model):
        super().__init__()

        self.model = model

        self.video_thread = VideoThread(self.model)
        self.video_thread.on_frame_ready.connect(self.on_frame_changed)
        self.video_thread.on_timeslider_position_changed.connect(self.on_timeslider_position_changed)

    def load(self):
        # Emit a video length changed signal
        self.on_video_len_changed.emit(self.model.video_len)

        # Emit a zoom track data changed signal
        mouse_events = self.model.mouse_events
        zoom_track_data = mouse_events['click']
        self.on_zoom_tracks_changed.emit(zoom_track_data)

    def update_padding(self, value):
        self.model.update_padding(value)
        self.on_padding_changed.emit(self.model.padding)

        if not self.video_thread.is_running():
            self.current_frame()

    def update_inset(self, value):
        self.model.update_inset(value)
        self.on_inset_changed.emit(self.model.inset)

    def update_border_radius(self, value):
        self.model.update_border_radius(value)
        self.on_border_radius_changed.emit(self.model.border_radius)

        if not self.video_thread.is_running():
            self.current_frame()

    def toggle_playing_video(self):
        if self.video_thread.is_running():
            # Stop
            self.on_playing_changed.emit(False)
            self.video_thread.stop()
        else:
            # Start
            self.on_playing_changed.emit(True)
            self.video_thread.start()  # Correctly start the thread

    def next_frame(self):
        # Grab next frame and emit a frame changed signal
        frame = self.model.next_frame()
        self.on_frame_changed.emit(frame)

        # Calculate the desired position of the time slider and emit a signal
        pixels_per_second = 200
        frame_index = self.model.current_frame_index()
        x_pos = frame_index / self.model.fps * pixels_per_second
        self.on_timeslider_position_changed.emit(x_pos)

    def prev_frame(self):
        # Grab previous frame and emit a frame changed signal
        frame = self.model.prev_frame()
        self.on_frame_changed.emit(frame)

        # Calculate the desired position of the time slider and emit a signal
        pixels_per_second = 200
        frame_index = self.model.current_frame_index()
        x_pos = frame_index / self.model.fps * pixels_per_second
        self.on_timeslider_position_changed.emit(x_pos)

    def current_frame(self):
        frame = self.model.current_frame()
        self.on_frame_changed.emit(frame)

    def read_frame(self, frame_index):
        frame = self.model.read(frame_index)
        self.on_frame_changed.emit(frame)

    def fps(self):
        return self.model.fps

    def update_frame_based_on_position(self, x_pos):
        is_running = False
        if self.video_thread.is_running():
            is_running = True
            self.video_thread.stop()

        pixels_per_second = 200
        frame_index = int(x_pos / pixels_per_second * self.model.fps)
        self.read_frame(frame_index)

        if is_running:
            self.video_thread.start()

    def update_slider_position(self, x_pos):
        self.on_timeslider_position_changed.emit(x_pos)

    def update_zoom_tracks(self, data):
        index, x_pos, width = data
        pixels_per_second = 200
        frame_index = x_pos / pixels_per_second * self.model.fps
        duration = width / pixels_per_second

        updated_data = {'index': index, 'frame_index': frame_index, 'duration': duration, 'x_pos': x_pos, 'width': width}

        new_zoom_tracks = self.model.update_zoom_tracks(updated_data)
        self.on_zoom_tracks_changed.emit(new_zoom_tracks)

    def insert_zoom_track(self, data):
        x_pos, width = data
        pixels_per_second = 200
        frame_index = x_pos / pixels_per_second * self.model.fps
        duration = width / pixels_per_second

        updated_data = {'x': 0.5, 'y': 0.5, 'frame_index': frame_index, 'duration': duration, 'x_pos': x_pos, 'width': width}
        new_zoom_tracks = self.model.insert_zoom_track(updated_data)
        self.on_zoom_tracks_changed.emit(new_zoom_tracks)

    def delete_track(self, index):
        new_zoom_tracks = self.model.delete_track(index)
        self.on_zoom_tracks_changed.emit(new_zoom_tracks)

    def delete_all_tracks(self):
        new_zoom_tracks = self.model.delete_all_tracks()
        self.on_zoom_tracks_changed.emit(new_zoom_tracks)

    def update_wallpaper(self, data):
        self.model.update_wallpaper(data)

        if not self.video_thread.is_running():
            self.current_frame()


class VideoThread(QThread):
    on_frame_ready = Signal(np.ndarray)
    on_timeslider_position_changed = Signal(int)
    on_playing_changed = Signal(bool)

    def __init__(self, model):
        super().__init__()
        self.model = model
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            frame = self.model.next_frame()
            if frame is None:
                break

            frame_index = self.model.current_frame_index()
            self.on_frame_ready.emit(frame)

            pixels_per_second = 200
            x_pos = frame_index / self.model.fps * pixels_per_second
            self.on_timeslider_position_changed.emit(x_pos)

            self.msleep(20)  # 50 frames per second

    def stop(self):
        self._running = False
        self.wait()  # Ensure the thread finishes execution

    def is_running(self):
        return self._running