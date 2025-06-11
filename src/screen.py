import mss
from PIL import Image
from torchvision import transforms
import numpy
import cv2
from enum import Enum

class ImageType(Enum):
    PILImage = 0,
    GrayscaleImage = 1,
    
Region = {
    "top": 300,
    "left": 1150,
    "width": 1500,
    "height": 500
}

class AIScreenshot:
    def __init__(self):
        self.sct = mss.mss()
        self.screenshot = None
        self.PILImage = None
        self.tensor = None
        self.array = None
        self.transform = transforms.Compose([transforms.RandomHorizontalFlip(),
                                        transforms.RandomRotation(20),
                                        transforms.Resize(size=(224,224)),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5,),(0.5,))])
        self.image_grayscale = None
        
    def take_screenshot(self, region=False, region_area=Region):
        if (region == True):
            self.screenshot = self.sct.grab(region_area)
            self.process_to_PIL()
            self.process_to_array()
        else:
            self.screenshot = self.sct.grab(self.sct.monitors[1])
            self.process_to_PIL()
            self.process_to_array()

    def process_to_PIL(self):
        self.PILImage = Image.frombytes("RGB", self.screenshot.size, self.screenshot.rgb)
        
    def process_to_array(self):
        self.array = numpy.array(self.screenshot)
    
    def transform_to_tensor(self, image_type: ImageType):

        if (image_type == ImageType.PILImage):
            self.tensor = self.transform(self.PILImage)
        else:
            self.tensor = self.transform(self.PILImage.convert("L"))
        
        return self.tensor
        
    def show_screenshot(self, image_type: ImageType):
        if (image_type == ImageType.PILImage):
            self.PILImage.show()
        else:
            self.PILImage.convert("L").show()
        
    def transform_to_grayscale(self):
        self.image_grayscale = self.PILImage.convert("L")
        
        return self.image_grayscale
        
class ScreenRecorder:
    """Utility to record frames and save them as a video."""

    def __init__(self, video_name: str | None = None, fps: int = 10):
        self.video_name = video_name
        self.fps = fps
        self.frames: list[numpy.ndarray] = []

    def add_frame(self, frame: numpy.ndarray) -> None:
        """Add a frame to the recording."""
        self.frames.append(frame)

    def save(self, video_name: str | None = None) -> str:
        """Save all recorded frames into a video file.

        Parameters
        ----------
        video_name: str | None
            Optional file name to override the default provided at
            initialization.

        Returns
        -------
        str
            Path to the created video file.
        """

        name = video_name or self.video_name
        if name is None:
            import random
            import string

            name = "".join(random.choice(string.ascii_letters) for _ in range(18)) + ".webm"

        if not self.frames:
            raise ValueError("No frames recorded")

        height, width = self.frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*"VP90")
        writer = cv2.VideoWriter(name, fourcc, self.fps, (width, height))

        for img in self.frames:
            writer.write(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        writer.release()
        return name

class CharacterRecognition:
    def __init__(self):
        pass

    def read_screen(self, image: Image):
        """Run OCR on ``image`` and return the extracted text."""
        try:
            import pytesseract
        except Exception as exc:  # pragma: no cover - gracefully handle missing dep
            raise ImportError("pytesseract is required for OCR") from exc

        return pytesseract.image_to_string(image)
