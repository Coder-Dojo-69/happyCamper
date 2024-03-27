import os
from typing import Final
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

from globe_debunk_dict  import globe_debunk_dictionary
from text_response import text_response_dict
from commands_dictionary import commands_dict

pc_host = True

if pc_host:
    bot_token = '7072536114:AAFu_tRw_scbk9O2uV2hoU_awr2SdzmXk8Q'
else:
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

    for key, text_response in text_response_dict.items():
        
        if text_response['text'] in processed:

            return text_response['response']

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
    # ContextTypes.DEFAULT_TYPE,
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return

    else:

        response: str = handle_response(text)

    #+++ |=== DEBUNKS OF GLOBE LIES ===| +++#
    #: Iterate over the dictionary
    for key, values in globe_debunk_dictionary.items():
        string_list = values['string_list']
        caption = values['caption']
        image_file = values['file']
        video_file = values.get('video', None)  # Check if video file is specified
        # print(video_file)
        search_words = values['search_words']

        #: Check if any of the strings are present in the message
        for debunk_string in string_list:
            if debunk_string.lower() in text.lower():
                #: Get the path to the image file
                image_path = f"{system_path}{image_file}"
                # print(image_path)

                #: Check if the image file exists
                if os.path.exists(image_path):
                    # print('image path does exist')
                    #: Reply with photo
                    await update.message.reply_photo(
                        photo=open(image_path, 'rb'),
                        caption=caption)
                else:
                    print("Image file not found.")

                #: Check if video file exists and send video
                if video_file:
                    video_path = f"{system_path_vid}{video_file}"
                    # print(video_path)
                    if os.path.exists(video_path):
                        # print('path exists', video_path)
                        await update.message.reply_video(
                            video=open(video_path, 'rb'),
                            caption=caption)
                    else:
                        print("Video file not found.")

        #: Check if any two search words are present in the message
        if sum(word.lower() in text.lower() for word in search_words) >= 2:
            if video_file:  # If video file is specified
                video_path = f"{system_path_vid}{video_file}"
                if os.path.exists(video_path):
                    await update.message.reply_video(
                        video=open(video_path, 'rb'),
                        caption=caption)
                else:
                    print("Video file not found.")
            else:  # If no video file, default to photo
                image_path = f"{system_path}{image_file}"
                if os.path.exists(image_path):
                    await update.message.reply_photo(
                        photo=open(image_path, 'rb'),
                        caption=caption)
                else:
                    print("Image file not found.")

    #:::: |=== DEBUNK /DEBUNK ===| ::::#
                
    

    # print("Bot:", response)

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

