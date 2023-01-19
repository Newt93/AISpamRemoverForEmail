import imaplib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load the dataset
data = pd.read_csv('emails.csv')

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(data['message'], data['label'], test_size=0.2)

# Convert the messages into a numerical representation using CountVectorizer
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train the classifier
classifier = MultinomialNB()
classifier.fit(X_train_vec, y_train)

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL("imap.example.com")
imap.login("your_username", "your_password")

# Select the inbox
imap.select("INBOX")

# Search for messages from the specific sender
status, message_numbers = imap.search(None, 'FROM "specific_sender@example.com"')
message_numbers = message_numbers[0].split()

# Iterate through the messages
for message_number in message_numbers:
    # Fetch the message
    status, message = imap.fetch(message_number, '(RFC822)')

    # Convert the message to a string
    message = message[0][1].decode()

    # Make a prediction on the message
    prediction = classifier.predict(vectorizer.transform([message]))

    # Check if the message is spam
    if prediction == "spam":
        # Move the message to the spam folder
        imap.move(message_number, "spam")

# Close the connection
imap.logout()
