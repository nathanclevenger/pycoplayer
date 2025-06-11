from unittest import mock
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / 'src'))
import types, builtins
import sys as _sys
_sys.modules['mss'] = types.SimpleNamespace(mss=object())
fake_pil = types.ModuleType('PIL')
fake_pil.Image = types.SimpleNamespace()
_sys.modules['PIL'] = fake_pil
_sys.modules['PIL.Image'] = fake_pil.Image
_sys.modules['torchvision'] = types.SimpleNamespace(transforms=object())
_sys.modules['numpy'] = types.SimpleNamespace(array=lambda *a, **k: None, ndarray=object)
_sys.modules['cv2'] = types.SimpleNamespace(VideoWriter=lambda *a, **k: None,
                                            VideoWriter_fourcc=lambda *a: 0,
                                            COLOR_BGR2RGB=0,
                                            cvtColor=lambda *a, **k: a[0])
import importlib
import screen as screen_mod
importlib.reload(screen_mod)
from screen import ScreenRecorder


class DummyFrame:
    def __init__(self, shape=(4, 4, 3)):
        self.shape = shape



def test_screen_recorder_writes_frames(tmp_path):
    recorder = ScreenRecorder(video_name=str(tmp_path / 'out.webm'), fps=10)
    frame = DummyFrame()
    recorder.add_frame(frame)

    dummy_writer = mock.MagicMock()
    with mock.patch('cv2.VideoWriter', return_value=dummy_writer) as vw, \
         mock.patch('cv2.VideoWriter_fourcc', return_value=0) as vf, \
         mock.patch('cv2.cvtColor', side_effect=lambda a, b: a) as cvt:
        recorder.save()
        vw.assert_called_once()
        dummy_writer.write.assert_called_once_with(frame)
        dummy_writer.release.assert_called_once()
