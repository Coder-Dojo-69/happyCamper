import os
from typing import Final
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

from globe_debunk_dict  import globe_debunk_dictionary
from text_response import text_response_dict
from commands_dictionary import commands_dict

pc_host = False

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

TOKEN: Final = bot_token

BOT_USERNAME: Final = '@camper69bot'

'bot name : Happy Camper'

if pc_host:
    system_path = r"C:\app_dev\telegram_bot\happyCamper\source\pics\\"
    system_path_vid = r"C:\app_dev\telegram_bot\happyCamper\source\videos\\"
    # print(system_path)
    # print(system_path_vid)
else:
    system_path = f"/home/dojopython/happyCamper/source/pics/"
    system_path_vid = f"/home/dojopython/happyCamper/source/videos/"

#: Commands
async def start_command(update: Update, context: CallbackContext):
    # Reply to the /start command without mentioning the bot's username
    await update.message.reply_text(commands_dict['/start'], parse_mode=ParseMode.MARKDOWN)

# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    #++ |=== PRINT MESSAGES ===| ++#

    # reply_text = """Welcome to Camper Bot\n\nNavigation Commands:\n\n/start\n     /about\n/debunk\n     /debunk_list\n/response\n    /response_list\n/help\n   /ask\n   /FAQ"""

    # await update.message.reply_text(reply_text)

async def command_handler(update: Update, context: CallbackContext):
    command = update.message.text.split()[0]  #: Extract the command from the message
    command = command.replace(BOT_USERNAME, '').strip()  # Remove the bot's username if present
    if command in commands_dict:
        await update.message.reply_text(commands_dict[command])
    else:
        await update.message.reply_text("Command not found.")


#: Responses

def handle_response(text: str) -> str:

    processed: str = text.lower()

    # for key, text_response in text_response_dict.items():
        
    #     if text_response['text'] in processed:

    #         return text_response['response']
        
    # Flag to track if a response has been sent
    response_sent = False
    
    for key, values in text_response_dict.items():
        text = values['text']
        text_comb = values['text_comb']
        text_response = values['response']

        for text_string in text:
            if text_string.lower() in processed.lower() and not response_sent:
                
                response_sent = True  # Set the flag to True

                return text_response

        if sum(word.lower() in processed.lower() for word in text_comb) >= 2 and not response_sent:
            response_sent = True  # Set the flag to True
            
            return text_response

    # if 'motion of the earth' in processed:
        # return f'they tried to measure the motion of the earth but failed in the Michaelson Morley experiment using interferometry and mirrors to measure displacement of light as it "motioned" through the Aether'

    # return "Say that in another way"

# Function to handle the message
# async def handle_message(update: Update, context: CallbackContext):
    # message_type = update.message.chat.type
    # text = update.message.text


#: special functions

#: Handle message

async def handle_message(update: Update, context: CallbackContext):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Flag to track if a response has been sent
    response_sent = False

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    for key, values in globe_debunk_dictionary.items():
        string_list = values['string_list']
        caption = values['caption']
        image_file = values['file']
        video_file = values.get('video', None)
        search_words = values['search_words']

        for debunk_string in string_list:
            if debunk_string.lower() in text.lower() and not response_sent:
                image_path = f"{system_path}{image_file}"
                if os.path.exists(image_path):
                    await update.message.reply_photo(
                        photo=open(image_path, 'rb'),
                        caption=caption)
                    response_sent = True  # Set the flag to True
                else:
                    print("Image file not found.")

                if video_file:
                    video_path = f"{system_path_vid}{video_file}"
                    if os.path.exists(video_path):
                        await update.message.reply_video(
                            video=open(video_path, 'rb'),
                            caption=caption)
                        response_sent = True  # Set the flag to True
                    else:
                        print("Video file not found.")

        if sum(word.lower() in text.lower() for word in search_words) >= 2 and not response_sent:
            if video_file:
                video_path = f"{system_path_vid}{video_file}"
                if os.path.exists(video_path):
                    await update.message.reply_video(
                        video=open(video_path, 'rb'),
                        caption=caption)
                    response_sent = True  # Set the flag to True
                else:
                    print("Video file not found.")
            else:
                image_path = f"{system_path}{image_file}"
                if os.path.exists(image_path):
                    await update.message.reply_photo(
                        photo=open(image_path, 'rb'),
                        caption=caption)
                    response_sent = True  # Set the flag to True
                else:
                    print("Image file not found.")

    await update.message.reply_text(response)

#: Errors

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


#: interface

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    #: Commands
    # app.add_handler(CommandHandler('start', start_command))
    #: Adding command handlers dynamically
    for command in commands_dict:
        app.add_handler(CommandHandler(command[1:], command_handler))


    #: Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))


    #: Errors
    app.add_error_handler(error)


    #: Updates
    print('Polling...')
    app.run_polling(poll_interval=3)

