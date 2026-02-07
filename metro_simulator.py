from datetime import datetime as dt

# ========= Terminal Styling (ANSI) =========
RESET   = "\033[0m"
BOLD    = "\033[1m"
ITALIC  = "\033[3m"
UNDER   = "\033[4m"
# Colors
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"


# ============================================================
# 1. LOAD METRO LINE DATA FROM Metro_Data.txt
#    B  = Blue Line
#    BB = Blue-Branch Line
#    M  = Magenta Line
#    Y  = Yellow Line
# ============================================================

blue_line, blue_branch_line, magenta_line, yellow_line = [], [], [], []

with open("Metro Data.txt", "r") as metro_file:
    metro_rows = metro_file.readlines()
    for row in metro_rows:
        row = row.strip()
        parts = [p.strip() for p in row.split(',')]
        line_name = parts[0]
        if line_name == 'Blue':
            blue_line.append(parts)
        elif line_name == 'Blue Branch':
            blue_branch_line.append(parts)
        elif line_name == 'Magenta':
            magenta_line.append(parts)
        elif line_name == 'Yellow':
            yellow_line.append(parts)
#For ease of writing code
B = blue_line
BB = blue_branch_line
M = magenta_line
Y = yellow_line

#Interchange Dictonory being made using data extraction from Mtero_Data.txt
interchange = {}
with open("Metro Data.txt", "r") as f:
    data = f.readlines()
    for i in range(len(data)):
        data[i] = [x.strip() for x in data[i].split(",")]
    for row in data:
        if len(row) < 5:
            continue
        line1   = row[0]
        station = row[1]
        flag    = row[4]
        if not flag.startswith("Yes"):
            continue
        if len(row) >= 6:    
            line2 = row[5]
        key1 = (line1, line2)
        key2 = (line2, line1)
        if key1 not in interchange:
            interchange[key1] = []
        if station not in interchange[key1]:
            interchange[key1].append(station)
        if key2 not in interchange:
            interchange[key2] = []
        if station not in interchange[key2]:
            interchange[key2].append(station)


# ============================================================
# 2. LOAD TIMETABLE DATA FROM timings.txt
# ============================================================

departure_minutes_by_hour = {}

with open("timings.txt", "r") as timings_file:
    timing_lines = timings_file.readlines()
    for line in timing_lines:
        line = line.strip()
        hour_str, mins_part = line.split(':',1)
        hour_str = hour_str.strip()
        minutes_list = []
        for minute_str in mins_part.split(','):
            minute_str = minute_str.strip()
            minutes_list.append(int(minute_str))
        departure_minutes_by_hour[int(hour_str)] = minutes_list

#For ease of writing code
d = departure_minutes_by_hour


# ============================================================
# 3. HELPER: EXIT FUNCTION
# ============================================================

def exit():
    """
    Print a friendly exit message and return to caller.
    """
    print(f"\n{GREEN}{BOLD}👋 Thank you for using the Delhi Metro Simulator!{RESET}\n")


# ============================================================
# 4. LINE CHOOSER
# ============================================================

def line_chooser():
    """
    Ask user to choose a metro line.

    Returns
    -------
    1, 2, 3  → Blue, Magenta, Yellow
    None     → User chose to go back to main menu.
    'exit'   → User chose to exit the whole program.
    """
    while True:
        try:
            print()
            print(f"{CYAN}{BOLD}┌──────────────────────────────────────┐{RESET}")
            print(f"{CYAN}{BOLD}│          🚇  Choose a Line           │{RESET}")
            print(f"{CYAN}{BOLD}└──────────────────────────────────────┘{RESET}")
            print(f"{BOLD}  1️⃣  {WHITE}Blue Line (incl. Branch){RESET}")
            print(f"{BOLD}  2️⃣  {WHITE}Magenta Line{RESET}")
            print(f"{BOLD}  3️⃣  {WHITE}Yellow Line{RESET}")
            print(f"{BOLD}  4️⃣  {YELLOW}🔙 Go to Main Menu{RESET}")
            print(f"{BOLD}  5️⃣  {RED}❌ Exit{RESET}")

            chosen_line = int(input(f"{YELLOW}➡️  Enter your choice: {RESET}"))
            assert chosen_line in [1, 2, 3, 4, 5]
        except:
            print(f"\n{RED}{BOLD}⚠️  Invalid input.{RESET} Please enter a number between 1 to 5.")
            continue

        if chosen_line == 4:
            return None
        elif chosen_line == 5:
            return 'exit'
        else:
            return chosen_line


# ============================================================
# 5. STATION SELECTION
# ============================================================

def station():
    """
    Ask user to choose a station on a selected line.
    Returns
    -------
    (line_number, station_index, last_station_name, first_station_name)
    None   → User chose to go back to main menu.
    'exit' → User chose to exit the whole program.
    """
    selected_line = line_chooser()
    if selected_line is None:
        return None
    if selected_line == 'exit':
        return 'exit'

    # ---------- Blue (including Blue-Branch) ----------
    if selected_line == 1:
        # combined: list of (internal_line_number, station_index)
        combined_indices = []

        # Add Blue line stations
        for idx in range(len(B)):
            combined_indices.append((1, idx + 1))

        # Add Blue-Branch stations, avoiding duplicate names
        for idx in range(len(BB)):
            combined_indices.append((2, idx + 1))

        while True:
            try:
                branch_section_printed = 0
                print(f"\n{CYAN}{BOLD}┌──────────────────────────────────────┐{RESET}")
                print(f"{CYAN}{BOLD}│        📍  Choose a Station          │{RESET}")
                print(f"{CYAN}{BOLD}└──────────────────────────────────────┘{RESET}")
                print(f"{BOLD}{BLUE}Stations on Blue Line (Including Branch):{RESET}")

                for display_idx, (internal_line, st_idx) in enumerate(combined_indices, start=1):
                    if internal_line == 1:
                        station_name_text = B[st_idx - 1][1]
                    else:
                        # First time we enter Blue Branch section, print a sub-heading
                        if branch_section_printed == 0:
                            print(f"\n   {ITALIC}{MAGENTA}Blue Branch Stations ⬇️{RESET}\n")
                            branch_section_printed += 1
                        station_name_text = BB[st_idx - 1][1]
                    print(f"  {BOLD}{display_idx:2d}.{RESET} {WHITE}{station_name_text}{RESET}")

                print(f"\n  {BOLD}{len(combined_indices)+1}. {YELLOW}🔙 Go to Main Menu{RESET}")
                print(f"  {BOLD}{len(combined_indices)+2}. {RED}❌ Exit{RESET}")

                station_choice = int(input(f"{YELLOW}➡️  Enter your choice: {RESET}"))
                assert 1 <= station_choice <= len(combined_indices) + 2
            except:
                print(f"\n{RED}{BOLD}⚠️  Invalid input.{RESET} Please select a valid option.")
                continue

            if station_choice == len(combined_indices) + 1:
                return None
            elif station_choice == len(combined_indices) + 2:
                return 'exit'
            else:
                internal_line, station_idx = combined_indices[station_choice - 1]
                if internal_line == 1:
                    line_data = B
                else:
                    line_data = BB

                last_station_name = line_data[-1][1]
                first_station_name = line_data[0][1]
                return (internal_line, station_idx, last_station_name, first_station_name)

    elif selected_line == 2:
        line_data = M
        line_label = "Magenta Line"
    elif selected_line == 3:
        line_data = Y
        line_label = "Yellow Line"

    while True:
        try:
            print(f"\n{CYAN}{BOLD}┌──────────────────────────────────────┐{RESET}")
            print(f"{CYAN}{BOLD}│        📍  Choose a Station          │{RESET}")
            print(f"{CYAN}{BOLD}└──────────────────────────────────────┘{RESET}")
            print(f"{BOLD}{BLUE}Stations on {line_label}:{RESET}")

            for idx in range(len(line_data)):
                print(f"  {BOLD}{idx+1:2d}.{RESET} {WHITE}{line_data[idx][1]}{RESET}")

            print(f"\n  {BOLD}{len(line_data)+1}. {YELLOW}🔙 Go to Main Menu{RESET}")
            print(f"  {BOLD}{len(line_data)+2}. {RED}❌ Exit{RESET}")

            station_choice = int(input(f"{YELLOW}➡️  Enter your choice: {RESET}"))
            assert 1 <= station_choice <= len(line_data) + 2
        except:
            print(f"\n{RED}{BOLD}⚠️  Invalid input.{RESET} Please select a valid option.")
            continue

        if station_choice == len(line_data) + 1:
            return None
        elif station_choice == len(line_data) + 2:
            return 'exit'
        else:
            selected_line += 1
            last_station_name = line_data[-1][1]
            first_station_name = line_data[0][1]
            return (selected_line, station_choice, last_station_name, first_station_name)


# ============================================================
# 6. TIME INPUT
# ============================================================

def time():
    """
    Let user choose system time or enter manually.

    Returns
    -------
    (hour_str, minute_str) in 24-hour format ("0".."23", "0".."59")
    None   → User chose to go back to main menu.
    'exit' → User chose to exit the whole program.
    """
    while True:
        try:
            print(f"\n{BOLD}{CYAN}⏰ Time Options:{RESET}")
            print(f"{BOLD}  1️⃣  {WHITE}Use current system time{RESET}")
            print(f"{BOLD}  2️⃣  {WHITE}Enter time manually{RESET}")
            print(f"{BOLD}  3️⃣  {RED}❌ Exit{RESET}")
            print(f"{BOLD}  4️⃣  {YELLOW}🔙 Go to Main Menu{RESET}")
            time_choice = int(input(f"{YELLOW}➡️  Enter your choice: {RESET}"))
            assert time_choice in [1, 2, 3, 4]
        except:
            print(f"\n{RED}{BOLD}⚠️  Invalid choice.{RESET} Please select from 1 to 4.")
            continue

        if time_choice == 3:
            return 'exit'
        elif time_choice == 4:
            return None
        elif time_choice == 1:
            now = dt.now()
            return (now.strftime("%H"), now.strftime("%M"))
        else:
            try:
                print(f"\n{ITALIC}⌨️  Enter time in 24-hour format.{RESET}")
                hour_int = int(input("   Hour (0–23): "))
                minute_int = int(input("   Minute (0–59): "))
                if not (0 <= hour_int <= 23 and 0 <= minute_int <= 59):
                    raise ValueError
                return (str(hour_int), str(minute_int))
            except:
                print(f"\n{RED}{BOLD}⚠️  Invalid time.{RESET} Please enter hour (0–23) and minute (0–59) correctly.")
                continue


# ============================================================
# 7. TIMINGS MODULE
# ============================================================

def timings():
    """
    Show next and subsequent metro timings in both directions
    for the user's chosen station and time.
    """
    print(f"\n{BLUE}{BOLD}┌────────────────────────────┐{RESET}")
    print(f"{BLUE}{BOLD}│   🧭  Delhi Metro Timings  │{RESET}")
    print(f"{BLUE}{BOLD}└────────────────────────────┘{RESET}")

    # 1) Choose station
    station_info = station()
    if station_info is None:
        return
    elif station_info == 'exit':
        return 'exit'

    # 2) Choose reference time
    time_info = time()
    if time_info is None:
        return
    elif time_info == 'exit':
        return 'exit'

    # Helper: convert 24h -> "h:mm AM/PM"
    def conv(hh, mm):
        """
        Convert hour, minute in 24-hour format to a user-friendly
        12-hour AM/PM string.
        """
        period = "AM"
        display_h = hh
        if hh == 0:
            display_h = 12
        elif hh == 12:
            period = "PM"
        elif hh > 12:
            display_h = hh - 12
            period = "PM"
        return f"{display_h}:{mm:02d} {period}"

    line_no = station_info[0]      # line number 1..4
    station_idx = station_info[1]  # station index (1-based in that line array)
    user_hour = int(time_info[0])  # user hour (station local time)
    user_min = int(time_info[1])   # user minute

    # Number of stations on the selected line
    if line_no == 1:
        num_stations = len(B)
    elif line_no == 2:
        num_stations = len(BB)
    elif line_no == 3:
        num_stations = len(M)
    else:
        num_stations = len(Y)

    at_first_station = (station_idx == 1)
    at_last_station  = (station_idx == num_stations)

    # Offset from FIRST station to selected station (forward direction)
    offset_forward_minutes_total = (station_idx - 1) * 3
    offset_forward_hour = offset_forward_minutes_total // 60
    offset_forward_min = offset_forward_minutes_total % 60

    # Offset from LAST station to selected station (backward direction)
    offset_backward_minutes_total = (num_stations - station_idx) * 3
    offset_backward_hour = offset_backward_minutes_total // 60
    offset_backward_min = offset_backward_minutes_total % 60

    # Convert user time at station -> equivalent time at FIRST station (forward)
    first_hour_equiv = user_hour - offset_forward_hour
    first_min_equiv = user_min - offset_forward_min
    if first_min_equiv < 0:
        first_min_equiv += 60
        first_hour_equiv -= 1
    # wrap negative origin hours to previous day (e.g., -2 → 22)
    while first_hour_equiv < 0:
        first_hour_equiv += 24

    # Convert user time at station -> equivalent time at LAST station (backward)
    last_hour_equiv = user_hour - offset_backward_hour
    last_min_equiv = user_min - offset_backward_min
    if last_min_equiv < 0:
        last_min_equiv += 60
        last_hour_equiv -= 1
    # wrap negative origin hours to previous day
    while last_hour_equiv < 0:
        last_hour_equiv += 24

    # forward_arrivals: towards last station of the line (station_info[2])
    # backward_arrivals: towards first station of the line (station_info[3])
    forward_arrivals = []
    backward_arrivals = []

    print()  # blank line for cleaner output

    # ---------------- FORWARD DIRECTION: towards v[2] ----------------
    if not at_last_station:
        # Service window at ORIGIN: 06:00–23:00
        if (first_hour_equiv < 6 or first_hour_equiv > 23) or (first_hour_equiv == 23 and first_min_equiv > 0):
            print(f"\n{RED}{BOLD}❌ No service available towards {UNDER}{station_info[2]}{RESET}{RED}{BOLD} at this time.{RESET}")
        elif (first_hour_equiv == 23 and first_min_equiv == 0):
            print(f"\n{YELLOW}{BOLD}⚠️  Last metro towards {UNDER}{station_info[2]}{RESET}{YELLOW}{BOLD} will arrive at {conv(user_hour, 0)}{RESET}")
        else:
            scan_hour = first_hour_equiv
            scan_min = first_min_equiv

            # Scan timetable from this equivalent origin time until we get up to 3 departures
            while scan_hour <= 23 and len(forward_arrivals) < 3:
                minutes_list = d.get(scan_hour, [])
                for departure_minute_at_origin in minutes_list:
                    if departure_minute_at_origin >= scan_min:
                        # Reconvert to station time by adding offsets
                        arrival_hour = scan_hour + offset_forward_hour
                        arrival_min = departure_minute_at_origin + offset_forward_min
                        if arrival_min >= 60:
                            arrival_min -= 60
                            arrival_hour += 1
                        # wrap back to 0–23 to avoid 24,25,... hours
                        arrival_hour %= 24
                        forward_arrivals.append((arrival_hour, arrival_min))
                        if len(forward_arrivals) == 3:
                            break
                scan_hour += 1
                scan_min = 0

            if len(forward_arrivals) == 0:
                print(f"\n{RED}{BOLD}❌ No service available towards {UNDER}{station_info[2]}{RESET}{RED}{BOLD} at this time.{RESET}")
            else:
                next_h, next_m = forward_arrivals[0]
                print(f"\n{BOLD}{CYAN}Towards {station_info[2]}:{RESET}")
                print(f"  ➤    {BOLD}Next metro will arrive at{RESET} {YELLOW}{conv(next_h, next_m)}{RESET}")
                if len(forward_arrivals) > 1:
                    for (sub_h, sub_m) in forward_arrivals[1:]:
                        print(f"  ➤    {BOLD}Subsequent metro will arrive at{RESET} {YELLOW}{conv(sub_h, sub_m)}{RESET}")

    # ---------------- BACKWARD DIRECTION: towards v[3] ----------------
    if not at_first_station:
        # Service window at ORIGIN: 06:00–23:00
        if (last_hour_equiv < 6 or last_hour_equiv > 23) or (last_hour_equiv == 23 and last_min_equiv > 0):
            print(f"\n{RED}{BOLD}❌ No service available towards {UNDER}{station_info[3]}{RESET}{RED}{BOLD} at this time.{RESET}")
        elif (last_hour_equiv == 23 and last_min_equiv == 0):
            print(f"\n{YELLOW}{BOLD}⚠️  Last metro towards {UNDER}{station_info[3]}{RESET}{YELLOW}{BOLD} will arrive at {conv(user_hour, 0)}{RESET}")
        else:
            scan_hour = last_hour_equiv
            scan_min = last_min_equiv

            # Scan origin timetable to get up to 3 departures
            while scan_hour <= 23 and len(backward_arrivals) < 3:
                minutes_list = d.get(scan_hour, [])
                for departure_minute_at_origin in minutes_list:
                    if departure_minute_at_origin >= scan_min:
                        arrival_hour = scan_hour + offset_backward_hour
                        arrival_min = departure_minute_at_origin + offset_backward_min
                        if arrival_min >= 60:
                            arrival_min -= 60
                            arrival_hour += 1
                        # wrap back to 0–23 to avoid 24,25,... hours
                        arrival_hour %= 24
                        backward_arrivals.append((arrival_hour, arrival_min))
                        if len(backward_arrivals) == 3:
                            break
                scan_hour += 1
                scan_min = 0

            if len(backward_arrivals) == 0:
                print(f"\n{RED}{BOLD}❌ No service available towards {UNDER}{station_info[3]}{RESET}{RED}{BOLD} at this time.{RESET}")
            else:
                next_h, next_m = backward_arrivals[0]
                print(f"\n{BOLD}{CYAN}Towards {station_info[3]}:{RESET}")
                print(f"  ➤    {BOLD}Next metro will arrive at{RESET} {YELLOW}{conv(next_h, next_m)}{RESET}")
                if len(backward_arrivals) > 1:
                    for (sub_h, sub_m) in backward_arrivals[1:]:
                        print(f"  ➤    {BOLD}Subsequent metro will arrive at{RESET} {YELLOW}{conv(sub_h, sub_m)}{RESET}")

# ============================================================
# 8. JOURNEY PLANNER
# ============================================================

def journey():
    """
    Plan a journey between two stations.
    """

    # ============================================================
    # 8. HELPER FUNCTIONS FOR JOURNEY
    # ============================================================

    def station_name(line_no, idx, line_lists):
        """
        Get station name for a given (line_no, 1-based index).
        """
        return line_lists[line_no][idx - 1][1].strip()


    def build_pair_candidates(path, line_lists, simple_line, interchange):
        """
        For a path like [Line 1, Line 2, Line 3, ...], build a list:
        pair_cands[i] = list of possible interchange stations between Line i and Line i+1.
        """
        pair_cands = []
        for i in range(len(path) - 1):
            current_line = path[i]
            next_line = path[i + 1]
            key = (simple_line[current_line], simple_line[next_line])

            # If there is no defined interchange between these line names
            if key not in interchange:
                return None

            interchange_station_names = interchange[key]
            current_line_data = line_lists[current_line]
            next_line_data = line_lists[next_line]
            choices_for_pair = []

            for ic_name in interchange_station_names:
                idx_on_current = None
                idx_on_next = None

                # Find station index on current_line
                for j in range(len(current_line_data)):
                    if current_line_data[j][1].strip() == ic_name:
                        idx_on_current = j + 1
                        break

                # Find station index on next_line
                for j in range(len(next_line_data)):
                    if next_line_data[j][1].strip() == ic_name:
                        idx_on_next = j + 1
                        break

                # If station present on both lines, it is a valid interchange
                if idx_on_current is not None and idx_on_next is not None:
                    choices_for_pair.append({
                        'name'    : ic_name,
                        'idx_prev': idx_on_current,
                        'idx_next': idx_on_next
                    })

            # If no interchange station actually found, entire path invalid
            if not choices_for_pair:
                return None

            pair_cands.append(choices_for_pair)

        return pair_cands


    def simulate_route(path, pair_cands, choice_indices,
                    start_line, start_idx, start_total, end_idx,
                    next_departure, to_minutes, from_minutes):
        """
        Simulate a complete journey for a fixed 'path' of lines
        and a fixed choice of interchange,start and end stations for each line-pair.
        """
        steps = []
        current_line = start_line
        current_idx = start_idx
        current_minutes = start_total

        # For each line transition (each interchange)
        for i in range(len(path) - 1):
            next_line = path[i + 1]
            chosen_candidate = pair_cands[i][choice_indices[i]]
            ic_name = chosen_candidate['name']
            exit_idx = chosen_candidate['idx_prev']   # index on current_line
            entry_idx = chosen_candidate['idx_next']  # index on next_line

            # ----- Ride on current_line to the interchange station -----
            hops = abs(exit_idx - current_idx)
            if hops > 0:
                forward = (exit_idx > current_idx)
                cur_h, cur_m = from_minutes(current_minutes)
                dep = next_departure(current_line, current_idx, cur_h, cur_m, forward)
                if dep is None:
                    # No train available in this direction anymore
                    return None, None
                dep_h, dep_m = dep
                dep_total = to_minutes(dep_h, dep_m)
                travel_min = hops * 3
                arr_total = dep_total + travel_min
                arr_h, arr_m = from_minutes(arr_total)

                steps.append({
                    'type': 'ride',
                    'line': current_line,
                    'from_idx': current_idx,
                    'to_idx': exit_idx,
                    'dep_h': dep_h, 'dep_m': dep_m,
                    'arr_h': arr_h, 'arr_m': arr_m,
                    'travel_min': travel_min
                })
                current_minutes = arr_total
            # else: already at the interchange station, no ride needed

            # ----- Interchange step (+5 min waiting / walking time) -----
            current_minutes += 5
            ic_h, ic_m = from_minutes(current_minutes)
            steps.append({
                'type': 'interchange',
                'name': ic_name,
                'time_h': ic_h,
                'time_m': ic_m
            })

            # ----- Switch to next line at the corresponding index -----
            current_line = next_line
            current_idx = entry_idx

        # ----- Final ride on last line to destination station -----
        hops = abs(end_idx - current_idx)
        if hops > 0:
            forward = (end_idx > current_idx)
            cur_h, cur_m = from_minutes(current_minutes)
            dep = next_departure(current_line, current_idx, cur_h, cur_m, forward)
            if dep is None:
                return None, None
            dep_h, dep_m = dep
            dep_total = to_minutes(dep_h, dep_m)
            travel_min = hops * 3
            final_total = dep_total + travel_min
            arr_h, arr_m = from_minutes(final_total)

            steps.append({
                'type': 'ride',
                'line': current_line,
                'from_idx': current_idx,
                'to_idx': end_idx,
                'dep_h': dep_h, 'dep_m': dep_m,
                'arr_h': arr_h, 'arr_m': arr_m,
                'travel_min': travel_min
            })
        else:
            # Already at destination station after last interchange
            final_total = current_minutes
            arr_h, arr_m = from_minutes(final_total)

        return final_total, steps


    # ---------- Fare helper (based on total number of stations) ----------
    def compute_fare(total_stations):
        """
        Compute fare based on number of stations travelled.
        """
        return total_stations * 6
    
    def compute_carbon_savings(total_stations):
        """
        Compute CO2 savings 
        Returns savings in kg.
        """
        savings_grams = total_stations * 150
        return savings_grams

    # Map line number → station list
    line_lists = {1: B, 2: BB, 3: M, 4: Y}
    line_names = {
        1: "Blue Line",
        2: "Blue-Branch Line",
        3: "Magenta Line",
        4: "Yellow Line"
    }
    simple_line = {
        1: "Blue",
        2: "Blue Branch",
        3: "Magenta",
        4: "Yellow"
    }

    # ---- Time helper functions for minutes arithmetic ----

    def to_minutes(hh, mm):
        """Convert hour, minute to total minutes from midnight."""
        return hh * 60 + mm

    def from_minutes(total):
        """Convert total minutes from midnight to (hour, minute)."""
        hh = total // 60
        mm = total % 60
        return hh, mm

    def conv(hh, mm):
        """
        Convert 24-hour time -> 'h:mm AM/PM'.
        """
        period = "AM"
        display_h = hh
        if hh == 0:
            display_h = 12
        elif hh == 12:
            period = "PM"
        elif hh > 12:
            display_h = hh - 12
            period = "PM"
        return f"{display_h}:{mm:02d} {period}"

    def next_departure(line_no, station_idx, cur_h, cur_m, forward):
        """
        Nothing just the timings() logic.
        """
        line_data = line_lists[line_no]
        num_stations = len(line_data)

        if forward:
            offset_min = (station_idx - 1) * 3
        else:
            offset_min = (num_stations - station_idx) * 3

        offset_h = offset_min // 60
        offset_m = offset_min % 60

        # Convert station time -> origin-equivalent time
        origin_hour = cur_h - offset_h
        origin_min = cur_m - offset_m
        if origin_min < 0:
            origin_min += 60
            origin_hour -= 1
        # wrap negative origin hours to previous day (e.g., -2 → 22)
        while origin_hour < 0:
            origin_hour += 24

        # Metro service window (at origin station): 06–23
        if (origin_hour < 6 or origin_hour > 23) or (origin_hour == 23 and origin_min > 0):
            return None

        scan_hour_origin = origin_hour
        scan_min_origin = origin_min

        # Scan timetable at origin station
        while scan_hour_origin <= 23:
            minutes_list = d.get(scan_hour_origin, [])
            for departure_minute_origin in minutes_list:
                if departure_minute_origin >= scan_min_origin:
                    # Found a departure at origin, convert back to station time
                    dep_origin_h = scan_hour_origin
                    dep_origin_m = departure_minute_origin
                    dep_station_h = dep_origin_h + offset_h
                    dep_station_m = dep_origin_m + offset_m
                    if dep_station_m >= 60:
                        dep_station_m -= 60
                        dep_station_h += 1
                    # wrap to 0–23 so conv() never sees 24,25,...
                    dep_station_h %= 24
                    return dep_station_h, dep_station_m
            scan_hour_origin += 1
            scan_min_origin = 0

        return None

    # ---------------1. Main Journay Functionality --------------------
    print(f"\n{CYAN}{BOLD}┌────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}{BOLD}│     🧭  Delhi Metro Journey Planner    │{RESET}")
    print(f"{CYAN}{BOLD}└────────────────────────────────────────┘{RESET}")

    # ---------------- 2. SELECT START & DEST ----------------
    print(f"\n{GREEN}{BOLD}🟢 Select your START station:{RESET}")
    start_station_info = station()
    if start_station_info is None:
        return
    if start_station_info == 'exit':
        return 'exit'

    print(f"\n{RED}{BOLD}🔴 Select your DESTINATION station:{RESET}")
    end_station_info = station()
    if end_station_info is None:
        return
    if end_station_info == 'exit':
        return 'exit'

    start_line = start_station_info[0]
    start_idx  = start_station_info[1]
    end_line   = end_station_info[0]
    end_idx    = end_station_info[1]

    start_line_data = line_lists[start_line]
    end_line_data   = line_lists[end_line]
    start_name = start_line_data[start_idx - 1][1].strip()
    end_name   = end_line_data[end_idx - 1][1].strip()

    # ---------------- 3. JOURNEY START TIME ----------------
    print(f"\n{BOLD}⏰ Now choose your JOURNEY START TIME:{RESET}")
    time_info = time()
    if time_info is None:
        return
    if time_info == 'exit':
        return 'exit'

    start_h = int(time_info[0])
    start_m = int(time_info[1])
    start_total = to_minutes(start_h, start_m)

    # =======================================================
    #   1: MINIMUM TIME
    # =======================================================
    def min_time():
        """
        Minimise total travel time (riding + interchange time + waiting time).
        """

        # Case 1: Same station (start == destination)
        if start_line == end_line and start_idx == end_idx:
            print(f"\n{BOLD}{CYAN}📜 Journey Plan:{RESET}")
            print(f"Start at {WHITE}{start_name}{RESET} ({line_names[start_line]})")
            print(f"{GREEN}{BOLD}You are already at your destination.{RESET}")
            print(f"{YELLOW}Total travel time: 0 minutes{RESET}")
            print(f"{BOLD}🚉 Total Stations:{RESET} {YELLOW}0{RESET}")
            print(f"{BOLD}💰 Estimated Fare:{RESET} {YELLOW}₹0{RESET}")
            print(f"{BOLD}🌿 Carbon Saved:{RESET}{GREEN} 0 gms CO₂ {RESET}")
            return

        # Case 2: Same line (no interchange needed)
        if start_line == end_line:
            # Direct ride on one line
            moving_forward = (end_idx > start_idx)
            hops = abs(end_idx - start_idx)
            cur_h, cur_m = from_minutes(start_total)

            dep = next_departure(start_line, start_idx, cur_h, cur_m, moving_forward)
            if dep is None:
                print(f"\n{RED}{BOLD}❌ No metro available from this station at the given time for the selected destination.{RESET}")
                return

            dep_h, dep_m = dep
            dep_total = to_minutes(dep_h, dep_m)
            print(f"\n{BOLD}{CYAN}🚅 Direct Ride:{RESET}")
            print(f"{BOLD}Line:{RESET}   {WHITE}{line_names[start_line]}{RESET}")
            print(f"{BOLD}From:{RESET}   {WHITE}{start_name} Station{RESET}")
            print(f"{BOLD}To:{RESET}     {WHITE}{end_name} Station{RESET}")
            print(f"{BOLD}Board:{RESET}  {YELLOW}{conv(dep_h, dep_m)}{RESET}")

            travel_min = hops * 3
            arrive_total = dep_total + travel_min
            arr_h, arr_m = from_minutes(arrive_total)

            print(f"{BOLD}Arrive:{RESET} {YELLOW}{conv(arr_h, arr_m)}{RESET}")
            total_time = arrive_total - start_total

            # Fare calculation for direct route
            total_stations = hops
            fare = compute_fare(total_stations)
            carbon_saved = compute_carbon_savings(total_stations)

            print(f"{GREEN}{BOLD}⏱  Total travel time: {total_time} minutes{RESET}")
            print(f"{BOLD}🚉 Total Stations:{RESET} {YELLOW}{total_stations}{RESET}")
            print(f"{BOLD}💰 Estimated Fare:{RESET} {YELLOW}₹{fare}{RESET}")
            print(f"{BOLD}🌿 Carbon Saved:{RESET} {GREEN}{carbon_saved:.2f} gms CO₂{RESET}")
            return

        # Case 3: Different lines → consider multi-interchange routes
        all_lines = [1, 2, 3, 4]
        other_lines = [x for x in all_lines if x not in (start_line, end_line)]

        candidate_paths = []
        # 1-interchange path: [start_line → end_line]
        candidate_paths.append([start_line, end_line])
        # 2-interchange paths: [start_line → mid → end_line]
        for mid in other_lines:
            candidate_paths.append([start_line, mid, end_line])
        # 3-interchange paths: [start_line → a → b → end_line] and [start_line → b → a → end_line]
        if len(other_lines) == 2:
            a, b = other_lines[0], other_lines[1]
            candidate_paths.append([start_line, a, b, end_line])
            candidate_paths.append([start_line, b, a, end_line])

        best_final = None
        best_steps = None

        # Try all candidate line paths and all combinations of interchange stations
        for path in candidate_paths:
            pair_cands = build_pair_candidates(path, line_lists, simple_line, interchange)
            if pair_cands is None:
                continue

            num_interchanges = len(pair_cands)

            if num_interchanges == 1:
                for i0 in range(len(pair_cands[0])):
                    choice_indices = [i0]
                    final_total, steps = simulate_route(
                        path, pair_cands, choice_indices,
                        start_line, start_idx, start_total, end_idx,
                        next_departure, to_minutes, from_minutes
                    )
                    if final_total is None:
                        continue
                    if best_final is None or final_total < best_final:
                        best_final = final_total
                        best_steps = steps

            elif num_interchanges == 2:
                for i0 in range(len(pair_cands[0])):
                    for i1 in range(len(pair_cands[1])):
                        choice_indices = [i0, i1]
                        final_total, steps = simulate_route(
                            path, pair_cands, choice_indices,
                            start_line, start_idx, start_total, end_idx,
                            next_departure, to_minutes, from_minutes
                        )
                        if final_total is None:
                            continue
                        if best_final is None or final_total < best_final:
                            best_final = final_total
                            best_steps = steps

            elif num_interchanges == 3:
                for i0 in range(len(pair_cands[0])):
                    for i1 in range(len(pair_cands[1])):
                        for i2 in range(len(pair_cands[2])):
                            choice_indices = [i0, i1, i2]
                            final_total, steps = simulate_route(
                                path, pair_cands, choice_indices,
                                start_line, start_idx, start_total, end_idx,
                                next_departure, to_minutes, from_minutes
                            )
                            if final_total is None:
                                continue
                            if best_final is None or final_total < best_final:
                                best_final = final_total
                                best_steps = steps

        if best_final is None or best_steps is None:
            print(f"\n{RED}{BOLD}❌ No valid route (with service) found between these stations at this time.{RESET}")
            return

        # --------- Print chosen minimum-time route ----------
        step_no = 1
        total_stations = 0

        for i in range(len(best_steps)):
            step = best_steps[i]

            if step['type'] == 'ride':
                line_no = step['line']
                from_idx = step['from_idx']
                to_idx = step['to_idx']
                from_name = station_name(line_no, from_idx, line_lists)
                to_name = station_name(line_no, to_idx, line_lists)
                dep_h, dep_m = step['dep_h'], step['dep_m']
                arr_h, arr_m = step['arr_h'], step['arr_m']
                travel_min = step['travel_min']

                hops = travel_min // 3
                total_stations += hops

                direction_icon = "➡️" if to_idx > from_idx else "⬅️"

                print(f"\n{BOLD}{CYAN}Step {step_no}{RESET} {direction_icon}")
                print(f"   {BOLD}Line:{RESET}   {WHITE}{line_names[line_no]}{RESET}")
                print(f"   {BOLD}From:{RESET}   {WHITE}{from_name}{RESET}")
                print(f"   {BOLD}To:{RESET}     {WHITE}{to_name}{RESET}")
                print(f"   {BOLD}Time:{RESET}   {YELLOW}{conv(dep_h, dep_m)}{RESET}  →  {YELLOW}{conv(arr_h, arr_m)}{RESET}")
                step_no += 1

            elif step['type'] == 'interchange':
                ic_name = step['name']

                next_line_text = None
                direction_terminal = None

                # Look ahead to the next ride step to print line & direction
                if i + 1 < len(best_steps) and best_steps[i + 1]['type'] == 'ride':
                    ride_next = best_steps[i + 1]
                    next_line_no = ride_next['line']
                    next_line_text = line_names[next_line_no]
                    from_idx2 = ride_next['from_idx']
                    to_idx2 = ride_next['to_idx']

                    if to_idx2 > from_idx2:
                        direction_terminal = line_lists[next_line_no][-1][1].strip()
                    else:
                        direction_terminal = line_lists[next_line_no][0][1].strip()

                print(f"\n{MAGENTA}{BOLD}Step {step_no}{RESET} 🔁  Interchange at {UNDER}{ic_name}{RESET}", end='')
                if next_line_text is not None:
                    if direction_terminal is not None:
                        print(f" for {WHITE}{next_line_text}{RESET} towards {WHITE}{direction_terminal}{RESET}")
                    else:
                        print(f" for {WHITE}{next_line_text}{RESET}")
                else:
                    print()
                step_no += 1

        total_time = best_final - start_total
        total_time_h, total_time_m = from_minutes(total_time)

        fare = compute_fare(total_stations)
        carbon_saved = compute_carbon_savings(total_stations)

        print(f"\n{GREEN}{BOLD}✅ Journey Completed!{RESET}")
        print(f"{BOLD}🏁 Destination:{RESET} {WHITE}{end_name}{RESET}")
        print(f"{BOLD}🕒 Start Time:{RESET} {YELLOW}{conv(start_h, start_m)}{RESET}")
        if total_time_h == 0:
            print(f"{BOLD}⏱  Total Time:{RESET} {YELLOW}{total_time} Minutes{RESET}")
        else:
            print(f"{BOLD}⏱  Total Time:{RESET} {YELLOW}{total_time_h} Hours {total_time_m} Minutes{RESET}")
        print(f"{BOLD}🚉 Total Stations:{RESET} {YELLOW}{total_stations}{RESET}")
        print(f"{BOLD}💰 Estimated Fare:{RESET} {YELLOW}₹{fare}{RESET}")
        print(f"{BOLD}🌿 Carbon Saved:{RESET} {GREEN}{carbon_saved:.2f} gms CO₂{RESET}")
        return

    # =======================================================
    #   STRATEGY 2: MINIMUM INTERCHANGES
    # =======================================================
    def min_interchange():
        """
        Strategy 2:
        Minimise number of interchanges
        """

        # Case 1: Same station
        if start_line == end_line and start_idx == end_idx:
            print(f"\n{BOLD}{CYAN}📜 Journey Plan:{RESET}")
            print(f"Start at {WHITE}{start_name}{RESET} ({line_names[start_line]})")
            print(f"{GREEN}{BOLD}You are already at your destination.{RESET}")
            print(f"{YELLOW}Total travel time: 0 minutes{RESET}")
            print(f"{BOLD}🚉 Total Stations:{RESET} {YELLOW}0{RESET}")
            print(f"{BOLD}💰 Estimated Fare:{RESET} {YELLOW}₹0{RESET}")
            return

        # Case 2: Same line → 0 interchanges, already minimal
        if start_line == end_line:
            moving_forward = (end_idx > start_idx)
            hops = abs(end_idx - start_idx)
            cur_h, cur_m = from_minutes(start_total)

            dep = next_departure(start_line, start_idx, cur_h, cur_m, moving_forward)
            if dep is None:
                print(f"\n{RED}{BOLD}❌ No metro available from this station at the given time for the selected destination.{RESET}")
                return

            dep_h, dep_m = dep
            dep_total = to_minutes(dep_h, dep_m)
            print(f"\n{BOLD}{CYAN}🚅 Direct Ride (Min Interchanges):{RESET}")
            print(f"{BOLD}Line:{RESET}   {WHITE}{line_names[start_line]}{RESET}")
            print(f"{BOLD}From:{RESET}   {WHITE}{start_name} Station{RESET}")
            print(f"{BOLD}To:{RESET}     {WHITE}{end_name} Station{RESET}")
            print(f"{BOLD}Board:{RESET}  {YELLOW}{conv(dep_h, dep_m)}{RESET}")

            travel_min = hops * 3
            arrive_total = dep_total + travel_min
            arr_h, arr_m = from_minutes(arrive_total)

            print(f"{BOLD}Arrive:{RESET} {YELLOW}{conv(arr_h, arr_m)}{RESET}")
            total_time = arrive_total - start_total

            total_stations = hops
            fare = compute_fare(total_stations)

            print(f"{GREEN}{BOLD}⏱  Total travel time: {total_time} minutes{RESET}")
            print(f"{BOLD}🚉 Total Stations:{RESET} {YELLOW}{total_stations}{RESET}")
            print(f"{BOLD}💰 Estimated Fare:{RESET} {YELLOW}₹{fare}{RESET}")
            return

        # Case 3: Different lines → use triangle logic
        line_path = None

        if start_line == 2:  # Blue Branch
            if end_line == 1:
                line_path = [2, 1]
            elif end_line == 3:
                line_path = [2, 1, 3]
            elif end_line == 4:
                line_path = [2, 1, 4]

        elif start_line == 1:  # Blue
            if end_line == 2:
                line_path = [1, 2]
            elif end_line == 3:
                line_path = [1, 3]
            elif end_line == 4:
                line_path = [1, 4]

        elif start_line == 3:  # Magenta
            if end_line == 1:
                line_path = [3, 1]
            elif end_line == 2:
                line_path = [3, 1, 2]
            elif end_line == 4:
                line_path = [3, 4]

        elif start_line == 4:  # Yellow
            if end_line == 1:
                line_path = [4, 1]
            elif end_line == 2:
                line_path = [4, 1, 2]
            elif end_line == 3:
                line_path = [4, 3]

        if line_path is None:
            print(f"\n{RED}{BOLD}❌ No min-interchange path defined between these lines in the current network.{RESET}")
            return

        pair_cands = build_pair_candidates(line_path, line_lists, simple_line, interchange)
        if pair_cands is None:
            print(f"\n{RED}{BOLD}❌ No valid route (with service) found between these stations at this time.{RESET}")
            return

        best_final = None
        best_steps = None
        best_interchanges = len(pair_cands)

        num_interchanges = len(pair_cands)

        if num_interchanges == 1:
            for i0 in range(len(pair_cands[0])):
                choice_indices = [i0]
                final_total, steps = simulate_route(
                    line_path, pair_cands, choice_indices,
                    start_line, start_idx, start_total, end_idx,
                    next_departure, to_minutes, from_minutes
                )
                if final_total is None:
                    continue
                if best_final is None or final_total < best_final:
                    best_final = final_total
                    best_steps = steps

        elif num_interchanges == 2:
            for i0 in range(len(pair_cands[0])):
                for i1 in range(len(pair_cands[1])):
                    choice_indices = [i0, i1]
                    final_total, steps = simulate_route(
                        line_path, pair_cands, choice_indices,
                        start_line, start_idx, start_total, end_idx,
                        next_departure, to_minutes, from_minutes
                    )
                    if final_total is None:
                        continue
                    if best_final is None or final_total < best_final:
                        best_final = final_total
                        best_steps = steps

        elif num_interchanges == 3:
            for i0 in range(len(pair_cands[0])):
                for i1 in range(len(pair_cands[1])):
                    for i2 in range(len(pair_cands[2])):
                        choice_indices = [i0, i1, i2]
                        final_total, steps = simulate_route(
                            line_path, pair_cands, choice_indices,
                            start_line, start_idx, start_total, end_idx,
                            next_departure, to_minutes, from_minutes
                        )
                        if final_total is None:
                            continue
                        if best_final is None or final_total < best_final:
                            best_final = final_total
                            best_steps = steps

        if best_final is None or best_steps is None:
            print(f"\n{RED}{BOLD}❌ No valid route (with service) found between these stations at this time.{RESET}")
            return

        # --------- Print chosen min-interchange route ----------
        step_no = 1
        total_stations = 0

        for i in range(len(best_steps)):
            step = best_steps[i]

            if step['type'] == 'ride':
                line_no = step['line']
                from_idx = step['from_idx']
                to_idx = step['to_idx']
                from_name = station_name(line_no, from_idx, line_lists)
                to_name = station_name(line_no, to_idx, line_lists)
                dep_h, dep_m = step['dep_h'], step['dep_m']
                arr_h, arr_m = step['arr_h'], step['arr_m']
                travel_min = step['travel_min']

                hops = travel_min // 3
                total_stations += hops

                direction_icon = "➡️" if to_idx > from_idx else "⬅️"

                print(f"\n{BOLD}{CYAN}Step {step_no}{RESET} {direction_icon}")
                print(f"   {BOLD}Line:{RESET}   {WHITE}{line_names[line_no]}{RESET}")
                print(f"   {BOLD}From:{RESET}   {WHITE}{from_name}{RESET}")
                print(f"   {BOLD}To:{RESET}     {WHITE}{to_name}{RESET}")
                print(f"   {BOLD}Time:{RESET}   {YELLOW}{conv(dep_h, dep_m)}{RESET}  →  {YELLOW}{conv(arr_h, arr_m)}{RESET}")
                step_no += 1

            elif step['type'] == 'interchange':
                ic_name = step['name']

                next_line_text = None
                direction_terminal = None

                if i + 1 < len(best_steps) and best_steps[i + 1]['type'] == 'ride':
                    ride_next = best_steps[i + 1]
                    next_line_no = ride_next['line']
                    next_line_text = line_names[next_line_no]
                    from_idx2 = ride_next['from_idx']
                    to_idx2 = ride_next['to_idx']
                    if to_idx2 > from_idx2:
                        direction_terminal = line_lists[next_line_no][-1][1].strip()
                    else:
                        direction_terminal = line_lists[next_line_no][0][1].strip()

                print(f"\n{MAGENTA}{BOLD}Step {step_no}{RESET} 🔁  Interchange at {UNDER}{ic_name}{RESET}", end='')
                if next_line_text is not None:
                    if direction_terminal is not None:
                        print(f" for {WHITE}{next_line_text}{RESET} towards {WHITE}{direction_terminal}{RESET}")
                    else:
                        print(f" for {WHITE}{next_line_text}{RESET}")
                else:
                    print()
                step_no += 1

        total_time = best_final - start_total
        total_time_h, total_time_m = from_minutes(total_time)

        fare = compute_fare(total_stations)
        carbon_saved = compute_carbon_savings(total_stations)

        print(f"\n{GREEN}{BOLD}✅ Journey Completed! (Min Interchanges){RESET}")
        print(f"{BOLD}🔁 Interchanges Used:{RESET} {YELLOW}{best_interchanges}{RESET}")
        print(f"{BOLD}🏁 Destination:{RESET} {WHITE}{end_name}{RESET}")
        print(f"{BOLD}🕒 Start Time:{RESET} {YELLOW}{conv(start_h, start_m)}{RESET}")
        if total_time_h == 0:
            print(f"{BOLD}⏱  Total Time:{RESET} {YELLOW}{total_time} Minutes{RESET}")
        else:
            print(f"{BOLD}⏱  Total Time:{RESET} {YELLOW}{total_time_h} Hours {total_time_m} Minutes{RESET}")
        print(f"{BOLD}🚉 Total Stations:{RESET} {YELLOW}{total_stations}{RESET}")
        print(f"{BOLD}💰 Estimated Fare:{RESET} {YELLOW}₹{fare}{RESET}")
        print(f"{BOLD}🌿 Carbon Saved:{RESET} {GREEN}{carbon_saved:.2f} gms CO₂{RESET}")
        return

    # =======================================================
    #   USER CHOICE
    # =======================================================
    while True:
        try:
            print()
            print(f"{BOLD}{CYAN}How would you like to optimise your journey?{RESET}")
            print(f"{BOLD}  1️⃣  {WHITE}Minimum Time{RESET}")
            print(f"{BOLD}  2️⃣  {WHITE}Minimum Interchanges{RESET}")
            print(f"{BOLD}  3️⃣  {YELLOW}🔙 Go to Main Menu{RESET}")
            print(f"{BOLD}  4️⃣  {RED}❌ Exit{RESET}")
            choice = int(input(f"{YELLOW}➡️  Enter your choice: {RESET}"))
            assert choice in [1, 2, 3, 4]
        except:
            print(f"\n{RED}{BOLD}⚠️  Invalid input.{RESET} Please select 1, 2, 3 or 4.")
            continue

        if choice == 3:
            # Go back to main() menu
            return None
        elif choice == 4:
            # Exit the whole program
            return 'exit'
        elif choice == 1:
            return min_time()
        else:
            return min_interchange()


# ============================================================
# 9. MAIN INTERACTION POINT
# ============================================================

def main():
    """
    Main interaction loop for the Delhi Metro Simulator.
    Presents a simple menu to the user:
    """
    while True:
        try:
            print()
            print(f"{BOLD}  1️⃣  {WHITE}Check next metro timings{RESET}")
            print(f"{BOLD}  2️⃣  {WHITE}Plan your metro journey{RESET}")
            print(f"{BOLD}  3️⃣  {RED}Exit{RESET}")
            main_choice = int(input(f"{YELLOW}➡️  Enter your choice: {RESET}"))

            assert main_choice in [1, 2, 3]
        except:
            print(f"\n{RED}{BOLD}⚠️  Invalid input.{RESET} Please select 1, 2, or 3.")
            continue

        if main_choice == 3:
            exit()
            return

        if main_choice == 1:
            timings_result = timings()
            if timings_result is None:
                print(f"\n{YELLOW}↩️  Returning to main menu...{RESET}\n")
                continue
            exit()
            return
        else:
            journey_result = journey()
            if journey_result is None:
                print(f"\n{YELLOW}↩️  Returning to main menu...{RESET}\n")
                continue
            exit()
            return

# ============================================================
# 10. PROGRAM ENTRY POINT
# ============================================================

print(f"{CYAN}{BOLD}┌──────────────────────────────────────┐{RESET}")
print(f"{CYAN}{BOLD}│   🚇  Delhi Metro Simulator Menu     │{RESET}")
print(f"{CYAN}{BOLD}└──────────────────────────────────────┘{RESET}")

print(f"📌 {YELLOW}{ITALIC}{BOLD}{UNDER}Dear user, Please enter all your choices in the complete simulater by entering number beside the option you want to choose.{RESET}")

main()