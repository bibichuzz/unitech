/*
 * ================================================================================
 * SISTEMA UNITECH - MÓDULO DE GERAÇÃO DE RELATÓRIOS DE PRESENÇA
 * ================================================================================
 * 
 * DESCRIÇÃO:
 * Este programa é responsável por gerar relatórios de presença para professores.
 * Ele cria um arquivo de texto formatado com a lista de todos os alunos de uma
 * turma, incluindo espaços para marcar presença manualmente.
 * 
 * USO:
 * ./relatorio_presenca <data> <aluno1> <aluno2> ... <alunoN> <info_turma> <nome_arquivo>
 * 
 * PARÂMETROS ESPERADOS (argv):
 * argv[1]         = Data da aula (formato: dd/mm/aaaa)
 * argv[2..N-2]    = Lista de alunos (Nome - Matrícula)
 * argv[N-1]       = Informações da turma (Turma X, curso Y, Zº semestre)
 * argv[N]         = Nome do arquivo a ser gerado (Turma_Data sem barras)
 * 
 * ARQUIVO GERADO:
 * Pasta: relatorios_presenca/
 * Nome: <turma>_<data>.txt
 * Exemplo: SI1A23_25102023.txt
 * 
 * FORMATO DO RELATÓRIO:
 * Relatório de Presença
 * ======================
 * Turma SI1A23, curso Sistemas de Informação, 1º semestre
 * Data: 25/10/2023
 * ======================
 * Maria Silva - A12345B      [  ]  Presente?
 * João Santos - B67890C      [  ]  Presente?
 * ...
 * 
 * ================================================================================
 */

#include <stdio.h>

int main(int argc, char *argv[]) {
    // Declaração do buffer para armazenar o caminho do arquivo
    char turma_relatorio[30];
    
    // Monta o caminho do arquivo usando o último argumento como nome
    // argv[argc-1] = Nome do arquivo (exemplo: SI1A23_25102023)
    // Estrutura: relatorios_presenca/<nome_arquivo>.txt
    sprintf(turma_relatorio, "relatorios_presenca/%s.txt", argv[argc - 1]);
    
    // Abre o arquivo para escrita (modo "w")
    FILE *arquivo = fopen(turma_relatorio, "w");
    
    // Verifica se o arquivo foi criado com sucesso
    if (!arquivo) {
        perror("Erro ao criar o arquivo");
        return 1; // Retorna código de erro
    }

    // Escreve o cabeçalho do relatório
    fprintf(arquivo, "Relatório de Presença\n");
    fprintf(arquivo, "======================\n");
    
    // Escreve as informações da turma (ante/penúltimo argumento)
    // argv[argc-2] = Nome do professor
    // argv[argc-3] = Informações da turma (exemplo: "Turma SI1A23, curso...")
    fprintf(arquivo, "Professor %s\n", argv[argc-2]);
    fprintf(arquivo, "%s\n", argv[argc-3]);
    
    // Escreve a data da aula (primeiro argumento após o nome do programa)
    // argv[1] = Data no formato dd/mm/aaaa
    fprintf(arquivo, "Data: %s\n", argv[1]);
    fprintf(arquivo, "======================\n");
    
    // Loop para escrever todos os alunos da turma
    // Começa em argv[2] (primeiro aluno) e vai até argc-2 (antes das informações da turma)
    for (int i = 2; i < argc-3; i++) {
        // Escreve o nome do aluno com checkbox para marcar presença
        // Formato: "Nome do Aluno - Matrícula      [  ]  Presente?"
        fprintf(arquivo, "%s      [  ]  Presente? \n", argv[i]);
    }

    // Fecha o arquivo para garantir que os dados sejam salvos
    fclose(arquivo);
    
    // Mensagem de confirmação para o usuário
    printf("Relatório de presença gerado!\n");
    
    return 0; // Retorna sucesso
}