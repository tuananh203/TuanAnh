from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import json
import re
import math

with open("digestive_data/benh-tieu-hoa.json", "r", encoding="utf8") as f:
    list_benh = list(json.loads(f.read()))

with open("digestive_data/trieu_chung.json", "r", encoding="utf8") as f:
    list_trieu_chung = list(json.loads(f.read()))

with open("digestive_data/case_benh.json", "r", encoding="utf8") as f:
    list_case_benh = list(json.loads(f.read()))

with open("digestive_data/do_tuong_dong.json", "r", encoding="utf8") as f:
    dict_do_tuong_dong = dict(json.loads(f.read()))

USER_SYMPTONS = ["p", "d", "t", "n", "c", "dd", "h"]
WEIGHT_SYMPTONS = [5, 7, 3, 3, 1, 7, 5]


def tim_kiem_benh(ten_benh: str):
    for benh in list_benh:
        if ten_benh in benh["ten"]:
            return benh
    return None


def normalize_text(text: str) -> str:
    text = re.sub(r"[\[\]'-()\"#/@;:<>{}`+=~|.!?,]", " ", text.strip().lower())
    text = re.sub(r"\s+", " ", text)
    return text


class ActionAskThongTin(Action):
    def name(self) -> Text:
        return "action_ask_thong_tin"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ten_benh = normalize_text(tracker.get_slot("benh_tieu_hoa"))
        benh = tim_kiem_benh(ten_benh=ten_benh)
        if benh == None:
            dispatcher.utter_message(
                text="Xin lỗi! Có thể bệnh mà bạn nói không nằm trong bộ nhớ của chúng tôi hoặc nó không phải bệnh liên quan đến đường tiêu hóa."
            )
        else:
            dispatcher.utter_message(
                text=f"Tên bệnh: {ten_benh}\n- Khái niệm: {benh['khai_niem']}\n- Nguyên nhân: {benh['nguyen_nhan']}\n- Triệu chứng: {benh['trieu_chung']}\n- Phương pháp điều trị: {benh['phuong_phap_dieu_tri']}"
            )
        return []


class ActionAskKhaiNiem(Action):
    def name(self) -> Text:
        return "action_ask_khai_niem"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tracker.slots.keys()
        ten_benh = normalize_text(tracker.get_slot("benh_tieu_hoa"))
        benh = tim_kiem_benh(ten_benh=ten_benh)
        if benh == None:
            dispatcher.utter_message(
                text="Xin lỗi! Có thể bệnh mà bạn nói không nằm trong bộ nhớ của chúng tôi hoặc nó không phải bệnh liên quan đến đường tiêu hóa."
            )
        else:
            dispatcher.utter_message(
                text=f"Khái niệm bệnh {ten_benh}: {benh['khai_niem']}"
            )
        return []


class ActionAskNguyenNhan(Action):
    def name(self) -> Text:
        return "action_ask_nguyen_nhan"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ten_benh = normalize_text(tracker.get_slot("benh_tieu_hoa"))
        benh = tim_kiem_benh(ten_benh=ten_benh)
        if benh == None:
            dispatcher.utter_message(
                text="Xin lỗi! Có thể bệnh mà bạn nói không nằm trong bộ nhớ của chúng tôi hoặc nó không phải bệnh liên quan đến đường tiêu hóa."
            )
        else:
            dispatcher.utter_message(
                text=f"Nguyên nhân bệnh {ten_benh}: {benh['nguyen_nhan']}"
            )
        return []


class ActionAskTrieuChung(Action):
    def name(self) -> Text:
        return "action_ask_trieu_chung"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ten_benh = normalize_text(tracker.get_slot("benh_tieu_hoa"))
        benh = tim_kiem_benh(ten_benh=ten_benh)
        if benh == None:
            dispatcher.utter_message(
                text="Xin lỗi! Có thể bệnh mà bạn nói không nằm trong bộ nhớ của chúng tôi hoặc nó không phải bệnh liên quan đến đường tiêu hóa."
            )
        else:
            dispatcher.utter_message(
                text=f"Triệu chứng bệnh {ten_benh}: {benh['trieu_chung']}"
            )
        return []


class ActionAskPhuongPhapDieuTri(Action):
    def name(self) -> Text:
        return "action_ask_phuong_phap_dieu_tri"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ten_benh = normalize_text(tracker.get_slot("benh_tieu_hoa"))
        benh = tim_kiem_benh(ten_benh=ten_benh)
        if benh == None:
            dispatcher.utter_message(
                text="Xin lỗi! Có thể bệnh mà bạn nói không nằm trong bộ nhớ của chúng tôi hoặc nó không phải bệnh liên quan đến đường tiêu hóa."
            )
        else:
            dispatcher.utter_message(
                text=f"Phương pháp điều trị bệnh {ten_benh}: {benh['phuong_phap_dieu_tri']}"
            )
        return []


class ActionAskSlotsValues(Action):
    def name(self) -> Text:
        return "action_ask_slots_values"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_symptons = {k: v for k, v in tracker.slots.items() if k in USER_SYMPTONS}
        if self.Tat_Ca_Trieu_Chung_Deu_Binh_Thuong(user_symptons):
            dispatcher.utter_message(
                "Chúc mừng bạn! Bạn hoàn toàn không bị bệnh gì cả 😁"
            )
        else:
            best_match = self.best_match(user_symptons)
            ten_benh, du_doan = self.find_benh(user_symptons, best_match)
            buttons = [
                {
                    "title": "Thông tin",
                    "payload": '/thong_tin{"benh_tieu_hoa":"' + ten_benh + '"}',
                },
                {
                    "title": "Cách chữa",
                    "payload": '/phuong_phap_dieu_tri{"benh_tieu_hoa":"'
                    + ten_benh
                    + '"}',
                },
            ]
            if du_doan >= 0.9:
                dispatcher.utter_message(
                    f"Bạn chắc chắn bị {ten_benh}.😱", buttons=buttons
                )
            elif du_doan >= 0.8:
                dispatcher.utter_message(
                    f"Bạn tỷ lệ cao bị {ten_benh}.😨", buttons=buttons
                )
            elif du_doan >= 0.5:
                dispatcher.utter_message(
                    f"Bot nghi ngờ bạn bị {ten_benh}.🤔", buttons=buttons
                )
            else:
                dispatcher.utter_message(
                    f"Xin lỗi 😞! Bot chưa thể xác định được bệnh mà bạn gặp phải.\nBạn cần theo dõi thêm các triệu chứng để Bot có thể xác định bệnh đúng hơn"
                )
        return [SlotSet(k, None) for k, v in tracker.slots.items()]

    @staticmethod
    def Tat_Ca_Trieu_Chung_Deu_Binh_Thuong(symptons: dict) -> bool:
        for k, v in symptons.items():
            if not str(v).endswith("01"):
                return False
        return True

    @staticmethod
    def find_benh(user_symptons: dict, best_match: list):
        tmp = []
        for sympton in best_match:
            s = 0.0
            for code, weight in zip(USER_SYMPTONS, WEIGHT_SYMPTONS):
                if user_symptons[code] in dict_do_tuong_dong:
                    s += weight * dict_do_tuong_dong[user_symptons[code]][sympton[code]]
                else:
                    count = 0
                    s2 = 0
                    try:
                        for i in user_symptons[code].split():
                            s2 += dict_do_tuong_dong[i][sympton[code]]
                            count += 1
                    except:
                        pass
                    s += weight * (s2 / count)
            tmp.append((sympton["benh"], s / sum(WEIGHT_SYMPTONS)))
        tmp.sort(key=lambda x: x[1], reverse=True)
        return tmp[0]

    @staticmethod
    def compare(dict1: dict, dict2: dict) -> float:
        count = 0
        for i in USER_SYMPTONS:
            count += 1 if dict1[i] == dict2[i] else 0
        return count / len(USER_SYMPTONS)

    @staticmethod
    def best_match(user_symptons: dict) -> list:
        list_prop = [
            ActionAskSlotsValues.compare(user_symptons, case) for case in list_case_benh
        ]
        max_value = max(list_prop)
        list_best_match = [
            list_case_benh[i]
            for i, val in enumerate(list_prop)
            if math.isclose(max_value, val)
        ]
        return list_best_match


class ActionAskDone(Action):
    def name(self) -> Text:
        return "action_ask_done"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        slots = {k: v for k, v in tracker.slots.items()}
        count = 0
        user_trieu_chung = ""
        for rs in USER_SYMPTONS:
            if rs in slots and slots[rs]:
                count += 1
                for code in slots[rs].split():
                    user_trieu_chung += self.find_trieu_chung(code) + ", "
        if count:
            dispatcher.utter_message(
                f"Ngoài những triệu chứng {user_trieu_chung}bạn còn những biểu hiện gì khác không?"
            )
        else:
            dispatcher.utter_message("Bạn đang gặp những triệu chứng gì?")

    @staticmethod
    def find_trieu_chung(code: str) -> str:
        res = []
        for i in list_trieu_chung:
            if code == i["code"]:
                res.append(i["TC"])
        if len(res) == 0:
            return ""
        elif len(res) == 1:
            return res[0]
        else:
            return f"{res[0]} (hoặc {', '.join([i for i in res[1:]])})"


class ValidateChanDoanBenhForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_chan_doan_benh_form"

    def validate_done(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        res = {k: v for k, v in tracker.slots.items()}
        if "không" in str(slot_value):
            for slot in USER_SYMPTONS:
                if not res[slot]:
                    res[slot] = f"{slot.upper()}-01"
            res["done"] = True
            res["requested_slot"] = None
        else:
            res["done"] = None
            user_message = normalize_text(slot_value)
            user_symptoms = self.find_trieu_chung_code(user_message)
            if user_symptoms:
                for i in user_symptoms:
                    code = i.split("-")[0].lower()
                    if (
                        code in res
                        and isinstance(res[code], str)
                        and i not in res[code]
                    ):
                        res[code] += f" {i}"
                        res[code] = " ".join(sorted([j for j in res[code].split()]))
                    else:
                        res[code] = i
            else:
                dispatcher.utter_message(
                    f"Xin lỗi😓! Triệu chứng mà bạn vừa nhập hiện không có trong hệ thống.\nHệ thống của tôi sẽ cập nhập thông tin về triệu chứng này trong thời gian sớm nhất.👍"
                )
                with open(
                    "digestive_data/trieu_chung_moi.txt", "a+", encoding="utf8"
                ) as f:
                    f.write(user_message + "\n")
        return res

    @staticmethod
    def find_trieu_chung_code(text: str) -> str:
        res = []
        for tc in list_trieu_chung:
            if tc["TC"] in text:
                res.append(tc["code"])
        return res
