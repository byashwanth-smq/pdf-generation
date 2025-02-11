checkpoint_code_groups = {
    3: '4', 7: '4',
    0: '5', 15: '5', 19: '5',
    10: '6', 20: '6', 31: '6', 28: '6', 36: '6',
    2: '7', 17: '7',
    6: '8', 18: '8', 25: '8',
    12: '9', 8: '9', 29: '9', 4: '9',
    1: '10', 22: '10',
    9: '11', 23: '11'
}

table_headers = {
    3: [{"question": "question_description"}, {"response": "selected_answer"}, {"image": None}],
    4: [{"question": "question_description"}, {"quantity": "quantity"}, {"comment": "comment"}, {"image": None}],
    5: [{"question": "question_description"}, {"response": "selected_answer"}, {"comment": "comment"}, {"action_taken": "action_taken"}, {"image": None}],
    6: [{"dish_name": "dynamic_question"}, {"category": "category"}, {"question": "question_description"}, {"response": "selected_answer"}, {"after_90_min": "end_temp_or_storage_temp"}, {"comment": "comment"}],
    7: [{"question": "question_description"}, {"not_in_service": "not_in_service"}, {"equipment_temperature": "selected_answer"}, {"product_temperature": "product_temp"}, {"comment": "comment"}, {"action_taken": "action_taken"}, {"image": None}],
    8: [{"mog_name": "dynamic_question"}, {"quantity": "quantity"}, {"unit": "unit"}, {"start_temp": "start_temp"}, {"end_temp": "end_temp_or_storage_temp"}, {"comment": "comment"}, {"action_taken": "action_taken"}, {"image": None}],
    9: [{"mog_name": "dynamic_question"}, {"unit": "unit"}, {"duration": "minutes"}, {"sanitizer_concentration": "sanitizer_concentration"}, {"question": "question_description"}, {"response": "selected_answer"}, {"comment": "comment"}, {"action_taken": "action_taken"}, {"image": None}],
    10: [{"mog_name": "dynamic_question"}, {"quantity": "quantity"}, {"unit": "unit"}, {"duration": "minutes"}, {"sanitizer_concentration": "sanitizer_concentration"}, {"question": "question_description"}, {"response": "selected_answer"}, {"comment": "comment"}, {"action_taken": "action_taken"}, {"image": None}],
    11: [{"dish_name": "dynamic_question"}, {"quantity": "quantity"}, {"start_end_time": "start_time_end_time"}, {"category": "category"}, {"cooking_completion_temp": "start_temp"}, {"reheating_temp": "end_temp_or_storage_temp"}, {"question": "question_description"}, {"response": "selected_answer"}, {"comment": "comment"}, {"action_taken": "action_taken"}, {"image": None}],
    12: [
    {"sub_checkpoint": "question_description"},
    {"response": "selected_answer"},
    {"image": None},
    {"quantity": "quantity"},
    {"comment": "comment"},
    {"action_taken": "action_taken"},
    {"question": "question_description"},
    {"dish_name": "dynamic_question"},
    {"category": "category"},
    {"after_90_min": "end_temp_or_storage_temp"},
    {"not_in_service": "not_in_service"},
    {"equipment_temperature": "selected_answer"},
    {"product_temperature": "product_temp"},
    {"mog_name": "dynamic_question"},
    {"unit": "unit"},
    {"start_temp": "start_temp"},
    {"end_temp": "end_temp_or_storage_temp"},
    {"duration": "minutes"},
    {"sanitizer_concentration": "sanitizer_concentration"},
    {"qty": "quantity"},
    {"start_end_time": "start_time_end_time"},
    {"cooking_completion_temp": "start_temp"},
    {"reheating_temp": "end_temp_or_storage_temp"}
]
}