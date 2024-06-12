# All quotes taken from Lolly Daskal's list of 100 motivating quotes
# https://www.inc.com/lolly-daskal/100-motivational-quotes-for-inspiring-you-to-succeed.html

# importing required modules
import argparse
import random
import threading
import time


# This is the main function that will be called when the script is run
# we will be passing our work and rest durations along with our desired number of
# cycles
def main(work_duration, break_duration, cycles):
  # This is the message thread that will read a random message for Lolly's list and
  # print it
  def print_motivating_messages():
    with open('message.txt', 'r') as messages:
      all_messages = messages.readlines()
      while running:
        interval = random.randint(1, 10)
        time.sleep(interval)
        # Here we check to see if it is still running to avoid printing after the 
        # timer stops
        if running:  
          print(random.choice(all_messages))

  # This is the main timer function, it will be run for either a rest or work period
  def start_timer(duration, label):
    # running is defined as global to allow the motivating message program to access it
    global running
    running = True
    end_time = time.time() + duration
    print(
        f"""
        Commencing {work} timer! Good luck and have fun, you have {duration / 60} 
        minutes to {label}!
        """
    )

    # Create the "Motivating message" thread and start it
    message_thread = threading.Thread(target=print_motivating_messages)
    message_thread.start()

    # wait one second and check to see if the timer has ended
    while time.time() < end_time:
      time.sleep(1)
      """
      Once the timer has ended, set running to false which terminates the         
      message
      """
    running = False
    message_thread.join()
    print(f"{label.capitalize()} time is over!")
    
  # This is the actual logic that will alternate between work and rest periods
  count = 0
  while count <= cycles:
    start_timer(work_duration * 60, "work")
    start_timer(break_duration * 60, "break")
    count += 1


# This function will return the arguments passed to the script
def build_parser():
  # The actual parser object is defined here
  parser = argparse.ArgumentParser(description="""
      A tool for running pomodor timers in the 
      command line and generatingmotivational messages.
      """)
  # here we will add an argument that aceppts 3 int values
  parser.add_argument(
      'timer',
      type=int,
      nargs=3,
      metavar=('work', 'break', 'cycles'),
      help="The duration of the work and break timers in minutes.")

  # here we return the three values given by the timer argument
  return parser.parse_args().timer


# Try except statements placed to deal with edge cases
if __name__ == "__main__":
  try:
    # define our timer arguments as a tuple
    work, rest, cycles = build_parser()
    if cycles < 1 or work < 1 or rest < 1:
      raise ValueError("Inputs must be positive numbers greater than 0.")
      # call the main function with the tuple defined above
    main(work, rest, cycles)
  except TypeError:
    print(
        "Invalid input. Please enter the work duration, rest duration, and number of cycles as integers. immediatelly following the command. eg. python main.py 25 5 3"
    )

