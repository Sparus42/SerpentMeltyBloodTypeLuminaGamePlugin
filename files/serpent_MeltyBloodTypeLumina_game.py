from serpent.game import Game

from .api.api import MeltyBloodTypeLuminaAPI

from serpent.utilities import Singleton

import numpy.random as r

import sys




class SerpentMeltyBloodTypeLuminaGame(Game, metaclass=Singleton):

    def __init__(self, **kwargs):
        kwargs["platform"] = "steam"

        kwargs["window_name"] = "MELTY BLOOD: TYPE LUMINA "

        kwargs["app_id"] = "1372280"
        kwargs["app_args"] = None

        #Generic Memory Locations
        self.time_mAdr = 0x5630E0

        #Player 1 Memory Locations
        self.p1_mAdr = {
            "score": 0x5638C8,
            "character": 0x62B348,
            "color": 0x62B34C,
            "right": 0x5639AC,
            "health": 0xA8F1CC,
            "vital": 0xA8F1D0,
            "moon": 0xA8FA58,
            "blood": 0xA8FA54,
            "magic": 0xA8F1E0,
            "heat": 0xA8F230,
            "hactiv": 0x5630DC,
        }

        #Player 2 Memory Locations
        self.p2_mAdr = {
            "score": 0x563908,
            "character": 0x62B384,
            "color": 0x62B388,
            "right": 0x5639B0,
            "health": 0xA8FDC0,
            "vital": 0xA8FDC4,
            "moon": 0xA9064C,
            "blood": 0xA90648,
            "magic": 0xA8FDD4,
            "heat": 0xA8FE24,
            "hactiv": 0xA8FDD0,
        }

        super().__init__(**kwargs)

        self.api_class = MeltyBloodTypeLuminaAPI
        self.api_instance = None

    @property
    def screen_regions(self):
        pass
        '''regions = {
            "SAMPLE_REGION": (0, 0, 0, 0)
        }

        return regions'''

    @property
    def ocr_presets(self):
        presets = {
            "SAMPLE_PRESET": {
                "extract": {
                    "gradient_size": 1,
                    "closing_size": 1
                },
                "perform": {
                    "scale": 10,
                    "order": 1,
                    "horizontal_closing": 1,
                    "vertical_closing": 1
                }
            }
        }
        return presets

    def pull_memory(self):

        #Get player 1 memory data
        p1_mem = {}
        for key in self.p1_mAdr:
            p1_mem[key] = int.from_bytes(self.window_controller.read_memory(self.p1_mAdr[key], add_handle=True), sys.byteorder)

        #Get player 2 memory data
        p2_mem = {}
        for key in self.p2_mAdr:
            p2_mem[key] = int.from_bytes(self.window_controller.read_memory(self.p2_mAdr[key], add_handle=True), sys.byteorder)

        #Get generic memory data
        time = int.from_bytes(self.window_controller.read_memory(self.time_mAdr, add_handle=True), sys.byteorder)

        return (p1_mem, p2_mem, time)

    def set_char(self, player, character=None):
        mAdr = {}
        if player == 1:
            mAdr = self.p1_mAdr
        elif player == 2:
            mAdr = self.p2_mAdr
        else:
            raise ValueError('Player can only be 1 or 2.')

        if character == None:
            character = r.randint(0,14)
        character = character.to_bytes(4, sys.byteorder)

        self.window_controller.write_memory(character, mAdr['character'], add_handle=True)

    def set_color(self, player, color=None):
        mAdr = {}
        if player == 1:
            mAdr = self.p1_mAdr
        elif player == 2:
            mAdr = self.p2_mAdr
        else:
            raise ValueError('Player can only be 1 or 2.')

        if color == None:
            color = r.randint(0,13)
            if color > 9:
                color += 32

        color = color.to_bytes(4, sys.byteorder)

        self.window_controller.write_memory(color, mAdr['color'], add_handle=True)
