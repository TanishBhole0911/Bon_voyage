import pymongo
#from pymongo import ObjectId
from datetime import datetime
from bson.objectid import ObjectId

# MongoDB connection details (replace with yours)
client = pymongo.MongoClient("mongodb+srv://tanishbhole:ScGCwOOV4FjA69Ux@trip.jmdwcyr.mongodb.net/")
db = client["trip"]
collection = db["user-info"]

def give(interest, food, health, email, in_date, in_time, chat_history, out_date):
    """
    Stores user input in the collection and returns the inserted document's ID.

    Args:
        interest (str): User's area of interest.
        food (str): User's dietary preference.
        health (str): User's health considerations.
        email (str): User's email address.
        in_date (datetime): Date of user's check-in.
        in_time (datetime): Time of user's check-in.
        chat_history (str): Optional, stores conversation history.
        out_date (datetime): Date of user's check-out (optional).

    Returns:
        str: The unique identifier (_id) of the inserted document.
    """

    # Convert date and time strings to datetime objects (if needed)
    if isinstance(in_date, str):
        in_date = datetime.strptime(in_date, "%Y-%m-%d")  # Adjust format if needed
    if isinstance(in_time, str):
        in_time = datetime.strptime(in_time, "%Y-%m-%d %H:%M:%S")  # Adjust format if needed
    if out_date and isinstance(out_date, str):
        out_date = datetime.strptime(out_date, "%Y-%m-%d")  # Adjust format if needed

    # Create the document with chat_history included
    data = {
        "interest": interest,
        "food": food,
        "health": health,
        "email": email,
        "in_date": in_date,
        "in_time": in_time,
        "chat_history": chat_history,  # Added chat_history
        "out_date": out_date,
    }

    # Insert the document and get the inserted ID
    result = collection.insert_one(data)
    return str(result.inserted_id)

#give("A","B","C","D","24/04/11","5:00","2024/7/10")

#print(give("A","B","C","D","2024-04-11","2024-04-11 05:00:00","hahah", "2024-07-10"))


def get(document_id):
    """
    Retrieves document information based on its ID.

    Args:
        document_id (str): The unique identifier (_id) of the document.

    Returns:
        dict: A dictionary containing the retrieved document's information,
              or None if the document is not found.
    """

    # Find the document by ID and convert it to a dictionary
    document = collection.find({"_id": ObjectId(document_id)})
    return document if document else None

# Example usage (replace with your form handling logic)
interest = "Music"
food = "Vegan"
health = "No allergies"
email = "user@example.com"
in_date = datetime.today().strftime("%Y-%m-%d")  # Today's date
in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current time
chat_history = "Initial conversation"  # Example chat_history data
out_date = None  # Optional, can be set if applicable

document_id = give(interest, food, health, email, in_date, in_time, chat_history, out_date)
print(f"Document inserted with ID: {document_id}")

retrieved_data = get(document_id)
retrieved_list = list(retrieved_data)
retrieved_dict = retrieved_list[0]
if retrieved_dict:
    print("Retrieved information:")
    for elem in retrieved_dict:
        print(f"{elem}: {retrieved_dict[elem]}")
else:
    print("Document not found.")
# if retrieved_data:
#     print("Retrieved information:")
#     for key, value in retrieved_data.items():
#         print(f"{key}: {value}")
# else:
#     print("Document not found.")
