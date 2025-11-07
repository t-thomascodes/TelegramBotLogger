from decimal import Context
from itertools import product
from time import localtime
from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, filters, ContextTypes, MessageHandler
from datetime import time
from database import post_to_datbase
from config import TELEGRAM_BOT_NAME, TELEGRAM_API_KEY


BOT_TOKEN = TELEGRAM_API_KEY
BOT_USERNAME = TELEGRAM_BOT_NAME


# Conversation Handler Code 

# Define conversation states
USER_ACTIVITY, PRODUCTIVE_FLAG = range(2)

#Define valid prodictive states 
productive_states =["productive","neutral","not productive"]

# Entry point: /log
async def start_logger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! What have you been working on?")
    return USER_ACTIVITY

# Step 1: Capture activity
async def ask_user_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["activity"] = update.message.text
    await update.message.reply_text("Got it! Were you productive or not?")
    return PRODUCTIVE_FLAG

# Step 2: Capture productivity label
async def verify_productivity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["productivity"] = update.message.text.lower().strip()
    productivity = context.user_data["productivity"]

    if productivity not in productive_states:
        await update.message.reply_text("Please log activity as productive, not productive, or neutral")
        return PRODUCTIVE_FLAG
    else:

        activity = context.user_data["activity"]

        await update.message.reply_text(f"Logged. Activity: {activity}, Productivity: {productivity}. ✅")

        #Logs in database
        post_to_datbase(activity.lower(),productivity.lower())

        return ConversationHandler.END

# Fallback: cancel the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Log canceled. Type /log to start again.")
    return ConversationHandler.END

# Conversation handler definition
activity_conversation = ConversationHandler(
    entry_points=[CommandHandler("log", start_logger)],
    states={
        USER_ACTIVITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_user_activity)],
        PRODUCTIVE_FLAG: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_productivity)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)


    



# # Commands

# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     timestamp: int = update.message.date
#     print(f'User ({update.message.chat.id}) started the bot at {timestamp}')
#     await update.message.reply_text("Hello! Thank you for chatting with me! I will help your productivity!")

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Every 30 minutes I will ask you what you are doing! Just reply and I will store it")


# #Responses 
    
# def handle_response(text: str) -> str:
#     processed: str = text.lower()

#     if 'hello' in processed:
#         return 'Hey there!'
    
#     if 'i love python' in processed:
#         return 'Remember to subscribe'
    
#     return 'I do not understand what you wrote'
    

# # Messages

# # async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     message_type: str = update.message.chat.type
# #     text: str = update.message.text
# #     timestamp: int = update.message.date

# #     print(f'User ({update.message.chat.id}) in {message_type}: "{text}" at {timestamp}')

# #     # post_to_datbase(text)


# #     if message_type == 'group':
# #         if BOT_USERNAME in text:
# #             new_text: str = text.replace(BOT_USERNAME, '').strip()
# #             response: str = handle_response(new_text)
# #         else:
# #             return 
# #     else:
# #         response: str = handle_response(text)
# #         post_to_datbase(text)

# #     print('Bot:', response)
# #     await update.message.reply_text(response)


# # async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     print(f'Update {update} caused error: {context.error}')



# # Scheduled Reminders

# async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
#     """Send a reminder message to the user"""
#     job = context.job
#     await context.bot.send_message(
#         chat_id=job.chat_id, 
#         text="📝 What are you working on right now?"
#     )

# async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Start sending periodic reminders at specific times"""
#     chat_id = update.effective_chat.id
    
#     # Remove any existing jobs for this chat to avoid duplicates
#     current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
#     for job in current_jobs:
#         job.schedule_removal()
    
#     # Generate times from 8:00 AM to 10:00 PM, every 30 minutes
#     reminder_times = []
#     for hour in range(8, 22):  # 8 to 21 (8 AM to 9 PM)
#         reminder_times.append(time(hour=hour, minute=0))   # On the hour
#         reminder_times.append(time(hour=hour, minute=30))  # Half past
    
#     # Add the final 10:00 PM time
#     reminder_times.append(time(hour=22, minute=0))
    
#     # Schedule a daily job for each time
#     for reminder_time in reminder_times:
#         context.job_queue.run_daily(
#             send_reminder,
#             time=reminder_time,
#             chat_id=chat_id,
#             name=str(chat_id)  # Same name so they all get removed together
#         )
    
#     await update.message.reply_text(
#         f"✅ Reminders activated! I'll check in {len(reminder_times)} times daily from 8:00 AM to 10:00 PM."
#     )


# async def resume_reminders(context: ContextTypes.DEFAULT_TYPE):
#     """Resume reminders after flow state ends"""

#     chat_id = context.job.chat_id

#     current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
#     for job in current_jobs:
#         job.schedule_removal()
    
#     # Generate times from 8:00 AM to 10:00 PM, every 30 minutes
#     reminder_times = []
#     for hour in range(8, 22):  # 8 to 21 (8 AM to 9 PM)
#         reminder_times.append(time(hour=hour, minute=0))   # On the hour
#         reminder_times.append(time(hour=hour, minute=30))  # Half past
    
#     # Add the final 10:00 PM time
#     reminder_times.append(time(hour=22, minute=0))
    
#     # Schedule a daily job for each time
#     for reminder_time in reminder_times:
#         context.job_queue.run_daily(
#             send_reminder,
#             time=reminder_time,
#             chat_id=chat_id,
#             name=str(chat_id)  # Same name so they all get removed together
#         )
#     await context.bot.send_message(
#         chat_id = chat_id,
#         text = "Flow state ended! Reminders are back on"
#     )



# async def stop_remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Stop sending reminders"""
#     chat_id = update.effective_chat.id
#     current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    
#     if not current_jobs:
#         await update.message.reply_text("You don't have any active reminders.")
#         return
    
#     for job in current_jobs:
#         job.schedule_removal()
    
#     await update.message.reply_text("⏹️ Reminders stopped.") 

# async def start_flowstate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Start the flowstate command"""
#     chat_id = update.effective_chat.id
#     current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        
#     if not current_jobs:
#         await update.message.reply_text("You are not in reminder mode. Use /remind to start.")
#         return
    
#     for job in current_jobs:
#         job.schedule_removal()

#     await update.message.reply_text("Flowstate begun. No reminders will be sent for 2 hours")
    
#     # Resumes reminders in 2 hours         
#     context.job_queue.run_once(
#         resume_reminders,
#         when=7200,
#         chat_id=chat_id,
#         name=f"flowstate_{chat_id}"  # Same name so they all get removed together
#     )

# async def stop_flowstate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Stops the flowstate command"""

#     chat_id = update.effective_chat.id

#     current_job = context.job_queue.get_jobs_by_name(f"flowstate_{chat_id}")

#     if not current_job: 
#         await update.message.reply_text("You are not in flowstate mode. Use/flowstate to start.")
#         return 
    
#     for job in current_job:
#         job.schedule_removal()
    
#     # No update message because resume_reminders sends one already 
#     context.job_queue.run_once(
#         resume_reminders,
#         when=0,
#         chat_id=chat_id,
#         name = str(chat_id)
#     )





if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(BOT_TOKEN).build()
    
    #Commands
    # app.add_handler(CommandHandler('start',start_command)) 
    # app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('remind', remind_command))
    # app.add_handler(CommandHandler('stop', stop_remind_command))
    # app.add_handler(CommandHandler('flowstate', start_flowstate_command))
    # app.add_handler(CommandHandler('stop_flowstate', stop_flowstate_command))
    app.add_handler(activity_conversation)


    #Messages
    # app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    # Errorrs 
    # app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=5)
