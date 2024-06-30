from collections import OrderedDict

import cv2

from models import transforms
from utils.general import find_largest_leq_sorted
from config import config


class StudioModel:
    def __init__(self, video_path: str = None):
        self.video_path = video_path
        self.video_path = '/home/tamnv/Downloads/upwork-contract-exporter.mp4'

        self.load()

    def load(self):
        self.video_controller = VideoController(video_path=self.video_path)

        # Settings
        self.aspect_ratio = 'Auto'
        self.padding = 100
        self.inset = 10
        self.border_radius = 50

        # Transforms
        self.mouse_events = {
            'click': [
                {'x': 0.5, 'y': 0.5, 'frame_index': 50, 'duration': 1.5},
                {'x': 0.5, 'y': 0.5, 'frame_index': 150, 'duration': 1.5},
            ],
            'move': []
        }
        background = {'type': 'wallpaper','value': 1}
        self.transform = transforms.Compose({
            'aspect_ratio': transforms.AspectRatio('Auto'),
            'padding': transforms.Padding(padding=self.padding),
            # 'inset': Inset(inset=0),
            'zoom': transforms.Zoom(click_data=self.mouse_events['click'], fps=self.video_controller.fps),
            'roundness': transforms.Roundness(radius=self.border_radius),
            'shadow': transforms.Shadow(),
            'background': transforms.Background(background=background),
        })
        self.video_len = self.video_controller.video_len
        self.fps = self.video_controller.fps
        self.pixels_per_second = config['layout']['video_edit']['pixels_per_second']

    def read(self, frame_index=None):
        frame = self.video_controller.read(frame_index)

        if frame is None:
            return

        if self.transform:
            frame_index = self.video_controller.frame_index
            result = self.transform(input=frame, frame_index=frame_index)
            frame = result['input']

        return frame

    def current_frame(self):
        prev_frame_index = max(0, self.video_controller.frame_index - 1)
        return self.read(prev_frame_index)

    def current_frame_index(self):
        return self.video_controller.frame_index

    def next_frame(self):
        return self.read()

    def prev_frame(self):
        prev_frame_index = max(0, self.video_controller.frame_index - 1)
        return self.read(prev_frame_index)

    def update_aspect_ratio(self, value):
        self.aspect_ratio = value
        self.transform['aspect_ratio'] = transforms.AspectRatio(aspect_ratio=value)

    def update_padding(self, value):
        self.padding = value
        self.transform['padding'] = transforms.Padding(padding=value)

    def update_inset(self, value):
        self.inset = value

    def update_border_radius(self, value):
        self.border_radius = value
        self.transform['roundness'] = transforms.Roundness(radius=value)

    def update_zoom_tracks(self, data):
        # Remove all delete-marked tracks
        self._clean_delete_click_data()

        index = data['index']
        click = self.mouse_events['click'][index]

        del data['index']

        for key, value in data.items():
            click[key] = value

        self.transform['zoom'] = transforms.Zoom(
            click_data=self.mouse_events['click'],
            fps=self.video_controller.fps
        )

        return self.mouse_events['click']

    def insert_zoom_track(self, data):
        # Remove all delete-marked tracks
        self._clean_delete_click_data()

        x_pos = data['x_pos']
        frame_index = x_pos / self.pixels_per_second * self.video_controller.fps

        # Find position for the new track
        frame_indices = [item['frame_index'] for item in self.mouse_events['click']]

        index = find_largest_leq_sorted(frame_indices, frame_index)
        insert_index = index + 1

        self.mouse_events['click'].insert(insert_index, data)

        self.transform['zoom'] = transforms.Zoom(
            click_data=self.mouse_events['click'],
            fps=self.video_controller.fps
        )

        return self.mouse_events['click']

    def delete_track(self, index):
        self._clean_delete_click_data()

        self.mouse_events['click'][index]['delete'] = True

        return self.mouse_events['click']

    def delete_all_tracks(self):
        self._clean_delete_click_data()

        for click in self.mouse_events['click']:
            click['delete'] = True

        return self.mouse_events['click']

    def _clean_delete_click_data(self):
        new_click_data = []
        for click in self.mouse_events['click']:
            if not click.get('delete'):
                new_click_data.append(click)

        self.mouse_events['click'] = new_click_data

    def update_wallpaper(self, data):
        self.transform['background'] = transforms.Background(background=data)


class VideoController:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(video_path)
        self.fps = int(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.frame_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.num_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_len = self.num_frames / self.fps

    def read(self, frame_index=None):
        if isinstance(frame_index, int):
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index - 1)

        ret, frame = self.video_capture.read()
        if not ret:
            return

        return frame

    @property
    def frame_index(self):
        return int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))