import streamlit as st
import pandas as pd

def normalize_headers(df_sheet:pd.DataFrame, headers_normalization): 
    df_sheet.rename(columns=headers_normalization,inplace=True)
    return df_sheet

def normalize_staff(df_sheet:pd.DataFrame,staff):
    df_sheet["Estamento Del Supervisado"] = (
        df_sheet["Estamento Del Supervisado"].astype(str).str.strip().str.lower().replace(staff)
    )
    return df_sheet

def normalize_units(df_sheet: pd.DataFrame, units):
    """Homologa variantes sencillas del nombre de la unidad o servicio."""
    for column in ("Unidad/Servicio Del Supervisado", "Unidad/Servicio Supervisado"):
        if column in df_sheet.columns:
            values = df_sheet[column].astype(str).str.strip().str.lower()
            df_sheet[column] = values.map(units).fillna(values.str.title())
    return df_sheet

def normalize_timestamps_marca_temporal(df_sheet: pd.DataFrame):
    if "marca temporal" in list(df_sheet.columns):
        df_sheet["marca temporal"] = pd.to_datetime(df_sheet["marca temporal"], errors='coerce')
        df_sheet["Fecha De Registro"] = df_sheet["marca temporal"].dt.strftime('%d-%m-%Y')
        df_sheet["Hora De Registro"]  = df_sheet["marca temporal"].dt.time
        df_sheet.drop(columns='marca temporal',inplace=True)
        
    return df_sheet

def normalize_timestamps_fecha_supervision(df_sheet: pd.DataFrame):
    for column in list(df_sheet.columns):
        try:
            if pd.Timestamp(column):
                df_sheet["Fecha De Supervisión"] = pd.to_datetime(df_sheet[column],errors='coerce')        
                df_sheet["Fecha De Supervisión"] = df_sheet["Fecha De Supervisión"].dt.strftime('%d-%m-%Y')
                df_sheet.drop(columns=column, inplace=True)
        except ValueError:
            pass
    
    if "Fecha De Supervisión" in list(df_sheet.columns):
        df_sheet["Fecha De Supervisión"] = pd.to_datetime(
            df_sheet["Fecha De Supervisión"], errors='coerce'
        ).dt.strftime('%d-%m-%Y')

    if "Fecha De Instalación" in list(df_sheet.columns):
        df_sheet["Fecha De Instalación"] = pd.to_datetime(
            df_sheet["Fecha De Instalación"], errors='coerce'
        ).dt.strftime('%d-%m-%Y')

    return df_sheet

def clean_run(run):
    run = str(run)
    result_sum = 0
    index = 0
    series = [2,3,4,5,6,7]
    cleaned_run = ''.join(c for c in run if c.isdigit() or c == 'K' or c == 'k')

    if cleaned_run == '':
        return f'RUT No Ingresado'

    if len(cleaned_run) < 8 or len(cleaned_run) > 9:
        return f'RUT Inválido. (Verficar {run})'

    body = cleaned_run[:-1]
    dv = cleaned_run[-1].upper()
    
    fbody = body[:-6]
    mbody = body[-6:-3]
    lbody = body[-3:]
    
    body_reversed = list(reversed(body)) # 'reversed' devuelve un objeto iterable. A ese objeto iterable lo listo con 'list'.
    
    for body_factor in body_reversed: 
        body_factor = int(body_factor)

        serie_factor = series[index % len(series)]

        result_mult = serie_factor * body_factor
        result_sum = result_mult + result_sum

        index = index + 1 

    body_residual = result_sum % 11
    dv_result = 11 - body_residual

    if dv_result == 10:
        dv_result = 'K'
    elif dv_result == 11:
        dv_result = '0'
    
    if dv != str(dv_result):
        return f'RUT Inválido. (Verficar {run})'
    else:
        return fbody + '.' + mbody + '.' + lbody + '-' + dv

def clean_initials(initial):
    initial = str(initial)
    cleaned_initial = ''.join(c for c in initial if c != '.')
    if cleaned_initial == ('nan'):
        return "No Ingresó Iniciales"
    else:
        return cleaned_initial.upper().replace(" ","")
        
def question_analysis(answers):
    for answer in answers:
        if str(answer).lower().strip() == 'no':
            return "No Cumple"    
    return "Cumple"

def question_analysis_row(row: pd.Series):
    """Calcula el resultado de una fila y aplica la regla especial de barba."""
    for column, answer in row.items():
        text = str(answer).strip().lower()
        if "barba" in str(column).lower():
            if text != "no":
                return "No Cumple"
        elif text == "no":
            return "No Cumple"
    return "Cumple"
    
def priority_columns(df_sheet:pd.DataFrame, priority, rest):
    first = []
    for column in priority:
        if column in df_sheet.columns:
            first.append(column)
    
    rest = []
    for column in df_sheet.columns:
        if column not in priority:
            rest.append(column)
    df_sheet["Resultado"] = df_sheet[rest].apply(question_analysis_row,axis=1)
    total_columns = first + rest + ["Resultado"]

    #return first + rest
    return total_columns
