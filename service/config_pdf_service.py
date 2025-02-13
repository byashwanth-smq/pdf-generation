checkpoint_code_groups = {
    3: '4', 7: '4',
    0: '5', 15: '5', 19: '5',
    10: '6', 20: '6', 31: '6', 28: '6', 36: '6',  #todo - adjust this 31:6 - its wrong
    2: '7', 17: '7',
    6: '8', 18: '8', 25: '8',
    12: '9', 8: '9', 29: '9', 4: '9',
    1: '10', 22: '10',
    9: '11', 23: '11',
    100: '12'
}

table_col = {
    "question": "question_description",
    "response": "selected_answer",
    "image": None,
    "quantity": "quantity",
    "comment": "comment",
    "action_taken": "action_taken",
    "dish_name": "dynamic_question",
    "category": "category",
    "after_90_min": "end_temp_or_storage_temp",
    "not_in_service": "not_in_service",
    "equipment_temperature": "selected_answer",
    "product_temperature": "product_temp",
    "mog_name": "dynamic_question",
    "unit": "unit",
    "start_temp": ["start_temp", "selected_answer"],
    "end_temp": ["end_temp_or_storage_temp", "product_temp"],
    "duration": "minutes",
    "sanitizer_concentration": "sanitizer_concentration",
    "start_end_time": ["start_time", "end_time"],
    "cooking_completion_temp": ["start_temp", "selected_answer"],
    "reheating_temp": "end_temp_or_storage_temp"
}

table_headers = {
    3: [{"question": table_col["question"]}, {"response": table_col["response"]}, {"image": table_col["image"]}],
    4: [{"question": table_col["question"]}, {"quantity": table_col["quantity"]}, {"comment": table_col["comment"]}, {"image": table_col["image"]}],
    5: [{"question": table_col["question"]}, {"response": table_col["response"]}, {"comment": table_col["comment"]}, {"action_taken": table_col["action_taken"]}, {"image": table_col["image"]}],
    6: [{"dish_name": table_col["dish_name"]}, {"category": table_col["category"]}, {"question": table_col["question"]}, {"response": table_col["response"]}, {"after_90_min": table_col["after_90_min"]}, {"comment": table_col["comment"]}],
    7: [{"question": table_col["question"]}, {"not_in_service": table_col["not_in_service"]}, {"equipment_temperature": table_col["equipment_temperature"]}, {"product_temperature": table_col["product_temperature"]}, {"comment": table_col["comment"]}, {"action_taken": table_col["action_taken"]}, {"image": table_col["image"]}],
    8: [{"mog_name": table_col["mog_name"]}, {"quantity": table_col["quantity"]}, {"unit": table_col["unit"]}, {"start_temp": table_col["start_temp"]}, {"end_temp": table_col["end_temp"]}, {"comment": table_col["comment"]}, {"action_taken": table_col["action_taken"]}, {"image": table_col["image"]}],
    9: [{"mog_name": table_col["mog_name"]}, {"unit": table_col["unit"]}, {"duration": table_col["duration"]}, {"sanitizer_concentration": table_col["sanitizer_concentration"]}, {"question": table_col["question"]}, {"response": table_col["response"]}, {"comment": table_col["comment"]}, {"action_taken": table_col["action_taken"]}, {"image": table_col["image"]}],
    10: [{"mog_name": table_col["mog_name"]}, {"quantity": table_col["quantity"]}, {"unit": table_col["unit"]}, {"duration": table_col["duration"]}, {"sanitizer_concentration": table_col["sanitizer_concentration"]}, {"question": table_col["question"]}, {"response": table_col["response"]}, {"comment": table_col["comment"]}, {"action_taken": table_col["action_taken"]}, {"image": table_col["image"]}],
    11: [{"dish_name": table_col["dish_name"]}, {"quantity": table_col["quantity"]}, {"start_end_time": table_col["start_end_time"]}, {"category": table_col["category"]}, {"cooking_completion_temp": table_col["cooking_completion_temp"]}, {"reheating_temp": table_col["reheating_temp"]}, {"question": table_col["question"]}, {"response": table_col["response"]}, {"comment": table_col["comment"]}, {"action_taken": table_col["action_taken"]}, {"image": table_col["image"]}],
    12: [
        {"sub_checkpoint": table_col["question"]},
        {"response": table_col["response"]},
        {"image": table_col["image"]},
        {"quantity": table_col["quantity"]},
        {"comment": table_col["comment"]},
        {"action_taken": table_col["action_taken"]},
        {"question": table_col["question"]},
        {"dish_name": table_col["dish_name"]},
        {"category": table_col["category"]},
        {"after_90_min": table_col["after_90_min"]},
        {"not_in_service": table_col["not_in_service"]},
        {"equipment_temperature": table_col["equipment_temperature"]},
        {"product_temperature": table_col["product_temperature"]},
        {"mog_name": table_col["mog_name"]},
        {"unit": table_col["unit"]},
        {"start_temp": table_col["start_temp"]},
        {"end_temp": table_col["end_temp"]},
        {"duration": table_col["duration"]},
        {"sanitizer_concentration": table_col["sanitizer_concentration"]},
        {"qty": table_col["quantity"]},
        {"start_end_time": table_col["start_end_time"]},
        {"cooking_completion_temp": table_col["cooking_completion_temp"]},
        {"reheating_temp": table_col["reheating_temp"]}
    ]
}
