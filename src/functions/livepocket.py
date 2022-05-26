import json
import requests
from bs4 import BeautifulSoup
import datetime
from dateutil import parser
import math
import uuid

import schemas.request as request_schema
from schemas import detail as schema_detail


_timezone = datetime.timezone(datetime.timedelta(hours=9))


def get_livepocket_data(url: str) -> schema_detail.EventDetail:
    req = requests.get(url).text
    bs = BeautifulSoup(req, 'html.parser', from_encoding='utf-8')
    raw_data: str = bs.find("input", {"id": "event_ticket_groups"})["value"]
    data: list = json.loads(raw_data)
    title: str = bs.select_one(
        "#eventTitle > section > h1").get_text()
    ticket_data: dict = {
        "title": title,
        "data": data
    }
    ticket_detail: list = []
    application_detail: list = []

    for i in ticket_data["data"]:
        _uuid: str = str(uuid.uuid4())
        is_released: bool
        if i["group_name"] == "先着販売受付":
            is_lottery = False
        elif i["group_name"] == "抽選販売受付":
            is_lottery = True

        start_time: int = parse_datestr(i["group_starttime"], _timezone)
        end_time: int = parse_datestr(i["group_endtime"], _timezone)
        dt = datetime.datetime.now(_timezone).timestamp()
        if start_time < dt:
            is_released = True
        else:
            is_released = False
        apply_detail = schema_detail.ApplyDetail(
            id=_uuid, name=i["group_name"], lottery=is_lottery, released=is_released, start_time=start_time, end_time=end_time)
        application_detail.append(apply_detail)

        for j in i["tickets_info"]:
            start_time: int = parse_datestr(j["starttime"], _timezone)
            end_time: int = parse_datestr(j["endtime"], _timezone)
            dt = datetime.datetime.now(_timezone).timestamp()
            if i["group_name"] == "先着販売受付":
                is_lottery = False
            elif i["group_name"] == "抽選販売受付":
                is_lottery = True

            if start_time < dt:
                is_released = True
            else:
                is_released = False

            detail = schema_detail.TicketDetail(
                id=_uuid, name=j["name"], pricing=j["price"], start_time=start_time, end_time=end_time, stock=j["ticket_stock"], released=is_released, purchase_limit=j["limit_max"], limited=j["purchase_limited"])
            ticket_detail.append(detail)

    result = schema_detail.EventDetail(
        name=ticket_data["title"], url=url, tickets=ticket_detail, applications=application_detail)
    return result


def parse_datestr(date_str: str, tzinfo) -> int:
    parsed_str = parser.parse(date_str).replace(tzinfo=tzinfo).timestamp()
    result = math.floor(parsed_str)
    return result
