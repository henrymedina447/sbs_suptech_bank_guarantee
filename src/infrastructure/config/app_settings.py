import os
from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

path_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
dotenv_path = os.path.join(path_root, ".env")
load_dotenv(dotenv_path, override=True)


class AwsSettings(BaseModel):
    access_key_id: str = Field(description="es el access key de la cuenta obtenido en el IAM")
    secret: str = Field(description="es el secret key de la cuenta obtenido en el IAM")
    region: str = Field(description="La región de la aplicación")
    bedrock_token: str = Field(description="Es el bearer token para bedrock")



class S3Settings(BaseModel):
    bucket: str = Field(default="Nombre del bucket")
    prefix: str = Field(default="El prefijo - directorio donde se guardará")
    kms_key_id: str | None = Field(description="El KMS Key ID obtenido", default=None)


class TableSettings(BaseModel):
    it_table: str = Field(description="Es el nombre de la tabla interna del supervisado")
    rr_table: str = Field(description="Es el nombre de la tabla de reportes regulatorios")
    ar_table: str = Field(description="Es el nombre de la tabla resultados de análisis")
    si_table: str = Field(description="Es el nombre de la tabla supervisory records que contiene todos los metadatos")


class SqsSettings(BaseModel):
    queue_url: str = Field(description="Es el enlace de conexión para publicar en sqs")


class KafkaSettings(BaseModel):
    bootstrap_servers: str = Field(description="")
    topic: str = Field(description="Tópico del mensaje a escuchar")
    group_id: str = Field(description="Es el ID que identifica quien lo está consumiendo")
    security_protocol: Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"] = Field(
        description="Indica el protocolo de seguridad",
        default="PLAINTEXT")
    sasl_mechanism: str | None = Field(description="", default=None)
    sasl_username: str | None = Field(description="", default=None)
    sasl_password: str | None = Field(description="", default=None)


class AppSettings(BaseModel):
    aws_settings: AwsSettings = Field(description="Todas las configuraciones de AWS")
    table_settings: TableSettings = Field(description="Todas las configuraciones asociadas a las tablas de dynamo")
    kafka_settings: KafkaSettings = Field(description="Todas las configuraciones asociadas al kafka")
    s3_settings: S3Settings = Field(
        description="Todas las configuraciones asociadas al bucket s3 de guardar del análisis")
    sqs_settings: SqsSettings = Field(description="Todas las configuraciones asociadas a sqs")
    mode: Literal["mock", "development"] = Field(
        description="Indica si la aplicación está utilizando los mocks o no",
        default="development"
    )

    @classmethod
    def load(cls) -> "AppSettings":
        try:
            return cls(
                mode="mock",
                aws_settings=AwsSettings(
                    access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region=os.getenv("AWS_DEFAULT_REGION"),
                    bedrock_token=os.getenv("AWS_BEARER_TOKEN_BEDROCK")
                ),
                table_settings=TableSettings(
                    it_table=os.getenv("IT_TABLE"),
                    rr_table=os.getenv("RR_TABLE"),
                    ar_table=os.getenv("ANALYSIS_RESULT_TABLE"),
                    si_table=os.getenv("SUPERVISED_ITEMS_TABLE")
                ),
                kafka_settings=KafkaSettings(
                    bootstrap_servers=os.getenv("AWS_KAFKA_BOOTSTRAP_SERVERS"),
                    topic=os.getenv("AWS_KAFKA_TOPIC"),
                    group_id=os.getenv("AWS_KAFKA_GROUP_ID"),
                    security_protocol="PLAINTEXT",
                    sasl_mechanism=None,
                    sasl_username=None,
                    sasl_password=None
                ),
                s3_settings=S3Settings(
                    bucket=os.getenv("S3_BUCKET"),
                    prefix=os.getenv("S3_PREFIX"),
                    kms_key_id=os.getenv("S3_KMS_KEY_ID")
                ),
                sqs_settings=SqsSettings(
                    queue_url=os.getenv("SQS_QUEUE_URL"),
                )
            )
        except (KeyError, ValidationError) as e:
            raise RuntimeError(f"Configuración invalidad: {e}") from e


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    return AppSettings.load()
