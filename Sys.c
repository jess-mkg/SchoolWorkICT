#include "include.h"
void Sys()
{
	struct utsname uts;
	uname(&uts);
	printf("OS is %s\nVersion %s/n%s Hardware\n", uts.sysname, uts.machine, uts.version);
	printf("CPU type: ");
}
