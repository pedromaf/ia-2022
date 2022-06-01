class Estado:

    def __init__(self, missionarios_esq, missionarios_dir, canibais_esq, canibais_dir, lado_rio):
        # Inicializa um estado do problema contendo a informação da quantidade de missionários e canibais
        # de cada lado do rio e o lado do rio em que o barco se encontra.
        self.missionarios_esq = missionarios_esq
        self.missionarios_dir = missionarios_dir
        self.canibais_esq = canibais_esq
        self.canibais_dir = canibais_dir
        self.lado_rio = lado_rio
        self.pai = None
        self.filhos = []

    def validar_estado(self):
        # Número negativo de missionários ou canibais retorna estado inválido.#
        if (self.missionarios_esq < 0 or self.missionarios_dir < 0 or self.canibais_esq < 0 or self.canibais_dir < 0):
            return False

        # Número de missionários menor que número de canibais em algum lado do rio retorna estado inválido.
        # Se não existir nenhum missionário de um lado do rio não impede a presença de canibais do mesmo lado.
        if ((0 < self.missionarios_esq < self.canibais_esq) or (0 < self.missionarios_dir < self.canibais_dir)):
            return False
        else:
            return True

    def gerar_estados_filhos(self):
        # O barco permite passar até 2 missionários/canibais por vez.
        movimentos_possiveis = [{'mis': 2, 'can': 0},
                                 {'mis': 1, 'can': 1},
                                 {'mis': 0, 'can': 2},
                                 {'mis': 1, 'can': 0},
                                 {'mis': 0, 'can': 1}]

        for movimento in movimentos_possiveis:
            if(self.lado_rio == 'dir'):
                # Caso o lado atual do rio seja o direito, o calculo é feito passando
                # os valores do movimento para o lado esquerdo.
                filho_missionarios_esq = self.missionarios_esq + movimento['mis']
                filho_missionarios_dir = self.missionarios_dir - movimento['mis']
                filho_canibais_esq = self.canibais_esq + movimento['can']
                filho_canibais_dir = self.canibais_dir - movimento['can']

                estado_filho = Estado(filho_missionarios_esq, filho_missionarios_dir, filho_canibais_esq,
                                      filho_canibais_dir, 'esq')
            else:
                # Caso o lado atual do rio seja o esquerdo, o calculo é feito passando
                # os valores do movimento para o lado direito.
                filho_missionarios_esq = self.missionarios_esq - movimento['mis']
                filho_missionarios_dir = self.missionarios_dir + movimento['mis']
                filho_canibais_esq = self.canibais_esq - movimento['can']
                filho_canibais_dir = self.canibais_dir + movimento['can']

                estado_filho = Estado(filho_missionarios_esq, filho_missionarios_dir, filho_canibais_esq,
                                      filho_canibais_dir, 'dir')

            estado_filho.pai = self

            # Valida o novo estado filho gerado, caso o estado seja válido ele
            # é adicionado a lista de filhos do estado atual.
            if(estado_filho.validar_estado()):
                self.filhos.append(estado_filho)

    def verificar_solucao(self):
        # True se todos os canibais e misisonários estão do lado direito do rio.
        return (self.missionarios_esq == self.canibais_esq == 0 and self.missionarios_dir == self.canibais_dir == 3)

    def __str__(self):
        return f"<ESQ>  |  <DIR>\n M:{self.missionarios_esq}   |   M:{self.missionarios_dir}\n C:{self.canibais_esq}" \
               f"   |   C:{self.canibais_dir}\n"


class Problema:

    def __init__(self):
        # Fila de execução com o estado inicial (raiz) com 3 missionários e 3 canibais do lado esquerdo do rio.
        self.fila = [Estado(3, 0, 3, 0, 'esq')]
        # Lista que guarda a solução a partir da raiz até o estado com o problema solucionado.
        self.solucao = []

    def solucionar(self):
        # Iterar na fila de execução utilizando busca em largura.
        for estado in self.fila:
            if(estado.verificar_solucao()):
                # Se estado atual for a solução, o caminho do estado atual até a raiz
                # será enfileirado de trás pra frente (raiz -> solução).
                self.solucao = [estado]
                while estado.pai is not None:
                    self.solucao.insert(0, estado.pai)
                    estado = estado.pai
                break

            # Caso o estado atual não for a solução, será gerado os estados filhos a
            # partir do estado atual e enfileirados seguindo a busca em largura.
            estado.gerar_estados_filhos()
            self.fila.extend(estado.filhos)


if(__name__ == "__main__"):
    problema = Problema()
    problema.solucionar()

    for estado_solucao in problema.solucao:
        print(estado_solucao)
