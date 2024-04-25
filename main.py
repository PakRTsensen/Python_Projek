import itertools
import math
import time
import sys
import threading
import os
import platform  # Modul platform untuk informasi sistem operasi
import psutil    # Modul psutil untuk memantau penggunaan sumber daya
import language_control as lang # Modul untuk kontrol bahasa


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
print("Welcome to the Math Possibility Finder")
print("Created by Hasanur Rahevy")

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
            user_input = input("Enter the target number or type 'help' to show more options: ")

            if user_input.lower() == 'exit':
                print("Thank you for using the Math Possibility Finder!")
                sys.exit()
            
            # Check for 'mode info' command to display current mode
            if user_input.lower() in ['mode info', 'current mode', 'show mode']:
                print(f"You are currently in {mode} mode.")
                continue

            # Menampilkan bantuan
            if user_input.lower() in ['help', 'tolong', 'menu', 'bantuan', 'info']:
                print("Available commands:")
                print("- 'exit': Quit the program")
                print("- 'info system': Print information about your system")
                print("- 'mode info': Print current mode")
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
                print_error("Invalid input. Please enter a number or 'exit' to quit.")

        while True:
            max_digits_str = input("Enter the maximum number of digits: ")

            if not max_digits_str.strip():
                print_error("Maximum number of digits cannot be empty.")
            else:
                try:
                    max_digits = int(max_digits_str)

                    if max_digits <= 1:
                        print_error("Sorry, maximum number of digits must be greater than 1")
                    elif max_digits >= 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:
                        print_error("Maximum number of digits cannot be more than 100 digits of number.")
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

                    if len(timeout_str) > 100:
                        print_error("Maximum search time cannot have more than 100 digits.")
                    else:
                        break
                except ValueError:
                    print_error("Invalid input. Please enter a valid number.")

        calculation_in_progress = False  # Menandai bahwa perhitungan sedang berlangsung
        print(f"Calculating for target number: {target}...")

        valid_operations = []
        invalid_operations = []
        invalid_count = 0
        timeout_reached = False  # Flag untuk menandai apakah waktu telah habis

        start_time = time.time()

        # Membuat thread untuk menghentikan perhitungan jika waktu habis
        timeout_thread = threading.Timer(timeout, stop_calculation)
        timeout_thread.start()

        while not timeout_reached:
            for num_digits in range(2, max_digits + 1):
                for nums in itertools.combinations_with_replacement(range(2, 10), num_digits):
                    for ops in itertools.product("+-*/", repeat=num_digits - 1):
                        expression = f"{nums[0]}"
                        for i in range(num_digits - 1):
                            expression += ops[i] + f"{nums[i + 1]}"

                        if expression in known_results:
                            result = known_results[expression]
                            print_know(f"Already known: {expression} = {result}")
                        else:
                            try:
                                result = eval(expression)
                                if math.isclose(result, target, rel_tol=1e-1000):
                                    valid_operations.append(expression)
                                    print_valid(f"Valid: {expression} = {result}")
                                else:
                                    invalid_operations.append(expression)
                                    invalid_count += 1
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
            new_file_name = f"valid_calculations_{target}.txt"
            print_file(f"File 'valid_calculations_{target}.txt' in '{file_path}' directory is already exists. Renaming it to '{new_file_name}'.")
            os.rename(file_path, new_file_name)

        # Simpan hasil perhitungan dalam file
        with open(file_path, "w") as file:
            for operation in valid_operations:
                file.write(f"{operation}\n")

        print_file_valid(f"Valid calculations have been saved to '{file_path}'")

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
        print("\nResource Usage:")
        print_resource_usage(cpu_usage, ram_usage)

    except KeyboardInterrupt:
        if calculation_in_progress:
            print("\nWarning: Incomplete process. Calculation interrupted by user.")
        else:
            print("\nThank you for using the Math Possibility Finder!")
            sys.exit()
