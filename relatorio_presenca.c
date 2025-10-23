#include <stdio.h>

int main(int argc, char *argv[]) {
    char turma_relatorio[30];
    sprintf(turma_relatorio, "relatorios_presenca/%s.txt", argv[argc - 1]);
    FILE *arquivo = fopen(turma_relatorio, "w");
    if (!arquivo) {
        perror("Erro ao criar o arquivo");
        return 1;
    }

    fprintf(arquivo, "Relatório de Presença\n");
    fprintf(arquivo, "======================\n");
    fprintf(arquivo, "%s\n", argv[argc-2]);
    fprintf(arquivo, "Data: %s\n", argv[1]);
    fprintf(arquivo, "======================\n");
    for (int i = 2; i < argc-2; i++) {
        fprintf(arquivo, "%s      [  ]  Presente? \n", argv[i]);
    }

    fclose(arquivo);
    printf("Relatório de presença gerado!\n");
    return 0;
}