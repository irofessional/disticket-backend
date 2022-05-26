from typing import Optional, List

from pydantic import BaseModel, Field
import enum


class TicketDetail(BaseModel):
    id: str = Field(None, example="e2f7c778-b201-405d-810c-125c57e19579",
                    description="申込種別判別用のuuid")
    name: str = Field(None, exapmple="前売チケット(D代事前徴収))",
                      description="チケットの券種の名前")
    pricing: int = Field(None, example=600, description="チケットの価格")
    start_time: int = Field(None, example=1645441200,
                            description="発売開始(申し込み開始)日時のUNIX秒")
    end_time: int = Field(None, example=1646438340,
                          description="購入締め切り(申し込み締め切り)日時のUNIX秒")
    stock: Optional[int] = Field(
        None, example=350, description="発売予定枚数(ライポケのみ)")
    purchase_limit: int = Field(None, example=1,
                                description="購入可能枚数(ライポケのみ)")
    limited: bool = Field(None, example=False,
                          description="購入制限(ライポケのみ)")


class ApplyDetail(BaseModel):
    id: str = Field(
        None, example="e2f7c778-b201-405d-810c-125c57e19579", description="申込種別判別用のuuid")
    name: str = Field(None, example="先着販売受付", description="申込種別の名前")
    lottery: bool = Field(None, example=False, description="抽選かそうでないか")
    released: bool = Field(None, example=False, description="申込/発売済みかどうか")
    start_time: int = Field(None, example=1645441200,
                            description="発売開始(申し込み開始)日時のUNIX秒")
    end_time: int = Field(None, example=1646438340,
                          description="購入締め切り(申し込み締め切り)日時のUNIX秒")


class EventDetail(BaseModel):
    name: str = Field(
        None, example="アンスリューム不定期公演 「アンderGround」 アングラよ永遠に、皆大集合SP!〜", description="イベントの名前")
    url: str = Field(
        None, example="https://t.livepocket.jp/e/1asgp", description="チケットサイトのURL")
    tickets: List[TicketDetail]
    applications: List[ApplyDetail]


class TicketSiteType(enum.Enum):
    livepocket = "livepocket"
    tiget = "tiget"