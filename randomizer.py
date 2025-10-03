import json, random, sys, zlib
# Usage: run the Da-Funny.bat file and follow the prompts

print("Funny BT replay modifier/randomizer by UnknownUser\n\n")

if not len(sys.argv) == 0:
    var1 = sys.argv[1] # options for randomization (String | required for randomizer)*
    var2 = sys.argv[2] # min random (int | required for randomizer)*
    var3 = sys.argv[3] # max random (int | required for randomizer)*
    var4 = sys.argv[4] # encode/decode/randomize (String | Required)*
    var5 = sys.argv[5] # pretty print (yes/no | Optional)
    var6 = sys.argv[6] # filename (String | Required for encoder/decoder)*
    var7 = sys.argv[7] # coloum for data randomization (int | Optional)
    # * = These vars are mostly required but can be optional since there is a system in-place to user-input them if not provided.

def encoder(x): # x = filename
    try:
        x
    except NameError:
        x = input("IMPORTANT: JSON must be in the same directory as this encoder.\n\nEnter the output .btnks file name (without extension): ")

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

def decoder(x, x2): # x = filename, x2 = pretty print (yes/no)
    try:
        x
        # x2
    except NameError:
        x = input("IMPORTANT: The .btnks file must be in the same directory as this decoder.\n\nEnter the .btnks file name (with extension): ")
        # x2 = input("Do you want to pretty-print the JSON output? (yes/no): ").strip().lower()
        
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

def randomizer(var1, var2, var3, var7): # var1 = function option, var2 = min random, var3 = max random, var7 = coloum for data randomization
    try:
        var1
        var2 = int(var2)
        var3 = int(var3)
        var7 = int(var7)
    except (NameError, ValueError):
        var1 = input("Enter function option (data, aim, bullets): ").strip().lower()
        var2 = int(input("Enter minimum random value (negative integer): "))
        var3 = int(input("Enter maximum random value (positive integer): "))
        var7 = int(input("Enter column to randomize (1-13) or leave blank for all except user ID: ").strip())
        

    with open('output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


    if var1 == "data":
        # Add/subtract random value to each data value except user ID
        for entry in data.get('binaryBuffer', []):
            if var7 is not None:
                try:
                    col = int(var7-1)  # Convert to 0-based index
                    if 0 <= col < len(entry['data']):
                        print(str(entry['data'][col]))
                        entry['data'][col] += random.randint(var2, var3)
                        print("-> " + str(entry['data'][col]))
                    else:
                        print(f"Column index {col} out of range for entry['data']")
                except (ValueError, TypeError):
                    print(f"Invalid column index: {var7}")
            else:
                for i in range(len(entry['data'])):
                    print(str(entry['data'][i]))
                    if i != 3:
                        entry['data'][i] += random.randint(var2, var3)
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

    elif var1 == "aim":
        # Add/subtract random value to each aim angle
        for entry in data.get('aimBuffer', []):
            print(str(entry['angle']))
            entry['angle'] = random.randint(var2, var3)
            print("-> " + str(entry['angle']))
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)

    elif var1 == "bullets":
        # Placeholder: bullets not yet identified
        print("Bullets randomization not implemented.")

    else:
        print("Invalid function option. Please use 'data', 'aim', or 'bullets'.")

    print("Randomization complete. Check output.json for results.")

def backupMain():
    while True:
        choice = input("Choose an option:\n1. Encode\n2. Decode\n3. Randomize\n4. Exit\nEnter choice (1-4): ").strip()
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
            v1 = input("Enter function option (data, aim, bullets): ").strip().lower()
            v2 = input("Enter minimum random value (negative integer): ").strip()
            v3 = input("Enter maximum random value (positive integer): ").strip()
            randomizer(v1, v2, v3)
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
    

# Main execution
if __name__ == "__main__":
    if var4 == "encode":
        if var6.endswith('.btnks'):
            var6 = var6[:-6]
        encoder(var6)
    elif var4 == "decode":
        if not var6.endswith('.btnks'):
            var6 = var6 + '.btnks'
        decoder(var6, None)
    elif var4 == "randomize":
        randomizer(var1, var2, var3, var7)
    elif len(sys.argv) == 0:
        backupMain()
    else:
        print("Invalid arguments for var4. Use 'encode', 'decode', or 'randomize'.")
    
    input("Press Enter to exit/continue...")