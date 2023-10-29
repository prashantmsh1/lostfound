import face_recognition
import pickle
import os
from PIL import Image

# Load the known faces data from the pickle file
with open('known_faces_dict.pkl', 'rb') as file:
    known_faces_dict = pickle.load(file)

# Load an unknown face for testing
unknown_image_path = "13.jpg"  # Change this to your unknown image path

if os.path.exists(unknown_image_path):
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    unknown_face_encodings = face_recognition.face_encodings(unknown_image)

    if len(unknown_face_encodings) > 0:
        unknown_face_encoding = unknown_face_encodings[0]

        match_found = False
        tolerance = 0.6  # Tolerance for face comparison

        for known_name, known_face_encoding in known_faces_dict.items():
            # Compare the unknown face to the known faces
            result = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=tolerance)

            if result[0]:
                print(f"Successful match found: {known_name}")
                match_found = True

                # Display the matched image
                matched_image_path = os.path.join("photo", known_name + os.path.splitext(unknown_image_path)[1])
                matched_image = Image.open(matched_image_path)
                matched_image.show()
                

                break

        if not match_found:
            print("No match found")
    else:
        print("No face found in the unknown image")
else:
    print("File does not exist or is not supported. Please provide a valid .jpg, .jpeg, or .png file.")
