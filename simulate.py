import os
import subprocess
import time
import smtplib
import sys
import signal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from threading import Event
from itertools import cycle
# Configuration for directories
DATA_DIR = "/examples"
SAVE_ROOT = "/check"

# Email configuration
SMTP_SERVER = "smtp.qq.com"      #  SMTP server
SMTP_PORT = 587                   #  SMTP port
EMAIL_USER = "" # Replace with your  email
EMAIL_PASS = ""     # Replace with your SMTP auth code
EMAIL_RECEIVER = ""
ITERATIONS =3250 #​​Number of iterations
# GPU configuration
GPU_IDS = [ 0]            # List of available GPU IDs
MAX_PROCESSES_PER_GPU = 3        # Maximum concurrent processes per GPU
# Number of GPUs available
num_gpus = 2
gpu_cycle = cycle([0,2])  # This will cycle through 0, 1, 2, 3
# Global event to handle graceful termination
termination_event = Event()

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"[{datetime.now()}] Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_remaining_time_email(total_files, start_time, completed):
    remaining = total_files - completed
    elapsed = datetime.now() - start_time
    estimated_total = elapsed / completed * total_files if completed > 0 else 0
    remaining_time = estimated_total - elapsed
    remaining_hours = remaining_time.total_seconds() // 3600
    remaining_minutes = (remaining_time.total_seconds() % 3600) // 60
    remaining_seconds = remaining_time.total_seconds() % 60

    subject = "Processing Remaining Time Update"
    body = (f"Remaining files: {remaining}\n"
            f"Estimated remaining time: {int(remaining_hours)}h {int(remaining_minutes)}m {int(remaining_seconds)}s")

    send_email(subject, body)

def termination_handler(signum, frame):
    subject = "Processing Script Terminated"
    body = f"The processing script was terminated at {datetime.now()}."
    send_email(subject, body)
    termination_event.set()
    sys.exit(1)

def main():
    # Register termination signals
    signal.signal(signal.SIGINT, termination_handler)
    signal.signal(signal.SIGTERM, termination_handler)

    ply_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith('.ply')]
    total_files = len(ply_files)
    if total_files == 0:
        print("No .ply files found in the data directory.")
        return

    start_time = datetime.now()
    completed_files = 0
    processes = []
    last_email_time = start_time
    try:
        for ply_file in ply_files:
            if termination_event.is_set():
                break

            # Prepare file paths
            ply_path = os.path.join(DATA_DIR, ply_file)
            filename, _ = os.path.splitext(ply_file)
            obj_file = os.path.join(DATA_DIR, f"{filename}.obj")
            save_path = os.path.join(SAVE_ROOT, filename)

            gpu_id = next(gpu_cycle)

            cmd = [
                "python", "main.py",
                "--input-pc", ply_path,
                "--initial-mesh", obj_file,
                "--save-path", save_path,
                "--pools", "0.1", "0.0", "0.0", "0.0",
                "--iterations", "20001",
                "--gpu", str(gpu_id)  # Use specific GPU
            ]

            # If maximum concurrent processes reached, wait for one to finish
            while len(processes) >= num_gpus:
                for p in processes:
                    ret = p.poll()
                    if ret is not None:
                        processes.remove(p)
                        completed_files += 1
                        break
                else:
                    time.sleep(1)  # Wait a bit before checking again

            # Start the subprocess
            print(f"[{datetime.now()}] Starting process for {ply_file} on GPU {gpu_id}")
            proc = subprocess.Popen(cmd)
            processes.append(proc)

            # Check if it's time to send an email (every hour)
            current_time = datetime.now()
            if (current_time - last_email_time) >= timedelta(hours=1):
                send_remaining_time_email(total_files, start_time, completed_files)
                last_email_time = current_time

        while processes:
            for p in processes:
                ret = p.poll()
                if ret is not None:
                    processes.remove(p)
                    completed_files += 1
            time.sleep(1)

        subject = "Processing Completed"
        body = f"All {total_files} files have been processed successfully at {datetime.now()}."
        send_email(subject, body)

    except Exception as e:
        subject = "Processing Script Error"
        body = f"An error occurred: {e}\nTime: {datetime.now()}"
        send_email(subject, body)
        raise
    finally:
        for p in processes:
            p.terminate()
        if termination_event.is_set():
            subject = "Processing Script Terminated"
            body = f"The processing script was terminated at {datetime.now()}."
            send_email(subject, body)

if __name__ == "__main__":
    main()
