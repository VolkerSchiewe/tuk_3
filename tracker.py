class Tracker:
    def __init__(self):
        self.samples = 0
        self.frames = 0
        self.samples_per_frame = 0
        self.frames_interpolated = 0

    def track_sample(self):
        self.samples += 1

    def track_frame(self, samples):
        self.frames += 1
        self.samples_per_frame += samples

    def track_interpolated_frames(self, frames):
        self.frames_interpolated += frames

    def print(self):
        print(f'Tracked {self.samples} samples, {self.frames_interpolated} frames were interpolated, '
              f'{self.samples_per_frame / self.frames} samples per frame were found.')
