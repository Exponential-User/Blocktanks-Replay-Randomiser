import json, random, sys, zlib
# Usage: run the Da-Funny.bat file and follow the prompts, or just this script.

idPool = {}  # Dictionary to store usernames and their corresponding IDs
once = False # A Basic switch
var4 = None

if not len(sys.argv) <= 1:
    var1 = sys.argv[1]  # options for randomization (string | required for randomizer)*
    var2 = int(sys.argv[2]) if sys.argv[2].isdigit() and 0 <= int(sys.argv[2]) < 255 else 0  # min random (int | required for randomizer)*
    var3 = int(sys.argv[3]) if sys.argv[3].isdigit() and 0 < int(sys.argv[3]) < 255 else 255  # max random (int | required for randomizer)*
    var4 = sys.argv[4]  # encode/decode/randomize/acqiureUsernames/getMinMax (string | Required)*
    var5 = sys.argv[5]  # pretty print (string [yes/no] | Optional)
    var6 = sys.argv[6]  # filename (string | Required for encoder/decoder)*
    var7 = sys.argv[7]  # chosen value to randomise (int | Optional)
    var8 = sys.argv[8]  # Player name or id (string/int | required for randomizer)*
    # * = These vars are mostly required but can be optional since there is a system in-place to user-input them if not provided.

if not var4=="getMinMax":
    if not len(sys.argv) <= 1: print("Funny BT replay modifier/randomizer by UnknownUser\n\n")

def encoder(x): # x = filename
    try:
        x
    except (NameError, ValueError):
        print("Warning: Missing or invalid arguments for encoder, restarting input prompts...\n")
        x = input("IMPORTANT: JSON must be in the same directory as this encoder.\n\nEnter the output .btnks file name (without extension): ")

    # Ensure the filename ends with .btnks
    if not x.endswith('.btnks'):
        x += '.btnks'

    # Read and parse the JSON
    with open('output.json', 'r', encoding='utf-8') as f:
        json_obj = json.load(f)

    # Convert JSON to a regular string
    json_string = json.dumps(json_obj)

    # Encode to UTF-8 bytes
    utf8_bytes = json_string.encode('utf-8')

    # Compress with zlib
    compressed = zlib.compress(utf8_bytes)

    # Write to output .btnks file
    with open(x, 'wb') as f:
        f.write(compressed)

    print(f"Encoded and saved to {x} in the same directory as the encoder.")

def decoder(x, x2):  # x = filename, x2 = pretty print (yes/no)
    try:
        x
        x2
    except (NameError, ValueError):
        print("Warning: Missing or invalid arguments for decoder, restarting input prompts...\n")
        x = input("IMPORTANT: The .btnks file must be in the same directory as this decoder.\n\nEnter the .btnks file name (with extension): ")
        x2 = input("Do you want to pretty-print the JSON output? (yes/no): ").strip().lower()

    # Step 1: Read the compressed file
    with open(x, 'rb') as f:
        compressed_data = f.read()

    # Step 2: Decompress the data
    decompressed = zlib.decompress(compressed_data)

    # Step 3: Decode to text
    text = decompressed.decode('utf-8')

    if (x2 == "yes"): 
        # Step 4 (optional): Parse and pretty-print JSON
        parsed_json = json.loads(text)
        pretty_json = json.dumps(parsed_json, indent=4)

    # Print or save
    with open('output.json', 'w', encoding='utf-8') as f:
        f.write(pretty_json if x2 == "yes" else text)

# var1 = Options, var2 = Min Rand, var3 = Max Rand, var7 = Column, var8 = Username or user ID
def randomizer(var1, var2, var3, var7, var8):
    with open('output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    acqiureUsernames(False)  # make sure usernames were not the previous ones

    try:
        var1
        var2 = int(var2)
        var3 = int(var3)
        var8
    except (NameError, ValueError):
        print("Warning: Missing or invalid arguments for randomizer, restarting input prompts...\n")
        var1 = input("Enter function option (data, bullets): ").strip().lower()
        acqiureUsernames(True)
        var8 = input("Enter the player name or ID to modify: ").strip().lower()
        var2 = int(input("Enter minimum random value (negative integer): "))
        var3 = int(input("Enter maximum random value (positive integer): "))

    if var1 == "data":
        replayVersion = data.get('replayVersion') # a string of the replay version

        if replayVersion != '1.0.2':
            print(f"Replay version is not supported\nReplay Version: {replayVersion}")
            input("Press enter to exit...")
            return

        print(f"\nRandomizing tank data for player '{var8}' between {var2} and {var3}...\n")
        
        if idPool == {}:
            index = 2
            # Loop through eventBuffer to find idPool entries
            while index < len(data.get('eventBuffer', [])):
                id_pool = data.get('eventBuffer', [])[index]['data'].get('idPool', {})
                for username, user_id_value in id_pool.items():
                    if username not in idPool or idPool[username] != user_id_value:
                        idPool[username] = user_id_value
                index += 1

        modified_entries = 0
        total_entries = 0

        replayHost = data.get('replayHost')  # a string of the host's Username
        col = int(var7) if var7 and str(var7).strip() not in ('', '0', 'None') else None

        if validateHostID(replayHost, var8) is not None and col == 7:
            for entry in data.get('aimBuffer', []):
                entry['angle'] = random.randint(map_to_angle(var2), map_to_angle(var3))
            with open('output.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, separators=(',', ':'))

        # Get the user Id in idPool and sets var8 to the ID if var8 contains a username
        if not var8.isdecimal():
            print("Username detected changing to matching user ID")
            if var8 in idPool:
                var8 = idPool[var8]

        for entry in data.get('binaryBuffer', []):
            if not isinstance(entry.get('data'), list):
                continue

            # Each entry['data'] is a full frame (world message)
            d = entry['data']

            # Basic safety
            if len(d) < 4:
                continue

            tank_count = d[3]
            byte_index = 4

            # Loop through each tank (8 bytes per tank)
            for t in range(tank_count):
                if byte_index + 7 >= len(d):
                    break

                id_raw = d[byte_index]
                player_id = id_raw // 4
                # o = id_raw % 4

                # Match the player ID or username
                try:
                    if str(player_id) == str(var8) or idPool.get(player_id, None) == var8:
                        # Randomise X, Y, vX, vY bytes
                        if col is not None: # Check if a specific column is provided
                            if col in [1, 2, 3, 4, 5, 6, 7]:  # Valid columns to randomize
                                # if validateHostID(replayHost, var8) is not None and col == 7:
                                #     print(f"Skipping angle randomization for player '{var8}' as they are the replay host.")
                                #     byte_index += 8
                                #     total_entries += 1
                                #     continue
                                d[byte_index + col] = random.randint(var2, var3)
                        else:  # Randomise all relevant bytes if no specific column is provided
                            d[byte_index + 1] = random.randint(var2 if 0 < var2 < 10 else random.randint(0, 10), var3 if 11 < var3 < 30 else random.randint(11, 30))  # X high
                            d[byte_index + 2] = random.randint(var2 if 0 < var2 < 10 else random.randint(0, 10), var3 if 11 < var3 < 30 else random.randint(11, 30))   # Y high
                            d[byte_index + 3] = random.randint(var2 if 0 < var2 < 126 else random.randint(0, 126), var3 if 126 < var3 < 255 else random.randint(127, 255))  # X low
                            d[byte_index + 4] = random.randint(var2 if 0 < var2 < 126 else random.randint(0, 126), var3 if 126 < var3 < 255 else random.randint(127, 255))  # Y low
                            d[byte_index + 5] = random.choice((var2, var3))  # vX component
                            d[byte_index + 6] = random.choice((var2, var3))  # vY component
                            # if validateHostID(replayHost, var8) is None:
                            d[byte_index + 7] = random.randint(var2, var3)  # Angle component

                        modified_entries += 1

                    total_entries += 1
                    byte_index += 8  # move to next tank
                except Exception as e:
                    print(f"Error processing tank data: {e}")
                    byte_index += 8  # Ensure we still move to the next tank

        if modified_entries > 0:
            print(f"Successfully randomized {modified_entries} entries for player {var8}. (Total entries checked: {total_entries})")
        else:
            print(f"No matching player '{var8}' found in replay data.")

        # Save the changes
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))

    elif var1 == "bullets":
        print("Bullets randomization not implemented yet.")
    else:
        print("Invalid function option. Please use 'data' or 'bullets'.")

    print("Randomization complete. Check output.json for results.")
    
def acqiureUsernames(switch):
    index = 2

    # Read the JSON file
    with open('output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Loop through eventBuffer to find idPool entries
    while index < len(data.get('eventBuffer', [])):
        id_pool = data.get('eventBuffer', [])[index]['data'].get('idPool', {})
        for username, user_id_value in id_pool.items():
            if username not in idPool or idPool[username] != user_id_value:
                idPool[username] = user_id_value
        index += 1

    replayHost = data.get('replayHost')  # a string of the host's Username

    # Save to userlist.txt for the batch script to read off of
    with open('userlist.txt', 'w', encoding='utf-8') as f:
        for username, user_id_value in idPool.items():
            f.write(f"{username},{user_id_value}\n")
            if switch: print(f"Username: {username}, ID: {user_id_value}")

    if switch:
        print(f"Replay host (Creator) is: {replayHost}")
        print(f"Reply host ID is: {validateHostID(replayHost, replayHost)}\n")

    # print("---- MAP TEST ----")
    # getMap()

# Helper functions
def validateHostID(Host, user):  # Host = replayHost string, user = input username or id
    if Host in idPool:
        host_id = idPool[Host]
        if str(host_id) == str(user) or Host == user:
            return host_id
    return None

def getMap():  # unused helper function
    with open('output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    map_data = data.get('eventBuffer', [])[0]['data']['map'].get('map', 'Unknown')
    mapColumns = 0
    mapRows = 0
    for entry in map_data:
        # loop through each array in map and get dimensions by X and Y
        if isinstance(entry, list):
            mapRows += 1
            mapColumns = max(mapColumns, len(entry))
    
    # pretty print the map and its dimensions
    # mapString = '\n'.join([' '.join(map(str, row)) for row in map_data])

    # print(f"Map:\n{mapString}")
    # print(f"Map rows: {mapRows}, Map columns: {mapColumns}")
    return mapRows, mapColumns

def getMinMax(v, randMin, randMax, oneNum):
    min = 0
    max = 0
    tankSpeed = getTankSpeed()

    if randMin is None or randMax is None:
        min = 0
        if v == 1 or v == 2:  # X, Y high byte
            max = 30
        elif v == 3 or v == 4:  # X, Y low byte
            max = 255
        elif v == 5 or v == 6:  # Tank velocity's (vX, vY)
            if not once: print("Min and Max are only the values you can input.")
            once = True
            if tankSpeed == 0.5:
                min = 108
                max = 148
            elif tankSpeed == 0.75:
                min = 98
                max = 158
            elif tankSpeed == 1:
                min = 88
                max = 168
            elif tankSpeed == 1.5:
                min = 68
                max = 188
            elif tankSpeed == 2:
                min = 48
                max = 208
        elif v == 7: # Tank arm angle
            min = 50
            max = 230
        else:  # default Max value
            max = 255

        if str(oneNum).lower() == "min":
            return min
        elif str(oneNum).lower() == "max":
            return max

        return min, max

    if v == 1:
        min = randMin if 0 < randMin < randMax else random.randint(0, randMin)
        max = randMax if randMin < randMax < 30 else random.randint(randMax, 30)
    elif v == 2:
        min = randMin if 0 < randMin < randMax else random.randint(0, randMin)
        max = randMax if randMin < randMax < 30 else random.randint(randMax, 30)
    elif v == 3:
        min = randMin if 0 < randMin < randMax else random.randint(0, randMin)
        max = randMax if randMin < randMax < 255 else random.randint(randMax, 255)
    elif v == 4:
        min = randMin if 0 < randMin < randMax else random.randint(0, randMin)
        max = randMax if randMin < randMax < 255 else random.randint(randMax, 255)
    elif v == 5:
        min = randMin
        max = randMax
    elif v == 6:
        min = randMin
        max = randMax
    elif v == 7:
        min = 50 if randMin < 50 else randMin
        max = 230 if randMax < 231 else randMax
    else:
        min = 0 if randMin < 0 else randMin
        max = 255 if randMax < 256 else randMax
    
    if str(oneNum).lower() == "min":
        return min
    elif str(oneNum).lower() == "max":
        return max

    return min, max

def map_to_angle(v):
    v = int(v)
    if v < 50:
        v = 50
    elif v > 230:
        v = 230
    return (v * 2) - 280
    
def getTankSpeed():
    with open('output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    speed = data.get('eventBuffer', [])[0]['data']['config'].get('match_general_tankSpeed', 1)
    return speed

# main executions
def backupMain():
    while True:
        choice = input("Choose an option:\n1. Encode\n2. Decode\n3. Randomize\n4. Acquire Usernames (Optional)\n5. Exit\nEnter choice (1-5): ").strip()
        if choice == '1':
            filename = input("Enter the output .btnks file name (without extension): ").strip()
            encoder(filename)
        elif choice == '2':
            filename = input("Enter the .btnks file name (with extension): ").strip()
            prettyPrint = input("Do you want to pretty-print the JSON output? (yes/no): ").strip().lower()
            if prettyPrint not in ['yes', 'no']:
                print("Invalid input for pretty print. Defaulting to 'no'.")
                prettyPrint = "no"
            decoder(filename, prettyPrint)
        elif choice == '3':
            v1 = input("Enter function option (data, bullets): ").strip().lower()
            if v1 == "data":
                col_input = input("Enter specific column to randomize (1-7) or press Enter to randomize all: ").strip()
                v4 = int(col_input) if col_input else 0
                acqiureUsernames(True)
                v5 = input("Enter the player name or ID to modify: ").strip().lower()
                string1 = f" (Min: {getMinMax(v4, None, None, 'min')})"
                string2 = f" (Max: {getMinMax(v4, None, None, 'max')})"
            v2 = input(f"Enter minimum random value{string1}: ").strip()
            v3 = input(f"Enter maximum random value{string2}: ").strip()
            randomizer(v1, v2, v3, v4, v5)
        elif choice == '4':
            acqiureUsernames(True)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    if var4 == "encode":
        if var6.endswith('.btnks'):
            var6 = var6[:-6]
        encoder(var6)
    elif var4 == "decode":
        if not var6.endswith('.btnks'):
            var6 = var6 + '.btnks'
        decoder(var6, var5 if var5 in ['yes', 'no'] else 'no')
    elif var4 == "randomize":
        randomizer(var1, var2, var3, var7, var8)
    elif var4 == "acqiureUsernames":
        acqiureUsernames(True)
    elif var4 == "getMinMax":
        with open('minmax.txt', 'w', encoding='utf-8') as f:
            f.write(f"Min:{getMinMax(int(var7), None, None, 'min')}\nMax:{getMinMax(int(var7), None, None, 'max')}")
    elif len(sys.argv) <= 1:
        backupMain()
    else:
        print("Invalid arguments for var4. Use 'encode', 'decode', 'randomize' or 'acqiureUsernames'.")
    if len(sys.argv) <= 1:

        input("Press Enter to exit/continue...")

