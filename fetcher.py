import sys
import time
import signal

# SIGINT handler
def sigterm_handler(signum, frame):
	cur_time = time.asctime(time.localtime(time.time()))
	print >> sys.stderr, "Interrupted at %s" % cur_time
	sys.exit(0)
def main():
	cur_time = time.asctime(time.localtime(time.time()))
	print >> sys.stderr, "Program was run at %s" % cur_time
	sys.exit(0)

# Bind our handler to SIGINT
signal.signal(signal.SIGTERM, sigterm_handler)

# Run the main program
main()
