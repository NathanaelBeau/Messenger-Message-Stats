from transformers import pipeline

def get_label_and_score_message(message, analyzer):

    result = analyzer(
        message,
        return_all_scores=True
    )

    # Use the max function with a custom key function to find the dictionary with the maximum 'score'
    max_score_dict = max(result[0], key=lambda x: x['score'])

    return max_score_dict

def get_analyzer():

    analyzer = pipeline("text-classification", model="cmarkea/distilcamembert-base-sentiment")

    return analyzer


def get_messages_with_one_star_by_user(messages, names):
    user_messages_one_star = {}

    for index, message in enumerate(messages):

        if not isinstance(message, str):
            continue

        label_and_score_message = get_label_and_score_message(message, analyzer=get_analyzer())
        label = label_and_score_message['label']
        score = label_and_score_message['score']
        user = names[index]

        # Initialize a user's message list if it doesn't exist
        if user not in user_messages_one_star:
            user_messages_one_star[user] = []


        # Add the message to the user's list if it has the label '1 star'
        if label == '1 star':
            user_messages_one_star[user].append({'message': message, 'score': score})

    return user_messages_one_star

def get_top_hate_messages_for_all_users(user_messages_with_one_star, number_of_messages=10):
    # Find the top 10 messages by score for '1 star' label for each user
    top_10_messages_by_user = {}
    for user, messages in user_messages_with_one_star.items():
        # Sort the user's messages by score in descending order
        sorted_messages = sorted(messages, key=lambda x: x['score'], reverse=True)
        # Take the top 10 messages
        top_10_messages_by_user[user] = sorted_messages[:number_of_messages]

    # Combine the top 10 messages for all users
    all_top_10_messages = [message for messages in top_10_messages_by_user.values() for message in messages]

    # Sort the combined top 10 messages for all users by score
    all_top_10_messages = sorted(all_top_10_messages, key=lambda x: x['score'], reverse=True)

    # Return the top 10 messages for all users
    return all_top_10_messages[:number_of_messages]


def get_top_hate_messages_by_user(user_messages_with_one_star, number_of_messages=10):

    # Find the top 10 messages by score for '1 star' label for each user
    top_10_messages_by_user = {}
    for user, messages in user_messages_with_one_star.items():
        # Sort the user's messages by score in descending order
        sorted_messages = sorted(messages, key=lambda x: x['score'], reverse=True)
        # Take the top 10 messages
        top_10_messages_by_user[user] = sorted_messages[:10]

    return top_10_messages_by_user