import serial
import time
import logging
import csv
import datetime as dt
import argparse


def get_next_val(ser):
    while True:
        line = ser.readline().decode("utf-8")
        split = ["", ""]
        if len(line) > 10:
            split = line.split(":")
            if split[0] in ["Result after taring", "Liquid sense"]:
                print(f"{split[1]}")
                return float(split[1])


def write_csv(list_of_data, run="cd_04"):
    today = dt.datetime.now().strftime('%Y;%m;%d;%I;%M;%S') + run
    with open(f'dro-{today}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list_of_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="DROTest",
                                     description="DRO Data collection program.")
    
    parser.add_argument('-r', '--run', action="store", default="test")

    args = parser.parse_args()

    start_time = time.time()

    list_of_data = []

    try:
        with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
            while True:
                list_of_data.append((get_next_val(ser),time.time() - start_time, time.time()))
    except KeyboardInterrupt as error:
        logging.error(f"Caught keyboard interupt. {error}")
    
    finally:
        print(list_of_data)
        write_csv(list_of_data, args.run)