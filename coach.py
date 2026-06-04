from google import genai
import getpass

print("--- Running AI Coach Initialization ---")
api_key = getpass.getpass("Paste your Gemini API Key here (it will be invisible as you type) and press Enter: ")

# Authenticate the client
client = genai.Client(api_key=api_key)

workout_data = {
    "runner_name": "Ruslan",
    "distance_miles": 5.0,
    "total_time_minutes": 38.08,
    "splits": [
        {"mile": 1, "pace": "7:43", "heart_rate": 101},
        {"mile": 2, "pace": "7:31", "heart_rate": 175},
        {"mile": 3, "pace": "7:04", "heart_rate": 184},
        {"mile": 4, "pace": "7:58", "heart_rate": 190},
        {"mile": 5, "pace": "7:15", "heart_rate": 165}
    ]
}

system_instructions = (
    "You are a super friendly, encouraging, elite, and nice running coach. "
    "You always celebrate the runner's effort first before giving advice. "
    "However, PLEASE be real, and don't sugarcoat ANYTHING"
    "Refrain from using vulgar language, keep it clean"
    "Keep your tone lively, warm, and conversational, like a supportive friend. "
    "Analyze the runner's data, highlight a few things they did really well, "
    "and give them some insightful tips for their next run to keep improving."
)

# 3. The Data Compilation (F-Strings)
workout_summary = f"""
Analyze this workout for {workout_data['runner_name']}:
- Distance: {workout_data['distance_miles']} miles
- Total Time: {workout_data['total_time_minutes']} mins

Splits:
Mile 1: {workout_data['splits'][0]['pace']} (HR: {workout_data['splits'][0]['heart_rate']})
Mile 2: {workout_data['splits'][1]['pace']} (HR: {workout_data['splits'][1]['heart_rate']})
Mile 3: {workout_data['splits'][2]['pace']} (HR: {workout_data['splits'][2]['heart_rate']})
Mile 4: {workout_data['splits'][3]['pace']} (HR: {workout_data['splits'][3]['heart_rate']})
Mile 5: {workout_data['splits'][4]['pace']} (HR: {workout_data['splits'][4]['heart_rate']})
"""

# 4. The Network Request (Try/Except Safety Net)
print("\nTransmitting data to AI servers...")

try:
    # The new standard for generating content using the Client object
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=f"{system_instructions}\n\n{workout_summary}"
    )
    
    print("\n" + "="*30)
    print("Your coach says:")
    print("="*30)
    print(response.text)
    print("="*30 + "\n")

except Exception as error:
    print("\nError")
    print(f"The error was: {error}")

def save_feedback(feedback):
    with open("workout_history.txt", "a") as f:
        f.write("\n--- New Coaching Session ---\n")
        f.write(feedback)
        f.write("\n")

save_feedback(response.text)
print("Feedback saved to workout_history.txt!")