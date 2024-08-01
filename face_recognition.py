import face_recognition
import os
from constants import STUDENT_FACE_DIRECTORY

known_student_face_encodings = []


def load_known_student_face_encodings():
    for file_name in os.listdir(STUDENT_FACE_DIRECTORY):
        student_image = face_recognition.load_image_file(os.path.join(STUDENT_FACE_DIRECTORY, file_name))
        face_location = face_recognition.face_locations(student_image)
        if len(face_location) > 0:
            face_encoding = face_recognition.face_encodings(student_image, [face_location[0]])[0]
            known_student_face_encodings.append(face_encoding)


def encode_face(filename):
    try:
        image = face_recognition.load_image_file(filename)
        face_location = face_recognition.face_locations(image)
        if len(face_location) > 0:
            face_encoding = face_recognition.face_encodings(image, face_location)[0]
            return face_encoding
    except Exception as e:
        print(f"Error encoding face: {e}")
        return None


def check_matching_face(clicked_student_face_encoding):
    if clicked_student_face_encoding:
        for student_encoding in known_student_face_encodings:
            match_result = face_recognition.compare_faces([student_encoding], clicked_student_face_encoding[0])
            if True in match_result:
                return True
    return False
