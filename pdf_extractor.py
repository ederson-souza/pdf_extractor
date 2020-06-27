#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import pdftotext
import re


def read_data(file):
    
    """ Description Reads a PDF file and store information
    :type file: String like. Path to the PDF file.
    :param file: PDF file to read.

    :raises: Data extracted from PDF file.

    :rtype: String
    """
    
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f)
        data = ''
        for page in range(162):
            data += pdf[page]
            f.close()
        return data

def preprocessing(string):
    
    """ Description: Preprocessing pipeline to take useful information from the text.
    :type string: String
    :param string: String with data extracted from PDF file.

    :raises: Dictionary containing keys 'dates' and 'values'.

    :rtype: Dictionary
    """
    string1 = re.sub('\s{2,}', ' ', string)
    pattern = r'(PROJUDI)(.*?)(SANTOS )'
    string1 = re.sub(pattern, '', string1)
    string1 = re.sub(r'(\d{4}-\d{2}-\d{2}/\d{4})(.+?)(Saldo \(R\$\) )', '', string1)
    string1 = re.sub(r'(\d\d/\d\d)( SALDO.*?)(,\d\d\s?-? )', '', string1)
    string1 = re.sub(r'(\d\d/\d\d)( \(-\).*?)(,\d\d\s?-? )', '', string1)
    matches = re.findall(r'(\d\d/\d\d)(?: .*?)([\d\.]*\d+,\d\d\-?)', string1)
    dados = {'datas': [], 'valores':[]}
    for lancamento in matches:
        dados['datas'].append(lancamento[0])
        valor = lancamento[1]
        valor = re.sub(r'\.', '', valor)
        valor = re.sub(r',', '.', valor)
        if '-' in valor:
            valor = '-' + valor.replace('-', '')
        dados['valores'].append(round(float(valor),2)) 
    return dados

def save_xlsx(data):
    
    """ Description: Save extracted data to XLSX.
    :type data: Dictionary
    :param data: Preprocessed data. 

    :raises: XLSX file containg data needed.

    :rtype: XLSX file.
    """
    df = pd.DataFrame(data)
    df.to_excel('digitacao_pronta.xlsx', index=False)


raw_data = read_data('novos_extratos.pdf')
final_data = preprocessing(raw_data)
save_xlsx(final_data)
