import serial
import time
import logging
import csv
import datetime as dt

def get_next_val(ser):
    while True:
        line = ser.readline().decode("utf-8")
        split = ["", ""]
        if len(line) > 10:
            split = line.split(":")
            if split[0] == "Result after taring" or split[0] == "Liquid sense":
                print(f"{split[1]}")
                return float(split[1])

def write_csv(list_of_data, run="test"):
    today = dt.datetime.now().strftime('%Y;%m;%d;%I;%M;%S') + run
    with open(f'dro-{today}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list_of_data)

if __name__ == "__main__":
  
    start_time = time.time()

    list_of_data = []

    try:
        with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
            while True:
                list_of_data.append((get_next_val(ser),time.time() - start_time, time.time()))
    except KeyboardInterrupt as error:
        logging.error("Caught keyboard interupt")
    
    finally:
        print(list_of_data)
        write_csv(list_of_data)