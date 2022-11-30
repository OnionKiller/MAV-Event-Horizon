from uuid import uuid4
from sqlalchemy_utils import UUIDType, JSONType  # type:ignore
from sqlalchemy import Integer, Date, String  # type:ignore
from sqlalchemy import Column, ForeignKey  # type:ignore

from db import DeclarativeBase

UUID = UUIDType(native=True)


class MAVEvent(DeclarativeBase):
    """Simple class to hold event instances.
    The events are handled as immutable objects regarding the RSS feed.
    The (main) properties of an event are:
    ---

    `id`: Used by the RSS feed, this indicates corresponding events
    `last_modification`: Event timestamp when the event was last modified
    `update_uuid`: UUID of the next update of the event. Events may have multiple updated, then
        the event instaces are chained with this.
    """

    __tablename__ = "RSS_events_MAV"

    uuid = Column(
        UUID, primary_key=True, nullable=False, unique=True, default=uuid4
    )
    id = Column(Integer, nullable=False)
    last_modification = Column(Date, nullable=False)
    update_uuid = Column(UUID)
    title = Column(String(50))

    def __repr__(self):
        return f"[{self.uuid}]:({self.id})-{self.title}"


class MAVEventDump(DeclarativeBase):
    __tablename__ = "RAW_events_MAV"
    id = Column(Integer, primary_key=True)
    event_uuid = Column(
        UUID, ForeignKey("RSS_events_MAV.uuid", ondelete="SET NULL")
    )
    event_dict = Column(JSONType)

    def __repr__(self):
        return f"[{self.id}]:({self.event_uuid})-{str(dict):50}"
