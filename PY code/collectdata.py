import os
import cv2

cap = cv2.VideoCapture(0)
directory = 'Image/'

# Automatically create folders for all letters
letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
for letter in letters:
    os.makedirs(directory + letter, exist_ok=True)

current_idx = 0

while True:
    _, frame = cap.read()
    current_letter = letters[current_idx]
    count = len(os.listdir(directory + current_letter))

    # Draw ROI rectangle
    cv2.rectangle(frame, (0, 40), (300, 400), (255, 255, 255), 2)

    # --- TOP OVERLAY: Current letter + count ---
    cv2.rectangle(frame, (0, 0), (640, 38), (0, 0, 0), -1)
    cv2.putText(frame, f"Letter: {current_letter}  |  Photos: {count}/30",
                (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # --- BOTTOM LEGEND ---
    cv2.rectangle(frame, (0, 415), (640, 470), (0, 0, 0), -1)
    cv2.putText(frame, "A = back  |  D = next  |  SPACE = capture  |  Q = quit",
                (10, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 1)

    # --- LETTER NAVIGATION HINT (left/right arrows) ---
    if current_idx > 0:
        cv2.putText(frame, f"< {letters[current_idx - 1]}",
                    (310, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
    if current_idx < len(letters) - 1:
        cv2.putText(frame, f"{letters[current_idx + 1]} >",
                    (500, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    cv2.imshow("Sign Language Data Collector", frame)
    cv2.imshow("ROI", frame[40:400, 0:300])

    frame = frame[40:400, 0:300]

    interrupt = cv2.waitKey(10)

    # SPACE - capture
    if interrupt & 0xFF == ord(' '):
        cv2.imwrite(directory + current_letter + '/' + str(count) + '.png', frame)
        print(f"Saved {current_letter}/{count}.png")

    # D - next letter
    elif interrupt & 0xFF == ord('d'):
        if current_idx < len(letters) - 1:
            current_idx += 1
            print(f"Switched to: {letters[current_idx]}")

    # A - previous letter
    elif interrupt & 0xFF == ord('a'):
        if current_idx > 0:
            current_idx -= 1
            print(f"Switched to: {letters[current_idx]}")

    # Q - quit
    elif interrupt & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()