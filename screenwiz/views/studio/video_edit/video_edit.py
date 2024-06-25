from collections import OrderedDict

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QSize

from views.widgets.custom_scrollarea import CustomScrollArea
from views.widgets.mouse_area import MouseArea, ZoomTrackMouseArea
from views.studio.video_edit.timeline import Timeline
from views.studio.video_edit.time_indicator import TimeIndicator
from views.studio.video_edit.time_slider import TimeSlider
from views.studio.video_edit.clip_track import ClipTrack
from views.studio.video_edit.zoom_track import ZoomTrack
from views.studio.video_edit.hover_zoom_track import HoverZoomTrack
from utils.context_utils import AppContext


pixels_per_second = 200


class VideoEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setFixedHeight(250)
        self.init_ui()

        self.zoom_tracks = OrderedDict()
        self.mouse_areas = []

        AppContext.get('view_model').on_video_len_changed.connect(self.update_content_width)
        AppContext.get('view_model').on_zoom_tracks_changed.connect(self.update_zoom_tracks)
        AppContext.get('view_model').on_zoom_tracks_changed.connect(self.update_mouse_areas)

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Wrap everything in a scroll area
        scroll_area = CustomScrollArea()
        scroll_area.setWidgetResizable(True)

        # Content widget
        self.content_widget = QWidget()
        self.content_widget.setFixedSize(0, self.height() - 10)

        # Actual content
        self._init_timeline(parent=self.content_widget)
        self._init_clip_track(parent=self.content_widget)
        self._init_timeslider(parent=self.content_widget)
        # self._init_mouse_areas(parent=self.content_widget)
        self._init_hover_zoom_track(parent=self.content_widget)
        self._init_time_indicator(parent=self.content_widget)

        # Set content widget for the scroll area
        scroll_area.setWidget(self.content_widget)

        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def _init_timeline(self, parent):
        self.timeline = Timeline(parent=parent)
        self.timeline.move(0, 0)

    def _init_timeslider(self, parent):
        self.time_slider = TimeSlider(parent=parent)
        self.time_slider.move(0, 0)

    def _init_clip_track(self, parent):
        self.clip_track = ClipTrack(parent=parent)
        self.clip_track.move(0, 80)

    # def _init_zoom_tracks(self, parent):
    #     zoom_track_list = [1]

    #     self.zoom_tracks = []

    #     for item in zoom_track_list:
    #         size = QSize(500, 60)
    #         zoom_track = ZoomTrack(size=size, parent=parent)
    #         zoom_track.move(500, 150)
    #         self.zoom_tracks.append(zoom_track)
    def _init_hover_zoom_track(self, parent):
        self.hover_zoom_track = HoverZoomTrack(parent=parent)
        self.hover_zoom_track.setVisible(False)
        self.hover_zoom_track.move(0, 150)

    def _init_time_indicator(self, parent):
        self.time_indicator = TimeIndicator(parent=parent)
        self.time_indicator.setVisible(False)
        self.time_indicator.move(0, 0)

    def update_content_width(self, video_len):
        new_width = int(video_len * pixels_per_second) + 100
        self.content_widget.setFixedWidth(new_width)

    def update_zoom_tracks(self, zoom_track_data):
        drag_minimum_x = 0
        fps = AppContext.get('view_model').fps()

        # for i, zoom_track in self.zoom_tracks.items():
        #     zoom_track.deleteLater()

        # self.zoom_tracks = OrderedDict()

        # for i, item in enumerate(zoom_track_data):
        new_zoom_track_data = []
        for index, item in enumerate(zoom_track_data):
            frame_index = item['frame_index']

            is_deleted = item.get('delete', False)
            if is_deleted and index in self.zoom_tracks:
                self.zoom_tracks[index].deleteLater()
                del self.zoom_tracks[index]
                continue

            new_zoom_track_data.append(item)

        zoom_track_data = new_zoom_track_data

        for index, item in enumerate(zoom_track_data):
            frame_index = item['frame_index']
            duration = item['duration']
            if 'width' in item:
                width = item['width']
            else:
                width = int(duration * pixels_per_second)

            # Calculate the position and size
            if 'x_pos' in item:
                x_pos = item['x_pos']
            else:
                x_pos = int(frame_index / fps * pixels_per_second)
            size = QSize(width, 60)

            # Calculate the drag range
            if index + 1 < len(zoom_track_data):
                next_zoom_track = zoom_track_data[index + 1]
                drag_maximum_x = int(next_zoom_track['frame_index'] / fps * pixels_per_second)
            else:
                drag_maximum_x = 1e6

            if index not in self.zoom_tracks:
                zoom_track = ZoomTrack(
                    index=index,
                    size=size,
                    drag_range=[drag_minimum_x, drag_maximum_x],
                    parent=self.content_widget
                )
            else:
                zoom_track = self.zoom_tracks[index]
                zoom_track.setFixedSize(size)

            zoom_track.setVisible(True)
            zoom_track.move(x_pos, 150)

            self.zoom_tracks[index] = zoom_track

    def update_mouse_areas(self, zoom_track_data):
        prev_x = 0

        for mouse_area in self.mouse_areas:
            mouse_area.deleteLater()

        self.mouse_areas = []
        fps = AppContext.get('view_model').fps()

        new_zoom_track_data = []
        for index, item in enumerate(zoom_track_data):
            is_deleted = item.get('delete', False)
            if is_deleted:
                continue

            new_zoom_track_data.append(item)

        zoom_track_data = new_zoom_track_data

        for item in zoom_track_data:
            # frame_index = item['frame_index']
            # duration = item['duration']
            # fps = AppContext.get('view_model').fps()
            frame_index = item['frame_index']
            duration = item['duration']
            if 'width' in item:
                width = item['width']
            else:
                width = int(duration * pixels_per_second)

            # Calculate the position and size
            if 'x_pos' in item:
                x_pos = item['x_pos']
            else:
                x_pos = int(frame_index / fps * pixels_per_second)
            # size = QSize(width, 60)

            # x_pos = int(frame_index / fps * pixels_per_second)
            # width = int(duration * pixels_per_second)

            mouse_area_width = x_pos - prev_x
            if mouse_area_width <= 0:
                # TODO: remove it
                pass

            mouse_area = ZoomTrackMouseArea(parent=self.content_widget)
            mouse_area.setVisible(True)
            mouse_area.setFixedSize(mouse_area_width, 60)
            mouse_area.move(prev_x, 150)
            mouse_area.on_left.connect(self.hide_hover_zoom_track)
            mouse_area.on_clicked.connect(self.add_zoom_track)
            mouse_area.on_mouse_moved.connect(self.show_hover_zoom_track)

            self.mouse_areas.append(mouse_area)

            # Update previous x
            prev_x = x_pos + width

        # Last mouse area
        last_x = 1e6
        mouse_area = ZoomTrackMouseArea(parent=self.content_widget)
        mouse_area_width = last_x - prev_x
        mouse_area.setVisible(True)
        mouse_area.setFixedSize(mouse_area_width, 60)
        mouse_area.move(prev_x, 150)
        mouse_area.on_left.connect(self.hide_hover_zoom_track)
        mouse_area.on_clicked.connect(self.add_zoom_track)
        mouse_area.on_mouse_moved.connect(self.show_hover_zoom_track)
        self.mouse_areas.append(mouse_area)

        # for i, area in enumerate(self.mouse_areas):
        #     print('mouse ', i, area.size())
        # print('len mouse areas', len(self.mouse_areas))

    def add_zoom_track(self, pos):
        x_pos = pos.x()
        width = 200

        # Check valid

        inserted_data = [x_pos, width]

        AppContext.get('view_model').insert_zoom_track(inserted_data)

    def show_hover_zoom_track(self, pos):
        self.hover_zoom_track.setVisible(True)
        self.hover_zoom_track.move(pos.x(), 150)

        self.time_indicator.setVisible(True)
        self.time_indicator.move(pos.x(), 0)

    def hide_hover_zoom_track(self):
        self.hover_zoom_track.setVisible(False)
        self.time_indicator.setVisible(False)

    def update_clip_tracks(self):
        pass