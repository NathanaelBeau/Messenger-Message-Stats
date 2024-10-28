# Messenger Chat Analysis

This project is designed for analyzing messages from Facebook Messenger chats with friends. It parses message data from downloaded HTML files and provides visualizations on message activity, reactions, and individual user patterns.

## ⚠️ Project Status: Under Construction

This project is a work in progress, and I'm open to new ideas for features and analyses to add. Feel free to contribute or suggest improvements!

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Download Messenger Data from Facebook](#download-messenger-data-from-facebook)
  - [Install Dependencies](#install-dependencies)
  - [Usage](#usage)
- [Current Analysis Functions](#current-analysis-functions)
- [Contributions](#contributions)

## Features

- Counts the number of messages and photos sent by each user.
- Extracts message texts and timestamps to analyze activity by time of day.
- Counts reactions by each user and breaks them down by reaction type.
- Visualizes group activity patterns and individual user contributions.

## Getting Started

### Download Messenger Data from Facebook

1. Go to [Facebook Settings](https://www.facebook.com/settings).
2. Select **Your Facebook Information** > **Download Your Information**.
3. Choose **Messages** and specify the chat you’d like to analyze.
4. Select **HTML** format (other formats may not work with this parser).
5. Download the data and extract the files. You'll find individual HTML files for each chat in the `messages` folder.

### Install Dependencies

Clone this repository and install dependencies:
```bash
git clone https://github.com/your-username/messenger-chat-analysis.git
cd messenger-chat-analysis
conda install environment.yml
```

### Usage

Place your downloaded HTML files in a folder within the project directory. Update conversation_name in main.py to reflect the folder name containing your files. Then run the script:

```bash
python main.py
```

## Contributions

This project is open to new ideas and contributions! If you have suggestions for additional analyses, please feel free to open an issue or submit a pull request. Let's make this project a comprehensive tool for exploring Messenger chats together! Let me know if you'd like any adjustments or additional details!
