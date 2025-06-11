from unittest import mock
from types import SimpleNamespace
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / 'src'))
import types, sys as _sys
_sys.modules['mss'] = types.SimpleNamespace(mss=object())
fake_pil = types.ModuleType('PIL')
fake_pil.Image = types.SimpleNamespace()
_sys.modules['PIL'] = fake_pil
_sys.modules['PIL.Image'] = fake_pil.Image
_sys.modules['torchvision'] = types.SimpleNamespace(transforms=object())
_sys.modules['numpy'] = types.SimpleNamespace(ndarray=object)
_sys.modules['cv2'] = types.SimpleNamespace()
_sys.modules['pytesseract'] = types.SimpleNamespace(image_to_string=lambda x: '')
import importlib
import screen as screen_mod
importlib.reload(screen_mod)
from screen import CharacterRecognition


def test_read_screen_uses_ocr():
    img = SimpleNamespace()
    with mock.patch('pytesseract.image_to_string', return_value='text') as ocr:
        recog = CharacterRecognition()
        text = recog.read_screen(img)
        ocr.assert_called_once_with(img)
        assert text == 'text'
