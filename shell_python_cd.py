# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    shell_python_cd.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: goteixei <goteixei@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/05 15:55:55 by goteixei          #+#    #+#              #
#    Updated: 2025/04/05 17:50:59 by goteixei         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
import signal

def main_loop():
	# Tell the parent process (this script) to IGNORE SIGQUIT
	signal.signal(signal.SIGQUIT, signal.SIG_IGN)
		
	while True:
		try:
			i = input("$ ")
			params = i.split()

			# handle empty input
			if not params:
				continue

		 	# handle cd
			if params[0] == 'cd':

				# basic error handling
				if len(params) < 2:
					print("error: cd: bad arguments", file=sys.stderr)
				else:
					target_dir = params[1]
					try:
						os.chdir(target_dir)
					except FileNotFoundError:
						print(f"error: cd: cannot change directory to {target_dir}", file=sys.stderr)
					except NotADirectoryError:
						print(f"error: cd: cannot change directory to {target_dir}", file=sys.stderr)
					except PermissionError:
						print(f"error: cd: cannot change directory to {target_dir}", file=sys.stderr)
					except Exception as e:
						print(f"error: cd: cannot change directory to {target_dir}: {e}", file=sys.stderr)
				continue

			# forking and execution of external commands
			try:
				newpid = os.fork()
			except OSError as e:
				print(f"error: fatal (fork failed: {e})", file=sys.stderr)
				sys.exit(1)

			# child process
			if newpid == 0:
				# Reset SIGQUIT to default (Terminate + Core Dump)
				signal.signal(signal.SIGQUIT, signal.SIG_DFL)
				# Reset SIGINT to default (Terminate)
				signal.signal(signal.SIGINT, signal.SIG_DFL)

				print("Child Process: Executing")

				try:
					os.execvp(params[0], params)
				except FileNotFoundError:
					print(f"error: cannot execute {params[0]} (command not found)", file=sys.stderr)
				except PermissionError:
					print(f"error: cannot execute {params[0]} (permission denied)", file=sys.stderr)
				except Exception as e: # Catch other exec errors
					print(f"error: cannot execute {params[0]}: {e}", file=sys.stderr)
				#! IMPORTANT: Child MUST exit after exec error, use os._exit for safety - 1 for error status code
				#exit()
				os._exit(1)

			# parent process
			else:
				try:
					#os.wait()
					pid, status = os.waitpid(newpid, 0)
					print("Parent Process")
					print("Child Process ID: ", newpid)

					# CTRL+\
					if os.WIFSIGNALED(status):
						term_sig = os.WTERMSIG(status)
						# check if terminated by SIGQUIT (CTRL+\)
						if term_sig == signal.SIGQUIT:
							print("Quit")
						elif term_sig == signal.SIGINT:
							print()

				except OSError as e:
					print(f"error: fatal (waitpid failed for {newpid}: {e})", file=sys.stderr)		
					sys.exit(1)

		# handle Ctrl+C
		except KeyboardInterrupt:
			print()
			continue

		# handle CTRL+D
		except EOFError:
			print("\nExiting microshell.")
			break

		# handle other errors
		except Exception as e:
			print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
	print("Starting microshell...\n")
	main_loop()
	#print("\nMicroshell finished.")
