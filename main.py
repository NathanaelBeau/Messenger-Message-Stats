from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

from utils import get_html_files
from hatometre import get_analyzer, get_messages_with_one_star_by_user, get_top_hate_messages_by_user, get_top_hate_messages_for_all_users

def count_number_pics_sent(soup):
    # Dictionary to store count of photos sent by each user
    photo_counts = {}

    # Extracting names and photos
    for div in soup.find_all('div', class_="_3-95 _a6-g"):
        name_div = div.find('div', class_="_2ph_ _a6-h _a6-i")
        photo_div = div.find('a', href=True, class_=lambda x: x and "messages/inbox" in x)

        if name_div and photo_div:  # If both a name and a photo link are found
            name = name_div.get_text()
            photo_counts[name] = photo_counts.get(name, 0) + 1  # Increment count for the user

    return photo_counts


def get_messages_names_dates(soup):
    # Lists to store data
    names = []
    messages = []
    dates = []

    # Extracting names, messages, and dates
    for div in soup.find_all('div', class_="_3-95 _a6-g"):
        name_div = div.find('div', class_="_2ph_ _a6-h _a6-i")
        message_div = div.find('div', class_="_2ph_ _a6-p")
        date_div = div.find('div', class_="_a72d")

        if name_div:
            names.append(name_div.get_text())
        else:
            names.append(None)

        if message_div:
            # Get all divs within the message_div
            message_subdivs = message_div.find_all('div', recursive=False)

            # Check for nested divs and extract message text
            message_text = None
            for msg_div in message_subdivs:
                nested_divs = msg_div.find_all('div')
                if nested_divs:
                    for nested_div in nested_divs:
                        if nested_div.get_text().strip():  # if nested div has non-empty text
                            message_text = nested_div.get_text().strip()
                            break
                if message_text:  # If we found a message, break out of outer loop
                    break

            messages.append(message_text)
        else:
            messages.append(None)

        if date_div:
            dates.append(date_div.get_text())
        else:
            dates.append(None)

    return names, messages, dates


def count_reaction_by_person(soup):
    reactions_by_person = defaultdict(int)

    for div in soup.find_all('div', class_="_3-95 _a6-g"):
        reactions_list = div.find('ul', class_="_a6-q")

        # If reactions exist for the message
        if reactions_list:
            reactors = [li.get_text()[1:] for li in reactions_list.find_all('li')]  # Removing the emoji before name

            for reactor in reactors:
                reactions_by_person[reactor] += 1

    return reactions_by_person

def count_reaction_by_type_by_person(soup):
    # Get number of reactions by user and type
    reactions_by_user = defaultdict(lambda: defaultdict(int))

    for reaction_li in soup.find_all('li'):
        # Splitting the reaction and the user (assuming the format is 😆Khaled Haiballa)
        reaction = reaction_li.get_text()[0]
        user = reaction_li.get_text()[1:]
        reactions_by_user[user][reaction] += 1

    return reactions_by_user


def count_reaction_on_messages(soup):
    # Dictionary to store the count of reactions each person got on their messages
    reactions_on_messages = defaultdict(int)

    for div in soup.find_all('div', class_="_3-95 _a6-g"):
        sender = div.find('div', class_="_2ph_ _a6-h _a6-i").get_text()
        reactions_list = div.find('ul', class_="_a6-q")

        # If reactions exist for the message
        if reactions_list:
            reactors = [li.get_text()[1:] for li in reactions_list.find_all('li')]  # Removing the emoji before name

            # Counting the reactions on the message for the sender
            reactions_on_messages[sender] += len(reactors)

    return reactions_on_messages

def count_users_messages(soup):
    # Dictionary to store the count of messages by each user
    messages_by_user = defaultdict(int)

    for div in soup.find_all('div', class_="_3-95 _a6-g"):
        sender_div = div.find('div', class_="_2ph_ _a6-h _a6-i")

        # Check if sender_div is not None before extracting text
        if sender_div:
            sender = sender_div.get_text()
            messages_by_user[sender] += 1

    return messages_by_user

def print_group_time_activity(soup):
    activity_by_hour = defaultdict(int)

    # Iterate over all timestamps
    for timestamp_div in soup.find_all('div', class_="_a72d"):
        timestamp_text = timestamp_div.get_text()
        # Assuming the timestamp format is like "sep 11, 2023 4:39:09pm", extracting the hour part
        hour = int(timestamp_text.split(' ')[3].split(':')[0])

        if 'pm' in timestamp_text and hour != 12:  # Convert non-noon hours from PM to 24-hour format
            hour += 12
        elif 'am' in timestamp_text and hour == 12:  # Convert midnight from 12-hour to 24-hour format
            hour = 0

        activity_by_hour[hour] += 1

    # Plotting the activity pattern
    hours = list(activity_by_hour.keys())
    counts = list(activity_by_hour.values())

    plt.bar(hours, counts)
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Messages')
    plt.title('Group Activity Pattern')
    plt.xticks(list(range(0, 24)))
    plt.grid(axis='y')
    plt.show()


def print_group_activity_by_user(soup):
    # Dictionary to store the count of messages by hour for each user
    activity_by_user_and_hour = defaultdict(lambda: defaultdict(int))

    # Iterate over all message divs
    for div in soup.find_all('div', class_="_3-95 _a6-g"):
        sender_div = div.find('div', class_="_2ph_ _a6-h _a6-i")
        if sender_div is None:
            continue  # Skip this iteration if the sender div was not found
        sender = sender_div.get_text()
        timestamp_div = div.find('div', class_="_a72d")

        if timestamp_div:  # Ensure the timestamp exists
            timestamp_text = timestamp_div.get_text()
            # Assuming the timestamp format is like "sep 11, 2023 4:39:09pm", extracting the hour part
            hour = int(timestamp_text.split(' ')[3].split(':')[0])

            if 'pm' in timestamp_text and hour != 12:  # Convert non-noon hours from PM to 24-hour format
                hour += 12
            elif 'am' in timestamp_text and hour == 12:  # Convert midnight from 12-hour to 24-hour format
                hour = 0

            activity_by_user_and_hour[sender][hour] += 1

    # Plotting the activity pattern for each user
    for user, activity in activity_by_user_and_hour.items():
        hours = list(activity.keys())
        counts = list(activity.values())

        plt.bar(hours, counts, label=user)
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Messages')
        plt.title(f'Activity Pattern for {user}')
        plt.xticks(list(range(0, 24)))
        plt.grid(axis='y')
        plt.legend()
        plt.show()

def print_number_of_messages_by_user(messages_by_user):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(messages_by_user.keys()), y=list(messages_by_user.values()))
    plt.title('Number of Messages by User')
    plt.ylabel('Number of Messages')
    plt.xlabel('User')
    plt.xticks(rotation=45)
    plt.show()

def print_number_of_reactions_by_user(reactions_by_user):
    # Visualization for number of reactions by user
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(reactions_by_user.keys()), y=list(reactions_by_user.values()))
    plt.title('Number of Reactions by User')
    plt.ylabel('Number of Reactions')
    plt.xlabel('User')
    plt.xticks(rotation=45)
    plt.show()

def print_number_of_reactions_by_type_by_user(reactions_by_user):
    # Visualization for number of reactions by user
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(reactions_by_user.keys()), y=list(reactions_by_user.values()))
    plt.title('Number of Reactions by User')
    plt.ylabel('Number of Reactions')
    plt.xlabel('User')
    plt.xticks(rotation=45)
    plt.show()

def print_number_of_reactions_on_messages_by_user(reactions_on_messages):
    # Visualization for number of reactions on messages
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(reactions_on_messages.keys()), y=list(reactions_on_messages.values()))
    plt.title('Number of Reactions on Messages by User')
    plt.ylabel('Number of Reactions')
    plt.xlabel('User')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    conversation_name = 'bdrsxtetra/' # Put the name of the conversation folder here
    name_files_html = get_html_files(conversation_name)

    # Use a list to accumulate the content of all HTML files
    all_html_contents = []

    for name_file_html in name_files_html:
        with open(conversation_name + name_file_html, 'r', encoding='utf-8') as file:
            all_html_contents.append(file.read())

    # Join all the contents and parse them with BeautifulSoup
    combined_html = ''.join(all_html_contents)
    # combined_html = all_html_contents[0]
    soup = BeautifulSoup(combined_html, 'html.parser')

    names, messages, dates = get_messages_names_dates(soup)

    analyzer = get_analyzer()

    user_messages_one_star = get_messages_with_one_star_by_user(messages, names)

    top_hate_messages = get_top_hate_messages_for_all_users(user_messages_one_star)

    top_hate_messages_by_user = get_top_hate_messages_by_user(user_messages_one_star)

    print(top_hate_messages_by_user)
    print(top_hate_messages)

    print_group_activity_by_user(soup)
    print_group_time_activity(soup)
    number_of_messages_by_user = count_users_messages(soup)
    print_number_of_messages_by_user(number_of_messages_by_user)
