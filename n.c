#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/auxv.h>

int mkcmd(char *cmd, char *n_home, char *name) {
  sprintf(cmd, "%1$s/%2$s/%2$s", n_home, name);
  return access(cmd, X_OK) == 0;
}

int main(int argc, char **argv) {
  char *exe, cur, n_home[PATH_MAX], cmd[PATH_MAX], env[PATH_MAX];
  int i;
  DIR *dp;
  struct dirent *ep;

  // Get n executable path
  exe = (char *)getauxval(AT_EXECFN);

  if(exe == 0) {
    fprintf(stderr, "couldn't find n executable path");
    return 1;
  }

  // Get n home dir
  sprintf(n_home, "%s", exe);

  for(i = strlen(n_home) - 1; i >= 0; i--) {
    cur = n_home[i];
    n_home[i] = '\0';
    if(cur == '/') break;
  }

  if(argc < 2) {
    // Iterate over directories to print subcommands
    dp = opendir(n_home);

    if(dp == NULL) {
      fprintf(stderr, "couldn't open n home");
      return 2;
    }

    printf("usage: %s <subcommand> [<args>]\n\nSubcommands:\n\n", argv[0]);

    while((ep = readdir(dp))) {
      if(!strcmp(ep->d_name, ".") || !strcmp(ep->d_name, "..")) {
        continue;
      }

      if(mkcmd(cmd, n_home, ep->d_name)) {
        printf("%s\n", ep->d_name);
      }
    }

    closedir(dp);
  } else {

    // Check if subcommand is valid
    if(!mkcmd(cmd, n_home, argv[1])) {
      fprintf(stderr, "n subcommand not found\n");
      return 2;
    }

    // Create custom environment variables
    sprintf(env, "N_HOME=%s", n_home);
    putenv(strdup(env));
    sprintf(env, "N_CMD_HOME=%s/%s", n_home, argv[1]);
    putenv(strdup(env));

    // Execute the subcommand
    execvp(cmd, &argv[1]);
  }

  return 0;
}
