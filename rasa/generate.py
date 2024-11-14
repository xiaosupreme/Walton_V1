import random
import json

# List to store all generated samples
data = []

# Helper function to add generated samples to data list
def add_samples(phrases, intent):
    for phrase in phrases:
        data.append({"text": phrase, "intent": intent})

# Room Information
room_availability_questions = [
    "What rooms are available right now?",
    "Can you list the available rooms?",
    "Do you have any rooms open?",
    "What types of rooms can I book?",
    "Show me the available room options.",
    "What rooms do you have available today?",
    "Are there any vacant rooms?",
    "What room types are currently open for booking?",
]

room_price_questions = [
    "How much does each room cost per night?",
    "Can you tell me the price per night for each room type?",
    "What are the rates for the rooms?",
    "What's the nightly rate for each room?",
    "How much would a night cost for each type of room?",
    "What are today’s room rates?",
    "Could you give me the nightly prices for all room types?",
]

# Check-In and Amenities
check_in_time_questions = [
    "What is the check-in time?",
    "When can I check in?",
    "Could you tell me the check-in policy?",
    "What time is check-in?",
    "What time am I allowed to check in?",
    "When does check-in start?",
]

breakfast_questions = [
    "Is breakfast included?",
    "Do you offer complimentary breakfast?",
    "Is there free breakfast with the stay?",
    "Does the booking come with breakfast?",
    "What’s the breakfast policy?",
    "Can I get free breakfast with my booking?",
]

wifi_workspace_questions = [
    "Do your rooms have Wi-Fi and a workspace?",
    "Is there Wi-Fi and a work area in the rooms?",
    "Can I get Wi-Fi and a desk in the room?",
    "Does the room include internet access and a workspace?",
    "Do all rooms have internet and workspaces?",
    "Is Wi-Fi included, and can I work in the room?",
]

# Parking and Transportation
parking_availability_questions = [
    "Is there parking available?",
    "Do you offer parking for guests?",
    "Can I park my car there?",
    "What are the parking options?",
    "Is guest parking provided?",
    "Is there secure parking at the hotel?",
]

airport_transportation_questions = [
    "Do you offer airport transportation?",
    "Is there a shuttle to the airport?",
    "Can I get a ride to the airport?",
    "Does the hotel provide airport transport?",
    "Can I arrange airport pickup?",
]

# Discounts and Payment Options
discounts_questions = [
    "Do you offer any discounts?",
    "Are there any current promotions?",
    "Can I get a discount on my booking?",
    "What discounts are available?",
    "Are there any seasonal promotions?",
    "Do you have discounts for first-time guests?",
]

payment_methods_questions = [
    "What payment methods do you accept?",
    "Can I pay with a credit card?",
    "Do you take online payments?",
    "What are the accepted payment options?",
    "Can I pay using PayPal?",
    "What forms of payment do you allow?",
]

installments_questions = [
    "Can I pay in installments?",
    "Is there an installment plan available?",
    "Can I split my payment?",
    "Do you offer payment plans?",
    "Is it possible to pay in parts?",
]

# Amenities and Facilities
fitness_center_questions = [
    "Do you have a fitness center?",
    "Is there a gym on-site?",
    "Can I work out at the hotel?",
    "Does the hotel have gym facilities?",
    "Are there exercise facilities?",
]

laundry_facilities_questions = [
    "Are there laundry facilities on-site?",
    "Can I do laundry at the hotel?",
    "Do you offer laundry services?",
    "Is there a place for guests to do laundry?",
    "Are self-service laundry facilities available?",
]

# Local Attractions and Recommendations
nearby_attractions_questions = [
    "Can you recommend nearby attractions?",
    "What are some things to do around here?",
    "Are there any attractions close by?",
    "What local places should I visit?",
    "Do you have recommendations for nearby restaurants?",
    "What are the best places to eat nearby?",
]

# Special Requests and Pet Policies
special_occasion_questions = [
    "Can you help me arrange a surprise for a special occasion?",
    "I’d like to plan a surprise, can you help?",
    "Can the hotel help with a special occasion?",
    "Is there any way to arrange a special surprise?",
    "Can someone assist with organizing a celebration?",
]

conference_rooms_questions = [
    "Do you have conference rooms available?",
    "Is there event space for meetings?",
    "Can I book a conference room?",
    "What are the options for conference rooms?",
    "Does the hotel offer rooms for events?",
]

pet_policy_questions = [
    "Can I bring my pet?",
    "Is the hotel pet-friendly?",
    "Are pets allowed?",
    "What’s the policy on pets?",
    "Can I have a pet in the room?",
]

pet_fee_questions = [
    "How much is the security deposit for pets?",
    "What’s the cleaning fee for pets?",
    "Is there a pet deposit?",
    "What are the fees for bringing a pet?",
    "Do I have to pay extra for my pet?",
]

# Adding generated samples to the data list
add_samples(room_availability_questions, "room_availability")
add_samples(room_price_questions, "room_price")
add_samples(check_in_time_questions, "check_in_time")
add_samples(breakfast_questions, "complimentary_breakfast")
add_samples(wifi_workspace_questions, "wifi_workspace")
add_samples(parking_availability_questions, "parking_availability")
add_samples(airport_transportation_questions, "airport_transportation")
add_samples(discounts_questions, "discounts_promotions")
add_samples(payment_methods_questions, "payment_methods")
add_samples(installments_questions, "installments")
add_samples(fitness_center_questions, "fitness_center")
add_samples(laundry_facilities_questions, "laundry_facilities")
add_samples(nearby_attractions_questions, "nearby_attractions")
add_samples(special_occasion_questions, "special_occasion")
add_samples(conference_rooms_questions, "conference_rooms")
add_samples(pet_policy_questions, "pet_policy")
add_samples(pet_fee_questions, "pet_fee")

# Save the generated data to a JSON file
with open("hotel_chatbot_intent_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Data generation complete. Check hotel_chatbot_intent_data.json for the output.")
