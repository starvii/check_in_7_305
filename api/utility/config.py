import os
from pathlib import Path


class Config:
    def __init__(self):
        self.BASE: str = str(Path(__file__).parent.parent.parent)
        self.STATIC: str = str(Path(self.BASE) / Path('web/dist/'))
        self.DATABASE: str = str(Path(self.BASE) / Path('db.sqlite'))
        os.environ['BASE'] = self.BASE
        os.environ['STATIC'] = self.STATIC
        os.environ['DATABASE'] = self.DATABASE
