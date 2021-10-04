import telegram
import telegram.ext
from random import randint

QUESTION = 1
CORRECT = 2

def randomize_numbers(update_obj, context):
    # store the numbers in the context
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(0,1000), randint(0, 1000)
    # send the question
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']}+{context.user_data['rand_y']}")
# in the WELCOME state, check if the user wants to answer a question

def question(update_obj, context):
    # expected solution
    solution = int(context.user_data['rand_x']) + int(context.user_data['rand_y'])
    # check if the solution was correct
    if solution == int(update_obj.message.text):
        # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
        update_obj.message.reply_text("Correct answer!")
        return CORRECT
    else:
        # wrong answer, reply, send a new question, and loop on the QUESTION state
        update_obj.message.reply_text("Wrong answer :'(")
        # send another random numbers calculation
        randomize_numbers(update_obj, context)
        return QUESTION

# in the CORRECT state
def correct(update_obj, context):

    update_obj.message.reply_text("Glad it was useful! ")
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(f"See you {first_name}!, bye")
    return telegram.ext.ConversationHandler.END
