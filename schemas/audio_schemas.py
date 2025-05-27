from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum


class AudioFileBase(BaseModel):
    user_id: int
    title: str
    file_size: int


class AudioFileOut(AudioFileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class AudioResultStatus(StrEnum):
    on_process: str = "В обработке"
    ready: str = "Готово"
    error: str = "Ошибка"


class AudioResultBase(BaseModel):
    audio_file_id: int
    transcription: dict
    status: AudioResultStatus


class AudioResultOut(AudioResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
