#include <stdio.h>
#include <unistd.h>
#include <signal.h>

static int
fork_bomb(void) {
	int pids = 0;
	
	// Reset signal handler for SIGTERM
	signal(SIGTERM, SIG_DFL);

	// Fork and create as many children as we can
	while (1) {
		pid_t pid;
		if ((pid = fork()) == -1)
			break;
		if (pid == 0)
			pause();
		pids++;
	}

	// Create our own process group so we can kill 'em all at once
	setpgid(0, 0);

	// Kill 'em all without killing ourselves
	signal(SIGTERM, SIG_IGN);
	killpg(getpgid(0), SIGTERM);

	return pids;
}

int main(void) {
	printf("%d\n", fork_bomb());
	return 0;
}
