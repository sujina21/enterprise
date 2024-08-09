import sqlite3
from speech import recognize_speech, speak_text, generate_user_id
from database import *
from face_capture import capture_faces
from face_recognition import train_face_recognizer

# List of questions
QUESTION_LIST = [
    "What is your full name?",
    "What is your age?",
    "Are you Boy or Girl?",
    "What is your phone number?",
    "Please describe the issue you are experiencing with your eyes. This will help us understand your condition better."
]


def get_patient_responses():
    responses = []
    for question in QUESTION_LIST:
        speak_text(question)
        print(f"{question}\nListening...")
        response = recognize_speech()
        responses.append(response)


    if str(responses[2]).lower() == "boy":
        is_male = True
    elif str(responses[2]).lower() == "girl":
        is_male = False
    else:
        is_male=True
    responses[-1] = "male" if is_male else "female"
    return responses

def handle_existing_patient(patient):
    patient_id = patient[0]
    visited_to = patient[6]

    if visited_to:
        doctor = fetch_doctor_data(visited_to)
        if doctor:
            speech_txt=f"Welcome Back {patient[1]},Do you want to visit {doctor[1]} again? Say Yes or No."
            print(f"{speech_txt}\nListening...")
            speak_text(speech_txt)
            response = recognize_speech()
            if "yes" in response.lower():
                if doctor[3] == "present":
                    if doctor[2] == "free":
                        update_doctor_status(visited_to, "busy")
                        print(f"Your best doctor is {doctor[1]}. {fetch_doctor_location(doctor[0])}")
                        speak_text(f"Your best doctor is {doctor[1]}. {fetch_doctor_location(doctor[0])}")
                        return visited_to
                    else:
                        return handle_busy_or_absent_doctor()
                else:
                    return handle_busy_or_absent_doctor()
            else:
                return handle_busy_or_absent_doctor()
        else:
            return handle_busy_or_absent_doctor()
    else:
        return handle_busy_or_absent_doctor()

def handle_busy_or_absent_doctor():
    new_doctor = assign_random_doctor()
    if new_doctor:
        speak_text(f"Your doctor is {new_doctor[1]}. {fetch_doctor_location(new_doctor[0])}")
        print(f"Your doctor is {new_doctor[1]}. {fetch_doctor_location(new_doctor[0])}")
        update_doctor_status(new_doctor[0], "busy")
        return new_doctor[0]
    else:
        speak_text("All doctor are busy. Please wait.")
        return None


    
def main(existing_patient_id=None):
    # Check if patient data already exists
    Id = existing_patient_id if existing_patient_id is not None else generate_user_id()
    patient = fetch_patient_data(Id)
    responses = get_patient_responses() if existing_patient_id is None else [patient[1],patient[2],patient[3],patient[4],patient[5]]
    # print(f"The responses is --> {responses}")
    name, age, gender, phone, problem = responses[:5]

    if patient:
        visited_to = handle_existing_patient(patient)
        if visited_to:
            update_patient_doctor(patient[0], visited_to)
        else:
            return
    else:
        visited_to = assign_random_doctor()
        if visited_to:
            speak_text(f"Your new doctor is {visited_to[1]}. {fetch_doctor_location(visited_to[0])}")
            update_doctor_status(visited_to[0], "busy")
        else:
            speak_text("No doctors available. Please wait.")
            return

    insert_or_update_patient(Id, name, age, gender, phone, problem, visited_to[0] if existing_patient_id is None else visited_to )
    capture_faces(Id) if existing_patient_id is None else None
    train_face_recognizer("dataset") if existing_patient_id is None else None

if __name__ == "__main__":
    main()
