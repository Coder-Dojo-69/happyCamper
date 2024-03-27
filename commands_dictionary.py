from globe_debunk_dict import globe_debunk_dictionary
from text_response import text_response_dict
from faq_dict import faq_dict

debunk_list_str = ""

for idx, key in enumerate(globe_debunk_dictionary):
    debunk_list_str += f"/{key}"
    if idx < len(globe_debunk_dictionary) - 1:
        debunk_list_str += "\n\n"

# print(debunk_list_str)

response_list_str = ""

for idx, key in enumerate(text_response_dict):
    response_list_str += f"/{key}"
    if idx < len(text_response_dict) - 1:
        response_list_str += "\n\n"

# print(response_list_str)
        
additional_commands_dict = {}

# Iterate over the globe_debunk_dictionary
for key, value in globe_debunk_dictionary.items():
    command_key = f"/{key}"
    # Format the string for each debunk entry
    debunk_info = (
        "String List:\n    - " + ",\n    - ".join(value['string_list']) + "\n\n" +
        "Caption: \"" + value['caption'] + "\"\n\n" +
        "File: \"" + value['file'] + "\"\n\n" +
        "Combination Words: '" + "', '".join(value['search_words']) + "'"
    )

    # Add the formatted string to the additional_commands_dict under the key
    additional_commands_dict[command_key] = debunk_info

# Iterate over the text_response_dict
for key, value in text_response_dict.items():
    command_key = f"/{key}"
    
    # Format the string for each response entry
    response_info = (
        "Trigger Text: " + value['text'] + "\n" +
        "Response: " + value['response']
    )
    
    # Add the formatted string to the additional_commands_dict under the key
    additional_commands_dict[command_key] = response_info

faq_text = ""
for faq_id, faq_info in faq_dict.items():
    question = faq_info['question']
    answer = faq_info['answer']
    faq_text += f"[{question}](/faq_{faq_id})\n\n"

print(faq_text)

commands_dict = {
    
    '/start' : """Welcome to Camper Bot\n\nNavigation Commands:\n\n/start\n     /about\n/debunk\n     /debunk_list\n/response\n    /response_list\n/help\n   /submit\n   /FAQ""",
    
    '/about' : """I'm the HappyCamper that looks up at the stars and says the Earth is Flat\n\nAs a HappyCamper I will give you another perspective on the nature of our reality.\n\nThe reality, the terrain is important in knowing where we are and how life should be lived\n\nTo get you started here are the lists for the debunks and the responses this HappyCamper can generate based on member imput\n\n/debunk\n/debunk_list\n\n/response\n/response_list""",
    
    '/debunk' : """A debunk response can be generated through a list of catch-phrases. For example if a member types in 'there is no curve' this post will generate an automated response to the catch phrase 'there is no curve.'\n\nA combination of words can also generate automated responses.\n\nHere is a list of available debunks to trigger.\n\n/debunk_list""",
    
    '/debunk_list' : f"""Here are the details of each debunk including what the debunk is and how it is triggered\n\n{debunk_list_str}""",
    
    '/response' : """Automate responses based on trigger text/word\n\n/response_list""",

    '/response_list' : f"""Here is a list of available responses\n\n{response_list_str}""",
    
    '/help' : f"""Whenever you get stuck type in /start to get back on track.\n\nTo Report HappyCamper for not being happy contact https://t.me/happycamperdemo""",
    '/submit' : f"""Got your own debunk or auto-response sugestions please submit to https://t.me/happycamperdemo with @admin""",
    '/FAQ' : f"""Got Questions? Looking for Answers?\n\n/faq_list\n\n/help""",
    '/faq_list' : faq_text,

} | additional_commands_dict