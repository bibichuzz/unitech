/*
 * ================================================================================
 * SISTEMA UNITECH - MÓDULO DE ENTREGA DE ATIVIDADES DE ALUNOS
 * ================================================================================
 * 
 * DESCRIÇÃO:
 * Este programa é responsável por criar arquivos de texto contendo as respostas
 * das atividades entregues pelos alunos. Ele recebe informações via linha de
 * comando e gera um arquivo formatado com os dados da atividade e a resposta.
 * 
 * USO:
 * ./atividade_aluno <id_atividade> <arg2> <titulo> <nome> <matricula> <resposta> <disciplina>
 * 
 * PARÂMETROS ESPERADOS (argv):
 * argv[1] = ID da atividade (exemplo: XYZ1111)
 * argv[2] = (não utilizado no código atual)
 * argv[3] = Título da atividade
 * argv[4] = Nome completo do aluno
 * argv[5] = Matrícula do aluno
 * argv[6] = Resposta/conteúdo da atividade
 * argv[7] = Nome da disciplina
 * 
 * ARQUIVO GERADO:
 * Pasta: atividades_alunos/
 * Nome: <id_atividade>_<matricula>.txt
 * Exemplo: XYZ1111_A12345B.txt
 * ================================================================================
 */

#include <stdio.h>
#include <time.h>

int main(int argc, char *argv[]) {
    // Declaração do buffer para armazenar o caminho do arquivo
    char atividade_aluno[30];
    
    // Monta o caminho do arquivo: atividades_alunos/<id_atividade>_<matricula>.txt
    // argv[1] = ID da atividade, argv[5] = Matrícula do aluno
    sprintf(atividade_aluno, "atividades_alunos/%s_%s.txt", argv[1], argv[5]);
    
    // Abre o arquivo para escrita (modo "w")
    FILE *arquivo = fopen(atividade_aluno, "w");
    
    // Verifica se o arquivo foi criado com sucesso
    if (!arquivo) {
        perror("Erro ao criar o arquivo");
        return 1; // Retorna código de erro
    }

    // Escreve o cabeçalho do arquivo com informações da disciplina
    fprintf(arquivo, "Disciplina: %s\n", argv[7]); 
    
    // Escreve o título da atividade
    fprintf(arquivo, "Atividade: %s\n", argv[2]);
    
    fprintf(arquivo, "======================\n");
    
    // Dados do aluno
    fprintf(arquivo, "Nome: %s\n", argv[4]);
    fprintf(arquivo, "Matrícula: %s\n", argv[5]);
    time_t agora = time(NULL);
    fprintf(arquivo, "Data de Entrega: %s\n", ctime(&agora));
    
    fprintf(arquivo, "======================\n");
    
    // Conteúdo da atividade
    fprintf(arquivo, "%s\n\n", argv[3]);
    
    // Escreve a resposta do aluno
    fprintf(arquivo, "Resposta: %s\n", argv[6]);

    // Fecha o arquivo para garantir que os dados sejam salvos
    fclose(arquivo);
    
    // Mensagem de confirmação para o usuário
    printf("Atividade enviada!\n");
    
    return 0; // Retorna sucesso
}