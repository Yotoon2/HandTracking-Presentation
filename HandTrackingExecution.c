#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#define GH_USER   "Yotoon2"
#define REPO_NAME "HandTracking-Presentation"
#define VENV_NAME "venv_cmi"
#define LIBS "mediapipe opencv-python numpy pynput pyserial bleak aioconsole"

// On force le chemin du Python systeme pour ignorer les versions casseres
#ifdef __APPLE__
    #define PYTHON_EXE "python3"
#else
    #define PYTHON_EXE "/usr/bin/python3"
#endif

int directory_exists(const char *path) {
    struct stat info;
    if (stat(path, &info) != 0) return 0;
    return (info.st_mode & S_IFDIR) != 0;
}

int main() {
    //Vérification et clonage du projet/ git
    if (!directory_exists(REPO_NAME)) {
        printf("[*] Clonage du projet...\n");
        char clone_cmd[512];
        snprintf(clone_cmd, sizeof(clone_cmd), "git clone https://github.com/%s/%s.git", GH_USER, REPO_NAME);
        system(clone_cmd);
		//Clonage du venv
		if (directory_exists(VENV_NAME)) {
        printf("[*] venv déjà installé\n");}
		else {
			printf("[*] Creation du venv avec %s...\n", PYTHON_EXE);
    		char venv_cmd[256];
    		snprintf(venv_cmd, sizeof(venv_cmd), "%s -m venv %s", PYTHON_EXE, VENV_NAME);
    		if (system(venv_cmd) != 0) {
        		printf("[!] Erreur fatale : Impossible de creer le venv. Installez python3-venv.\n");
        		return 1;}
		}
		// Installation des librairies
		printf("[*] Installation des bibliotheques...\n");
    	char install_cmd[512];
    	snprintf(install_cmd, sizeof(install_cmd), "./%s/bin/python3 -m pip install %s", VENV_NAME, LIBS);
    	system(install_cmd);
		}

    //Lancement
    printf("[*] Execution...\n");
    char run_cmd[512];
    snprintf(run_cmd, sizeof(run_cmd), "cd %s/Code && ../%s/bin/python3 main.py", REPO_NAME, VENV_NAME);
    system(run_cmd);

    return 0;
}
