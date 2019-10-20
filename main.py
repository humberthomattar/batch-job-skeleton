#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Informacoes Gerais

    Nome: generic-job
    Objetivo: Estrutura generica de progrma batch, inicialmente:
    - parametros externalizados,
    - log configurado,
    - leitura de múltiplos arquivos com padrão de nome
"""

# Metados
__maintainer__ = "Humbertho.Mattar"
__status__ = "Testing"
__version__ = "0.0.1"

import os
import sys
import yaml
import logging
from logging.config import fileConfig

def print_banner(texto):
    import pyfiglet
    print(pyfiglet.figlet_format(texto))
    return


def get_conf(file):
    import yaml
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    globals().update(cfg)
    return


def get_args():
    """
    Objetivo: Recuperar o parametro e validar na lista de valores válidos.

    """
    try:
        if (sys.argv[1] in accept_args):
            return str(sys.argv[1])
        else:
            logger.error(
                'Necessario ser um dos parametros da lista: ' + str(accept_args))
            sys.exit(1)
    except Exception as e:
        logger.error('Ausencia de um dos parametros da lista: ' + 
                    str(accept_args) + '.  error_msg: ' + str(e))
        sys.exit(1)


def set_filehandler(path, file):
    """
    Objetivo: Define um novo arquivo de log, sempre que chamado.

    path: diretorio dos arquivos de log
    file: nome do arquivo que está sendo processado.
    """
    from datetime import datetime
    try:
        filename = path + \
                   '{:%Y%m%d%H%M}.'.format(datetime.now()) + \
                   os.path.splitext(os.path.basename(file))[0] + '.log'
        file_handler = logging.handlers.RotatingFileHandler(filename)
        f = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        file_handler.setFormatter(f)
        logger.addHandler(file_handler)
        return
    except Exception as e:
        logger.error('Não foi possivel criar o arquivo de log. error_msg: ' + \
                      str(e))
        sys.exit(1)


def get_files(path, pattern):
    """
    Objetivo: Recuperar arquivos de um determinado diretorio.
    
    path: Diretorio dos arquivos a serem processados.
    pattern: Padrão de nomenclatura dos arquivos. Utilizado para \
    filtrar na pesquisa do diretorio.
    """
    import glob
    try:
        list_files = glob.glob(os.path.join(path, pattern), recursive=False)
        if list_files:
            logger.info("Arquivos a serem processados: " + str(list_files))
            return list_files
        else:
            logger.info("Nenhum arquivo encontrado em: " + str(files['path_in']))
            sys.exit(1)    
    except Exception as e:
        logger.error('Falha ao recuperar a lista de arquivos. erro_msg: ' + str(e))
        sys.exit(1)


def main():
    """
    Objetivos: Funcao de orquestracao da rotina nos arquivos. 
    Para cada arquivo, ela é a primeira a ser executada..

    """
    file_type = get_args()
    list_files = get_files(files['path_in'], files['pattern'])
    logger.info('Iniciando o processamento do(s) arquivo(s) de ' + 
                 str(file_type))
    # Início do loop nos arquivos

    for file in list_files:
        set_filehandler(log['path'], file)
        logger.info('Criado o arquivo de log para o arquivo: ' + str(file))
        # 
        # Inserir o código aqui
        #

    # Fim do loop nos arquivos
    logger.info('Fim da rotina')
    return


if __name__ == '__main__':
    #print_banner("Created by DtpLabs!!")
    fileConfig('conf/logging.ini')
    logger = logging.getLogger()
    get_conf('conf/config.yaml')
    sys.exit(main())
