import json

# Load the JSON data from a file
with open('pdf-generation_11.json', 'r') as file:
    data = json.load(file)

# Function to recursively extract unique "code" values and group them based on response details count
def group_codes_by_response_details_count(data, grouped_codes):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'code' and 'response_details' in data:
                for response_key, response_value in data['response_details'].items():
                    key_count = len(response_value)  # Count the number of keys in each response item
                    if key_count not in grouped_codes:
                        grouped_codes[key_count] = []
                    grouped_codes[key_count].append(data['code'])
            else:
                group_codes_by_response_details_count(value, grouped_codes)
    elif isinstance(data, list):
        for item in data:
            group_codes_by_response_details_count(item, grouped_codes)

# Initialize a dictionary to store codes grouped by the count of keys in response details
grouped_codes = {}

# Extract codes and group them by the count of keys in response details
group_codes_by_response_details_count(data, grouped_codes)

# Create the final JSON structure
final_json = {
    "code_groups": grouped_codes
}

# Print the result in JSON format
# print(json.dumps(final_json, indent=4))

table_code = "6"

if table_code is not None:
    code_groups = final_json.get("code_groups")
    print(code_groups)
    if code_groups:
        try:
            table_code_int = int(table_code)
            found = False
            for key, values in code_groups.items():
                if table_code_int in values:
                    print(key)  # Print only the key
                    found = True
                    # If you only need the first occurrence, you can break here:
                    # break
            if not found:
                print(f"Value {table_code} not found in any code group.")
        except ValueError:
            print(f"Invalid table_code: {table_code}. Cannot convert to integer.")
    else:
        print("code_groups key not found or empty in final_json")
else:
    print("No 'code' key found in table_data.")