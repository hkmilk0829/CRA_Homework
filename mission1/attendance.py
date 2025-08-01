ID_MAP = {}
NAMES = [''] * 100
DAT = [[0] * 7 for _ in range(100)]
POINTS = [0] * 100
GRADES = [0] * 100
WED_COUNT = [0] * 100
WEEKEND_COUNT = [0] * 100
ID_CNT = 0

DAY_INFO = { "monday": (0, 1), "tuesday": (1, 1), "wednesday": (2, 3), "thursday": (3, 1), "friday": (4, 1), "saturday": (5, 2), "sunday": (6, 2)}

def get_or_create_id(name):
    global ID_CNT
    if name not in ID_MAP:
        ID_CNT += 1
        ID_MAP[name] = ID_CNT
        NAMES[ID_CNT] = name
    return ID_MAP[name]

def record_attendance(name, day):
    user_id = get_or_create_id(name)
    day = day.lower()
    if day not in DAY_INFO:
        return
    index, point = DAY_INFO[day]
    DAT[user_id][index] += 1
    POINTS[user_id] += point
    if index == 2:  # Wednesday
        WED_COUNT[user_id] += 1
    if index in (5, 6):  # Weekend
        WEEKEND_COUNT[user_id] += 1
def finalize_grades():
    for i in range(1, ID_CNT + 1):
        # Wednesday bonus
        if DAT[i][2] > 9:
            POINTS[i] += 10
        # Weekend bonus
        if DAT[i][5] + DAT[i][6] > 9:
            POINTS[i] += 10
        # GOLD
        if POINTS[i] >= 50:
            GRADES[i] = 1
        # SILVER
        elif POINTS[i] >= 30:
            GRADES[i] = 2
        # NORMAL
        else:
            GRADES[i] = 0
def print_results():
    for i in range(1, ID_CNT + 1):
        grade_str = {1: "GOLD", 2: "SILVER", 0: "NORMAL"}[GRADES[i]]
        print(f"NAME : {NAMES[i]}, POINT : {POINTS[i]}, GRADE : {grade_str}")

def print_removed_users():
    print("\nRemoved player")
    print("==============")
    for i in range(1, ID_CNT + 1):
        if GRADES[i] == 0 and WED_COUNT[i] == 0 and WEEKEND_COUNT[i] == 0:
            print(NAMES[i])

def load_file(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    record_attendance(parts[0], parts[1])
            return True
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return False

def main():
    if load_file("attendance_weekday_500.txt"):
        finalize_grades()
        print_results()
        print_removed_users()

if __name__ == '__main__':
    main()