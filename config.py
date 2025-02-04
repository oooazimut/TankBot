from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModbusSettings(BaseModel):
    host: str
    port_pptp: int
    port_l2tp: int


class TankVars(BaseModel):
    low_border: int
    high_border: int
    warning: int
    critical: int
    pump_on: float


class Alarms(BaseModel):
    SENSOR_FAILURE: str
    FIRST_CRIT_LEVEL: str
    SECOND_CRIT_LEVEL: str
    CURR_SENSOR_FAILURE: str
    HIGH_CURRENT_FAILURE: str
    POSSIBLY_LACK_OF_POWER: str
    POSSIBLY_DEFECTIVE_PUMP: str


class Settings(BaseSettings):
    bot_token: SecretStr
    db_name: str
    modbus: ModbusSettings
    passwd: SecretStr
    tank: TankVars
    alarms: Alarms

    @property
    def sqlite_async_dsn(self):
        return f"sqlite+aiosqlite:///{self.db_name}"

    @property
    def sqlite_dsn(self):
        return f"sqlite:///{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
