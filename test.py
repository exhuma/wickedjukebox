from wickedjukebox import make_declarative_base, Base
make_declarative_base(uri='sqlite://', echo=True)

from wickedjukebox.database import *

Base.metadata.create_all()
