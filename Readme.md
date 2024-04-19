# Team (CtrlAltDelete)

- Srijan Sahay Srivastava
- Tanish Bhole
- Kasturi Sinha
- Samridhi Sati

# Bon Voyage


“Bon Voyage”  is a  travel-made-easy project that takes in account your suggestions and lets you take control by providing travel experience tailored to your own unique preferences.
Imagine a seamless experience where you input details like travel duration, destination, points of interest, and activities, and our AI engine crafts a tailored itinerary just for you. We go beyond generic suggestions, considering factors like optimal routes, travel time, and real-time updates to ensure a smooth and enjoyable trip. With AI-powered insights and recommendations, you'll discover hidden gems and off-the-beaten-path experiences that match your interests perfectly. Our app integrates seamlessly with travel booking platforms, navigation tools, and local services, making it effortless to turn your dream itinerary into reality. Say goodbye to cookie-cutter travel plans and hello to personalized adventures designed to make every journey unforgettable. 

# Features

- Planner : Gives detailed itinerary which includes rest stops,eateries and attractions.

- Live weather to plan holidays upto 5 days : This travel planner uses real-time weather data to suggest    dynamic adjustments to your itinerary. It constantly monitors weather forecasts for your destination. Based on the weather (rain, sunshine, etc.), it analyzes the suitability of planned activities. It suggests alternative activities or adjustments to your schedule for optimal enjoyment.
- Information is returned in a simple and readable format
- Filters are kept in mind for an elite user experience : Filters are kept in mind for an elite user experience:we use filters like food preferences, health issues, personal interest to provide with a personalized itinerary
- Fast and seamless response using Gemini as LLM and gRPC as protocol:
We use cutting-edge technology called Gemini, a large language model (LLM), to understand your requests and provide answers instantly.  Additionally, our system relies on gRPC to ensure smooth and efficient communication between different servers . 




Now the boring part..

![alt text](image-1.png)




Bon Voyage uses a  Master LLM, a large language model,  to power some of its functionalities.  Additionally, it  integrates with various APIs including Hotel API,  Food API, and Weather API to provide users with  travel-related information




Master LLM (Large Language Model):
Function: Bon Voyage utilizes a large language model (LLM) as its core engine. In Bon Voyage, the LLM is used for:
Understanding user queries and requests through the chat interface .
Providing recommendations and suggestions for destinations, activities, and logistics based on user preferences and context .
Generating different parts of the travel itinerary, like crafting descriptions for locations or writing email confirmations.

MongoDB:
MongoDB stores data in a flexible format rather than rigid tables. 
This makes it :
scalable 
well-suited for storing unstructured data like user profiles, chat history, and travel itinerary details with varying levels of complexity.

APIs (Application Programming Interfaces):
APIs act as intermediaries between Bon Voyage and various external services. By integrating with APIs, Bon Voyage can access and process information from those services without having to build everything from scratch. Here are some  APIs used in Bon Voyage:
Tomtom POI API: Provides real-time hotel availability, rates,offers information on restaurants, cafes, and other dining options .Calculates distance between two locations based on their longitudes and latitudes.
Tomorrow.io: An API which delivers weather data and forecasts for various locations to help users plan their trip accordingly .




gRPC:
gRPC uses a protocol buffer system to efficiently encode and decode data being transferred between applications. In Bon Voyage, gRPC is used for internal service communication between different microservices within the application, ensuring efficient data exchange.

Auth0:
Auth0 handles user sign-up, sign-in, and manages access permissions within the application. Integration with Auth0 allows Bon Voyage to securely manage user accounts and data.


Sample of backend

![alt text](image-2.png)

![alt text](image-3.png)




# Getting Started
After ensuring that the servers are up and running, proceed to call the LLM (Language Model) by executing the following commands in the MainFrame directory:
Setting up the servers:
4 folders
Perform the following steps in each server’s folder:

bash
# creating independent environments
Python3 -m venv venv
# install requirements
pip install -r requirements.txt
Python3 app.py


bash
# Install required dependencies
pip install -r requirements.txt
# running local server
uvicorn main:app

python app.py
These commands will install the necessary dependencies for the LLM model and then run the app using Python. Ensure that the servers are running and accessible before executing these commands to ensure smooth functionality.


# Acknowledgement
Wittyhacks and Datacode Community Organizers
Thank you to the organizers of Wittyhacks and the Datacode community for creating a platform for developers to showcase their talents and for fostering innovation in the tech space. Your dedication to these communities is truly inspiring.
Thankyou to the partners and sponsors for this enriching and rewarding experience
A big shout-out to Major League Hacking for their continuous support of hackathons around the world.  MLH's commitment to empowering developers, especially students, is commendable and has undoubtedly led to the creation of many groundbreaking projects.
Thanks to MongoDB for providing a powerful and scalable NoSQL database solution.  MongoDB's flexibility has likely played a crucial role in efficiently storing and managing data in the Bon Voyage travel planner.
We appreciate GoDaddy Registry for making domain registration accessible and reliable.  
Thank you to Auth0 for offering a secure and user-friendly authentication and authorization platform.  Auth0's integration has likely ensured that user accounts and data in Bon Voyage are well-protected.
A big thanks to GitHub Copilot for providing an AI-powered coding assistant.  GitHub Copilot's suggestions have likely helped developers working on Bon Voyage to write code more efficiently and effectively.
We appreciate Devfolio for creating a platform specifically for showcasing developer portfolios and projects.  Devfolio has likely been a valuable tool for the developers of Bon Voyage to share their creation with the world.
A big thank you to NMIMS Indore for providing the venue for this hackathon.  Having a dedicated space for developers to come together, collaborate, and build innovative projects is essential for a successful hackathon.And finally, a huge thankyou to the mentors who guided and supported us throughout the hackathon.
I hope this comprehensive acknowledgment expresses our gratitude to all the parties involved in making this project possible.









