import itertools # Modul itertools untuk membuat iterator untuk perulangan
import math # Modul math untuk operasi matematika
import time # Modul time untuk mengakses fungsi-fungsi yang berkaitan dengan waktu
import sys # Modul sys untuk mengakses fungsi-fungsi yang berkaitan dengan interpreter Python
import threading # Modul threading untuk membuat thread
import difflib # Modul difflib untuk saran perintah
import os # Modul os untuk mengakses fungsi-fungsi yang bergantung pada sistem operasi
import platform  # Modul platform untuk informasi sistem operasi
import psutil    # Modul psutil untuk memantau penggunaan sumber daya
from concurrent.futures import ThreadPoolExecutor # Modul untuk membuat thread


# Kode bagian ini digunakan untuk memberitahu pengguna apa yang sedang program hitung
show_logs = False
show_Resource = False
# Kode bagian ini digunakan untuk memastika program tau perintah apa aja yang tersedia
known_commands = ['exit', 'mode info', 'current mode', 'show mode', 'help', 'tolong', 'menu', 'bantuan', 'info', 'show log', 'show logs', 'show_verbose', 'show verbose', 'verbose', 'verbose info', 'calcu', 'calculators', 'kalkulator', 'kalku']

# Sementara dinonaktifkan dikarenakan fungsi bagian ini tidak berjalan sesuai rencana
#num_threads = os.cpu_count()  # Default to use all available cores

# Fungsi untuk mencetak teks dengan warna hijau
def print_valid(text):
    print("\033[92m" + text + "\033[0m")

# Fungsi untuk mencetak teks dengan warna oranye
def print_know(text):
    print("\033[38;5;202m" + text + "\033[0m")

# Fungsi untuk mencetak teks dengan warna kuning pada file valid_calculations.txt jika sudah ada
def print_file(text):
    print("\033[93m" + text + "\033[0m")

# Fungsi untuk mencetak teks dengan warna hijau pada file valid_calculations[target].txt jika file telah di save
def print_file_valid(text):
    print("\033[92m" + text + "\033[0m")

# Fungsi untuk mencetak teks dengan warna merah
def print_error(text):
    print("\033[91m" + text + "\033[0m")

# Fungsi untuk mencetak teks warning atau peringatan dengan warna merah
def print_warning(text):
    print("\033[91m" + text + "\033[0m")

# Fungsi untuk memberitahu user jika perintah yang diinputkan tidak dikenali
# Fitur ini saat ini masih belum tersedia dikarenakan masih Error atau belum tersedia untuk digunakan
#def suggest_command(user_input, commands):
    #suggestions = difflib.get_close_matches(user_input, commands, n=1, cutoff=0.7)  # Adjust cutoff for accuracy
    #if suggestions:
        #return f"Did you mean: '{suggestions[0]}'?"
    #return "Command not recognized. Type 'help' for available commands."

# Fungsi untuk mencetak informasi perangkat dan OS
# Anda dapat menonaktfkan seluruh fitur atau sebagain, jika anda ingin mengnonaktifkan seluruh fitur pastikan anda nonakfikan line nomer 103 hingga 106
def print_system_info():
    system_info = platform.uname()
    print(f"System: {system_info.system}")
    print(f"Node Name: {system_info.node}")
    print(f"Release: {system_info.release}")
    print(f"Version: {system_info.version}")
    print(f"Machine: {system_info.machine}")
    print(f"Processor: {system_info.processor}")

# Fungsi untuk mencetak informasi penggunaan sumber daya
def print_resource_usage(cpu_usage, ram_usage):
    print(f"CPU Usage: {cpu_usage}%")
    print(f"RAM Usage: {ram_usage}%")

# Teks pembuka dalam bahasa Inggris
print("Welcome to the Math Possibility Finder v2.7.7")
print("Created by Hasanur Rahevy")
print_warning(f"if you can't exit using CTRL+C while after interrupted the process, try process again with any number or \t type 'exit'")

mode = "search"  # Mode default adalah mode mencari
known_results = {}  # Dictionary untuk menyimpan hasil perhitungan yang sudah diketahui
calculation_in_progress =  False  # Flag untuk menandai apakah perhitungan sedang berlangsung

# Fungsi untuk menghentikan perhitungan jika waktu habis
def stop_calculation():
    global timeout_reached
    timeout_reached = True

while True:
    try:
        while True:
            user_input = input("Enter the target number or type 'help' to show more options: ").lower()

            if user_input.lower() in  ['exit', 'keluar', 'quit', 'out']:
                print("Thank you for using the Math Possibility Finder!")
                sys.exit()
            
            # Check for 'mode info' command to display current mode
            if user_input.lower() in ['mode info', 'current mode', 'show mode', 'mode?']:
                print(f"You are currently in {mode} mode.")
                continue

            if user_input.lower() == 'source':
                print(f"you can get the source code at the github @PaktRTsensen. (https://github.com/PakRTsensen/Python_Projek)")
                continue

            if user_input.lower() in  ['cmd', 'terminal', 'bash']:
                print_warning(f"only works on linux")
                os.system("bash")
                continue

            if user_input.lower() in  ['cmd root', 'terminal root', 'bash', 'sudo su']:
                print_warning(f"only works on linux")
                os.system("sudo su")
                os.system("bash")
                continue


            # Menampilkan bantuan
            if user_input.lower() in ['help', 'tolong', 'menu', 'bantuan', 'info']:
                print("Available commands:")
                print("- 'exit': Quit the program")
                print("- 'info system': Print information about your system")
                print("- 'mode info': Print current mode")
                print("- 'show_log': Show log output")
                print("- 'bash': to enter the terminal mode (linux only)")
                print("- 'sudo su': to enter the terminal mode (linux only)")
                print("- 'Resource info': Print system resource used")
                print("- 'resource status': to to check that system resource used")
                print("- 'source': to get this source code")
                print("- 'calcu': Enter calculator mode")
                print("- 'help': Display this help message")
                if mode == "search":
                    print("- 'back', 'kembali', 'return': Return to search mode (if in calculator mode)")
                if mode == "calculator":
                    print("- 'sin(x)': Sine of x (in radians) [sin(π/2) = sin(*) = 1]")
                    print("- 'cos(x)': Cosine of x (in radians) [cos(π) = cos(*) = -1]")
                    print("- 'tan(x)': Tangent of x (in radians) [tan(π/4) = tan(*) = 1]")
                    print("- 'asin(x)': Arcsine (inverse sine) of x [asin(1) = asin(*) = π/2]")
                    print("- 'acos(x)': Arccosine (inverse cosine) of x [acos(-1) = acos(*) = π]")
                    print("- 'atan(x)': Arctangent (inverse tangent) of x [atan(1) = atan(*) = π/4]")
                    print("- 'exp(x)': Exponential function e^x [exp(1) = exp(*) = e]")
                    print("- 'log(x, base)': Logarithm of x with specified base (e.g., 'log(100, 10)' for log base 10) [log(*) = log(e, *)]")
                    print("- 'sqrt(x)': Square root of x [sqrt(*)]")
                    print("- 'pi' or '*': Mathematical constant π (pi) [π]")
                    print("- 'e': Mathematical constant e [e]")
                    print("- 'fact(x)': Factorial of x (e.g., 'fact(5)' for 5!) [fact(*)]")
                continue

            # Kode bagian ini digunakan untuk menghandle perintah "show log" atau yang mirip untuk mengubah apakah log ditampilkan atau tida
            if user_input.lower() in ['show log', 'show logs', 'show_verbose', 'show verbose','verbose','verbose inf']:
                show_logs = not show_logs
                print("Log output is now enabled." if show_logs else "Log output is now disabled.")
                continue

            if user_input.lower() in ['show resource', 'show_resource','resource info', 'resource info']:
                show_Resource = not show_Resource
                print("Resource Used will show." if show_Resource else "Resource used is now disabled.")
                continue

                # Kode bagian ini digunakan untuk menampilkan apakah tampilan penggunaa sumber daya komputer akan ditampilkan atau tidak
            if user_input.lower() in ['resource status', 'resource?', 'resource verbose status']:
                print(f"resource status are showed." if show_Resource else "resource status off.")
                continue

            # Fitur ini untuk menghandle peritah dari user yang typo atau ditidak valid
            # Tetapi Fitur ini saat ini masih belum tersedia dikarenakan masih Error
            #if user_input in known_commands:
                # Process the command
                #pass
            #else:
            #suggestion = suggest_command(user_input, known_commands)
            #print(suggestion)

            # Mode kalkulator
            if user_input.lower() in ['calcu', 'calculators', 'kalkulator', 'kalku']:
                mode = "calculator"
                print_warning("Calculator mode (Warning: This mode is under development and may have limited functionality or bugs). Enter 'back' to return to search mode.")
                continue
            # Fitur Informasi System untuk Print informasi tentang system anda saat ini
            if user_input.lower() in ['informasi system', 'info system', 'tentang system', 'tentang system', 'informasi_system', 'system', 'system_info', 'info_system']:
                print("\nSystem Information:")
                print_system_info()
                continue

            # Kembali ke mode mencari
            if user_input.lower() in ['back', 'kembali', 'return', 'home']:
                if mode == "search":
                    print_error("You are already in search mode.")
                else:
                    mode = "search"
                    print("Returning to search mode.")
                continue

            if mode == "calculator":
                try:
                    result = eval(user_input)
                    print(f"Result: {user_input} = {result}")
                    continue  # Lanjut ke input berikutnya
                except Exception as e:
                    print_error(f"Error: {e}")

            try:
                target = float(user_input)

                if len(user_input.replace(".", "").replace("-", "")) > 100:
                    print_error("Input number cannot have more than 100 digits.")
                elif target == 0:
                    print_error("Sorry, cannot calculate for 0")
                else:
                    break
            except ValueError:
                print_error("Invalid input or command not found. Please enter a number or 'help' to get help.")
                
            if user_input.lower() == 'default limit':
                print_file(f"- Default input number cannot more than 100 digits.\n- Default input number cannot be zero (0)\n- Default Maximum digit to search must more than 1 digits or 16 seconds, and cannot more 100 digits\n- Default Maximum Number have to be must be greater than 1 and cannot more than 100")

            #if user_input.lower() == 'reload':
                #os.system("killall -9 python3 && python3 main.py")

        while True:
            max_digits_str = input("Enter the maximum number of digits: ")

            if not max_digits_str.strip():
                print_error("Maximum number of digits cannot be empty.")
            else:
                try:
                    max_digits = int(max_digits_str)

                    if max_digits <= 1:
                        print_error("Sorry, maximum number of digits must be greater than 1")
                    elif max_digits > 100:
                        print_error("Maximum number of digits cannot be more than 100 digits or type 'set limit [limit]'.")
                    else:
                        break
                except ValueError:
                    print_error("Invalid input. Please enter a valid number.")

        while True:
            timeout_str = input("Enter the maximum search time (seconds): ")

            if not timeout_str.strip():
                print_error("Maximum search time cannot be empty.")
            else:
                try:
                    timeout = int(timeout_str)

                    # Kode bagian ini digunakan untuk membatasi inputan user dan memastikan agar tidak overflow
                    if len(timeout_str) > 7:
                        print_error("Maximum search time cannot have more than 7 digits.")
                    if len(timeout_str) <= 1:
                        print_error("Maximum search time must be greater than 1 seconds")
                    if len(timeout_str) <= 16:
                        print_error("Maximum search time must be greater than 16 seconds")
                    else:
                        break
                except ValueError:
                    print_error("Invalid input. Please enter a valid number.")

        calculation_in_progress = True  # Menandai bahwa perhitungan sedang berlangsung
        # Kode bagian ini digunakan untuk memberitahu user bahwa perhitungan sedang berlangsung
        print(f"Calculating for target number: {target}...")

        valid_operations = []
        invalid_operations = []
        invalid_count = 0
        timeout_reached = False  # Flag untuk menandai apakah waktu telah habis

        start_time = time.time()

        # Membuat thread untuk menghentikan perhitungan jika waktu habis
        timeout_thread = threading.Timer(timeout, stop_calculation)
        timeout_thread.start()

        # Kode bagian ini digunakan untuk menghitung total kombinasi yang akan di proses
        total_combinations = sum(math.comb(9, n) * 4**(n-1) for n in range(2, max_digits + 1))
        combinations_processed = 0

        while not timeout_reached:
            for num_digits in range(2, max_digits + 1):
                for nums in itertools.combinations_with_replacement(range(2, 10), num_digits):
                    for ops in itertools.product("+-*/", repeat=num_digits - 1):
                        expression = f"{nums[0]}"
                        for i in range(num_digits - 1):
                            expression += ops[i] + f"{nums[i + 1]}"

                        # Kode bagian ini digunakan untuk menampilkan progress perhitungan
                        elapsed_time = time.time() - start_time
                        combinations_processed += 1
                        progress_combinations = (combinations_processed / total_combinations) * 100
                        progress_time = (elapsed_time / timeout) * 100
                        progress = min(progress_combinations, progress_time)
                        if show_logs == False:
                            print(f"\rProgress: {progress:.2f}%", end="")

                        if expression in known_results:
                            result = known_results[expression]
                            # Kode bagian ini digunakan untuk menampilkan hasil perhitungan yang sudah diketahui
                            if show_logs:
                                print_know(f"Already known: {expression} = {result}")
                        else:
                            try:
                                result = eval(expression)
                                if math.isclose(result, target, rel_tol=1e-1000):
                                    valid_operations.append(expression)
                                    # Kode bagian ini digunakan untuk menampilkan hasil perhitungan yang valid
                                    if show_logs:
                                        print_valid(f"Valid: {expression} = {result}")
                                else:
                                    invalid_operations.append(expression)
                                    invalid_count += 1
                                    # Kode bagian ini digunakan untuk menampilkan hasil perhitungan yang tidak valid
                                    if show_logs:
                                        print_error(f"Not Valid: {expression} = {result}")
                                known_results[expression] = result  # Menyimpan hasil perhitungan
                            except (ZeroDivisionError, ValueError, OverflowError):
                                pass

                        elapsed_time = time.time() - start_time
                        if elapsed_time >= timeout:
                            break
                    if elapsed_time >= timeout:
                        break
                if elapsed_time >= timeout:
                    break

        # Mematikan thread timeout jika perhitungan selesai
        timeout_thread.cancel()

        # Dapatkan direktori kerja saat ini
        current_directory = os.getcwd()

        # Buat path lengkap untuk file hasil perhitungan
        file_path = os.path.join(current_directory, f"valid_calculations_{target}.txt")

        # Cek apakah file sudah ada
        if os.path.isfile(file_path):
            # Kode bagian ini digunakan untuk memberitahu user bahwa file sudah ada dan akan di rename
            new_file_name = f"valid_calculations_{target}.txt"
            # Kode bagian ini digunakan untuk memberitahu user bahwa file sudah ada dan akan di rename
            print_file(f"\nFile 'valid_calculations_{target}.txt' in '{file_path}' directory is already exists. Renaming it to '{new_file_name}'.")
            os.rename(file_path, new_file_name)

        # Simpan hasil perhitungan dalam file
        with open(file_path, "w") as file:
            for operation in valid_operations:
                file.write(f"{operation}\n")

        # Kode bagian ini digunakan untuk memberitahu user bahwa perhitungan telah selesai
        print_file_valid(f"\nValid calculations have been saved to '{file_path}'")

        calculation_in_progress = False  # Menandai bahwa perhitungan telah selesai

        # Tampilkan informasi perangkat dan OS
        # Untuk sementara bagian ini dinonaktifkan karena saya merasa tidak terlalu memerlukannya
        #print("\nSystem Information:")
        #print_system_info()

        # Menghitung penggunaan sumber daya program
        process = psutil.Process(os.getpid())
        cpu_usage = process.cpu_percent()
        ram_usage = process.memory_percent()

        # Mencetak informasi penggunaan sumber daya
        # Bagian ini memiliki akurasi yang sangat rendah dalam memantau sumber daya komputer
        # Anda bisa menonaktifkannya jika ada mau
        if show_logs == True or show_Resource == True:
            print("\nResource Usage:")
            print_resource_usage(cpu_usage, ram_usage)

    except KeyboardInterrupt:
        if calculation_in_progress:
            print_error("\nWarning: Incomplete process. Calculation interrupted by user.")
        else:
            print("\nThank you for using the Math Possibility Finder!")
            sys.exit()


