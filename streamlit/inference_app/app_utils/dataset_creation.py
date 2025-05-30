from baseballcv.functions import BaseballSavVideoScraper
import cv2
import os
import random
from datetime import date
from typing import Callable

class DatasetCreator:
    """
    Class that creates random videos between April and August from 2021 to 2024 if the user doesn't have
    any videos to use.
    """
    def __init__(self, styling: Callable[[], None]) -> None:
         """
         Initializes the `DatasetCreator` class.

         Args:
            styling (Callable[[], None]): The css style formatted when each function is running.
         """
         styling()

    def generate_video(self, output_video):
        """
        Generates a random video using `BaseballSavVideoScraper`.

        Args:
            output_video (Path): The desired path for the video to go. 
        """
        teams = [
                "ATH", "ATL", "AZ", "BAL", "BOS", "CHC", "CIN", "CLE", "COL", "CWS", "DET", "HOU",
                "KC", "LAA", "LAD", "MIA", "MIL", "MIN", "NYM", "NYY", "PHI", "PIT", "SD", "SEA",
                "SF", "STL", "TB", "TEX", "TOR", "WSH"
            ]
        
        random_team = random.choice(teams)
        random_date = date.strftime(date(random.randint(2021, 2024), random.randint(4, 8), random.randint(1, 25)), '%Y-%m-%d')
        
        BaseballSavVideoScraper(random_date, download_folder=output_video, team_abbr=random_team, max_return_videos=1).run_executor()
        

    def generate_example_images(self, img_file, cap: cv2.VideoCapture, length: int) -> None:
        """
        Generates random images from the frames of a image file. The purpose for this is if
        the user doesn't have images but doesn't want to run through all the frames, they have the
        option to generate random frames of the video.

        Args:
            img_file (Path): The directory to the images file, where the image will be written to.
            cap (VideoCapture): The captured video.
            length (int): The length of the video in frames.
        """
        random_index = random.sample(range(0, length), 3)

        i = 0
        while cap.isOpened():
            read, frame = cap.read()

            if read and i in random_index:
                file_name = os.path.join(img_file, f"frame_{i}.jpg")
                cv2.imwrite(file_name, frame)

            i += 1

            if i > max(random_index):
                break
