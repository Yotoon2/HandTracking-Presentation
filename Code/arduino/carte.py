import serial
import time

PORT = '/dev/ttyACM0'
BAUDRATE = 115200

ALPHA = 0.7
DELTA_THRESHOLD = 8.0
STABLE_TRESHOLD = 4.0
COOLDOWN = 0.5
STARTUP_IGNORE = 1.0


roll_filt = None
pitch_filt = None
yaw_filt = None

roll_prev = 0
pitch_prev = 0
yaw_prev = 0

last_gesture_time = 0
ready_time = 0

def wrap_angle(angle):
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

def angle_diff(current, reference):
    return wrap_angle(current - reference)

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)

def read_orientation():
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        try:
            
            parts = line.split(",")
            
            if len(parts) != 4:
                print("4")
                continue
            
            roll = float(parts[0])
            pitch = float(parts[1])
            yaw = float(parts[2])
            heading = float(parts[3])

            roll = wrap_angle(roll)
            pitch = wrap_angle(pitch)
            yaw = wrap_angle(yaw)
            heading = wrap_angle(heading)

            return roll, pitch, yaw, heading
        
        except:
            continue

def calibrate_neutral(duration=5.0):
    global roll0, pitch0, yaw0
    global roll_filt, pitch_filt, yaw_filt
    global roll_prev, pitch_prev, yaw_prev

    print("Calibration...")

    roll_sum = 0
    pitch_sum = 0
    yaw_sum = 0
    count = 0

    start = time.time()

    while ((time.time() - start) < duration):

        roll, pitch, yaw, heading = read_orientation()
        roll_sum += roll
        pitch_sum += pitch
        yaw_sum += yaw
        count += 1

    roll0 = roll_sum/count
    pitch0 = pitch_sum/count
    yaw0 = yaw_sum/count

    roll_filt = roll0
    pitch_filt = pitch0
    yaw_filt = yaw0

    roll_prev = roll0
    pitch_prev = pitch0
    yaw_prev = yaw0

    print("Calibration terminée")

    print(f"Roll0 : {roll0:.2f} | Pitch0 : {pitch0:.2f} | Yaw0 : {yaw0:.2f}")

def initialize_filter(duration=1.0):
    global roll_filt, pitch_filt, yaw_filt
    global roll_prev, pitch_prev, yaw_prev
    global ready_time

    print("Initialisation...")

    values = []

    start = time.time()

    while time.time() - start < duration:
        roll, pitch, yaw, heading = read_orientation()
        values.append((roll, pitch, yaw))
    roll_filt = sum(v[0] for v in values) / len(values)
    pitch_filt = sum(v[1] for v in values) / len(values)
    yaw_filt = sum(v[2] for v in values) / len(values)

    roll_prev = roll_filt
    pitch_prev = pitch_filt
    yaw_prev = yaw_filt

    ready_time = time.time()

    print("Terminé")
    print(f"Roll0 : {roll_filt:.2f} | Pitch0 : {pitch_filt:.2f} | Yaw0 : {yaw_filt:.2f}")


def detect_movement(roll, pitch, yaw, heading):
    global roll_filt, pitch_filt, yaw_filt
    global roll_prev, pitch_prev, yaw_prev
    global last_gesture_time

    old_roll = roll_filt
    old_pitch = pitch_filt
    old_yaw = yaw_filt

    roll_filt = wrap_angle(ALPHA * roll_filt + (1 - ALPHA) * roll)
    pitch_filt = wrap_angle(ALPHA * pitch_filt + (1 - ALPHA) * pitch)
    yaw_filt = wrap_angle(ALPHA * yaw_filt + (1 - ALPHA) * yaw)

    d_roll = angle_diff(roll_filt, roll_prev)
    d_pitch = angle_diff(pitch_filt, pitch_prev)
    d_yaw = angle_diff(yaw_filt, yaw_prev)

    abs_dr = abs(d_roll)
    abs_dp = abs(d_pitch)
    abs_dy = abs(d_yaw)

    movement = "STABLE"

    now = time.time()

    if now - ready_time < STARTUP_IGNORE:
        return movement, d_roll, d_pitch, d_yaw, roll_filt, pitch_filt, yaw_filt
    
    if  now - last_gesture_time < COOLDOWN:
        return "COOLDOWN", d_roll, d_pitch, d_yaw, roll_filt, pitch_filt, yaw_filt
    
    if abs_dy > DELTA_THRESHOLD and abs_dy > abs_dp and abs_dy > abs_dp:
        movement = "SWIPE RIGHT" if d_yaw > 0 else "SWIPE LEFT"
        last_gesture_time = now
    elif abs_dp > DELTA_THRESHOLD and abs_dp > abs_dy and abs_dp > abs_dr:
        movement = "HAND UP" if d_pitch > 0 else "HAND DOWN"
        last_gesture_time = now

    elif abs_dr > DELTA_THRESHOLD and abs_dr > abs_dy and abs_dr > abs_dp:
        movement = "TILT RIGHT" if d_roll > 0 else "TILT LEFT"
        last_gesture_time = now

    return movement, d_roll, d_pitch, d_yaw, roll_filt, pitch_filt, yaw_filt

def main():
    initialize_filter(duration=1.0)

    print("=====DETECTION PRETE=====")

    while True:
        roll, pitch, yaw, heading = read_orientation()

        movement, d_roll, d_pitch, d_yaw, rf, pf, yf = detect_movement(roll, pitch, yaw, heading)
        print(f"Roll : {rf:7.2f} | "
              f"Pitch : {pf:7.2f} | "
              f"Yaw : {yf:7.2f} | "
              f"Heading : {heading:7.2f} | "
              f"dR : {d_roll:6.2f} | dP: {d_pitch:6.2f} | dY : {d_yaw:6.2f} || "
              f"{movement}")
        time.sleep(0.03)

if __name__ == "__main__":
    main()