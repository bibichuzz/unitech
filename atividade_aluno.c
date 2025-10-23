#include <stdio.h>

int main(int argc, char *argv[]) {
    char atividade_aluno[30];
    sprintf(atividade_aluno, "atividades_alunos/%s_%s.txt", argv[1], argv[5]);
    FILE *arquivo = fopen(atividade_aluno, "w");
    if (!arquivo) {
        perror("Erro ao criar o arquivo");
        return 1;
    }

    fprintf(arquivo, "Disciplina: %s\n", argv[7]); 
    fprintf(arquivo, "Atividade: %s\n", argv[3]);
    fprintf(arquivo, "======================\n");
    fprintf(arquivo, "Nome: %s\n", argv[4]);
    fprintf(arquivo, "Matrícula: %s\n", argv[5]);
    fprintf(arquivo, "======================\n");
    fprintf(arquivo, "%s\n\n", argv[3]);
    fprintf(arquivo, "Resposta: %s\n", argv[6]);

    fclose(arquivo);
    printf("Atividade enviada!\n");
    return 0;
}