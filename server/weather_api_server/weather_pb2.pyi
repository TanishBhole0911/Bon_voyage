from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Forcaste_Weather_req(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    def __init__(self, address: _Optional[str] = ...) -> None: ...

class Values(_message.Message):
    __slots__ = ("precipitationProbability", "temperature", "weatherCodeDay")
    PRECIPITATIONPROBABILITY_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    WEATHERCODEDAY_FIELD_NUMBER: _ClassVar[int]
    precipitationProbability: float
    temperature: float
    weatherCodeDay: str
    def __init__(self, precipitationProbability: _Optional[float] = ..., temperature: _Optional[float] = ..., weatherCodeDay: _Optional[str] = ...) -> None: ...

class Interval(_message.Message):
    __slots__ = ("startTime", "values")
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    startTime: str
    values: Values
    def __init__(self, startTime: _Optional[str] = ..., values: _Optional[_Union[Values, _Mapping]] = ...) -> None: ...

class Forcaste_Weather_res(_message.Message):
    __slots__ = ("timestep", "endTime", "startTime", "intervals")
    TIMESTEP_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    INTERVALS_FIELD_NUMBER: _ClassVar[int]
    timestep: str
    endTime: str
    startTime: str
    intervals: _containers.RepeatedCompositeFieldContainer[Interval]
    def __init__(self, timestep: _Optional[str] = ..., endTime: _Optional[str] = ..., startTime: _Optional[str] = ..., intervals: _Optional[_Iterable[_Union[Interval, _Mapping]]] = ...) -> None: ...
