import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Calidad App - Hospital Mario Sánchez")
name = st.text_input("¿Tu Nombre?")
st.write(f"Hola {name}")

uploaded_file = st.file_uploader("Sube tu Excel", type="xlsx")

units = { # ¿Como refactorizar este diccionario para evitar tener que homologar cada unidad? Si mal no recuerdo, necesita librería extra
                        "unidad de emergencia":"Emergencia",
                        "unidad emergencia":"Emergencia",
                        "emergencia":"Emergencia",

                        "pabellón":"Pabellón",
                        "pabellon":"Pabellón",
                        
                        "pabellón / esterilización":"Pabellón/Esterilización",
                        "pabellón/esterilización":"Pabellón/Esterilización",
                        "pabellón/ esterilización":"Pabellón/Esterilización",
                        "pabellón /esterilización":"Pabellón/Esterilización",

                        "pabellon / esterilizacion":"Pabellón/Esterilización",
                        "pabellon/esterilizacion":"Pabellón/Esterilización",
                        "pabellon/ esterilizacion":"Pabellón/Esterilización",
                        "pabellon /esterilizacion":"Pabellón/Esterilización",

                        "pabellón / esterilizacion":"Pabellón/Esterilización",
                        "pabellon/esterilización":"Pabellón/Esterilización",
                        "pabellón/ esterilizacion":"Pabellón/Esterilización",
                        "pabellon /esterilización":"Pabellón/Esterilización",

                        "pabellon / esterilización":"Pabellón/Esterilización",
                        "pabellón/esterilizacion":"Pabellón/Esterilización",
                        "pabellon/ esterilización":"Pabellón/Esterilización",
                        "pabellón /esterilizacion":"Pabellón/Esterilización",

                        "maternidad":"Maternidad",
                        "maternidad / uego":"Maternidad",
                        "maternidad/uego":"Maternidad",
                        "maternidad/ uego":"Maternidad",
                        "maternidad /uego":"Maternidad",

                        "policlínico":"Policlínico",
                        "policlinico":"Policlínico",

                        "dental":"Dental",

                        "medicina":"Medico-Qirúrgico",

                        ### OUT OF SCOPE???

                        "alimentación":"Alimentación",
                        "alimentacion":"Alimentación",

                        "esterilización":"Esterilización",
                        "esterilizacion":"Esterilización",

                        "servicios generales":"Servicios Generales",

                        "box de atención":"BOX De Atención",
                        "box de atencion":"BOX De Atención",
                        }

    # Función "normalización de unidades": nombres de unidades con algunas variantes que son lo mismo, entonces tomo el diccionario creado, para tomar como referencia
    # alguno de los nombres que se 'podrían encontrar' y los valido con un nombre común. Sirve para recorrer la "Serie" del df[unidad supervisada/del supervisado]

def unit_normalization(unit):   
    unit = str(unit).lower().strip() # Se encuentra coincidencia, lo valido como str, paso a minuscula, saco espacios anteriores y posteriores.
    return units.get(unit,"Unidad No Encontrada") # Retorno lo encontrado dentro de units, y obtengo la coincidencia curada, como 2do argumento, si no lo encuentro, devuelvo "Unidad No Encontrada"


    # Función "limpieza de rut": Recorro la 'Serie' de los df que manejen RUT
def clean_run(run):      
    run = str(run) # Valido lo que trabajaré (números) como 'str' (y no como int). La var 'run' contendrá lo encontrado en cada celda del df[serie] recorrido. 
    cleaned = ''.join(c for c in run if c.isdigit() or c == 'K' or c == 'k').upper() # Recorro lo encontrado en la celda del df correspondiente. 
              # Si encuentra espacios, los une. Recorre 'caracter', caracter por caracter en 'run' y valida si 'caracter' is digito (¿Valida si es núemero str y no letra str?. Duda). Se guarda
              # en var.  
              # IMPORTANTE: .isdigit efectivamente valida si es dígito, esto devuelve True o False. Lo mismo que con 'k' o 'K'. Solo conservo en 'cleaned' lo correctamente validado.

    if len(cleaned) < 8 or len(cleaned) > 9: # Una vez 'curado' el rut, validamos la estructura del mismo, y que cumpla 'de alguna manera, que es rut'. Validamos por descarte.
                                             # Si el 'largo' de la var anterior es < 8 ó > 9, ya no es un rut 'válido'.    
        return f'RUN {cleaned} Inválido'    # Muestra RUN Inválido si no se ingresa RUN
    else: #Sino, y es válido, lo estructuramos 
        body = cleaned[:-1] # Separamos cuerpo y 
        dv = cleaned[-1] #DV
        
        fbody = body[:-6] # Lógica: Cuento desde útimo dígito hacia atrás (6), y tomo todo lo que está desde el comienzo hasta el dígito donde esté -6
        mbody = body[-6:-3] # Lógica: Cuento -6 desde derecha a izquierda. Desde el dígito encontrado, abarco todo lo que encuentre hasta -3.
        lbody = body[-3:] # Lógica: Cuento -3 de der a izq, y abarco hace la derecha todo lo encontrado.
    
    return fbody + '.' + mbody + '.' + lbody + '-' + dv # Retorno cada var curada y la concateno.
    # IMPORTANTE: ¿Debería utilizar una función que valide RUT matemáticamente? ¿O con solo validar estructura ya me vale? 

#############################################################################################################################################################################

### Se utiliza para columnas vacías en "Observaciones" y "Número de autoclave en supervision"
def empty_cells_normalization(empy_cell):
    empy_cell = str(empy_cell) # Normalizo todo lo encontrado dentro del df[Observaciones] (Toda la columna)
    if empy_cell == '' or empy_cell == 'nan': # Si no encuentro datos en celda, o objeto 'nan' 
        return '' # Retorno vacío
    else: # Sino
        return empy_cell.capitalize() # Devuelvo lo encontrado, con mayúscula inicial.    


#############################################################################################################################################################################

    # Función para campo "Iniciales del supervisado" para quitar puntos y espacios intermedios, iniciales y finales.    
def clean_initials(initial):
    initial = str(initial) # Lo valido como str
    cleaned_initial = ''.join(c for c in initial if c != '.') # Uno espacios vacíos si existen. Recorro caracter por caracter, si caracter es distinto a '.' (Esta lógica todavía no la interiorizo bien, o bien no la he entendido) 
    if cleaned_initial == ('nan'): # Si las iniciales curadas == a 'nan' (celdas vacías)
        return 'No Ingresó Iniciales'   # Retorno que no se ingresaron.
    else: # Sino
        return cleaned_initial.upper().replace(" ","") # Retorno lo encontrado, en mayúsculas, y reemplazando 'espacios' por 'no espacios' (junto caracteres).

    # Función para Análisis de Preguntas
def question_analisis(answers): 
    for answer in answers: # Recorro todas las celdas que abarquen una posible respuesta EN FILAS.
        if str(answer).strip().lower() == 'no': # Si encuentra un "No", el usuario supervisado "No Cumple".
            return 'No Cumple' #Retorno "No Cumple"
    return 'Cumple' # Si en el recorrido no se encuetra un "no", Cumple.

#####   def question_analisis_exception(answers): 
#####       if "1- ¿El supervisado usa barba?" in df.columns:
#####           for answer_no in answers:                       #### Debo también recorrer la columna de 'usar barba' para encontrar no. #¿Para no cumple, debo validar un si == df[columns] usa barba?
#####               if str(answer_no).strip().lower() == 'si':
#####                   return "Al tener 'Si' en esta columna, ya lo arruina todo"



if uploaded_file:

    xls = pd.ExcelFile(uploaded_file)
    sheet = st.selectbox("Selecciona una hoja", xls.sheet_names)
    
    df = pd.read_excel(xls, sheet_name=sheet)

    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()


####### CASO "HOJA SELLADO". Problema: Para cumplimiento, una de las respuestas debe ser 'no', especificamente '1.-¿el supervisado usa barba'? 

#####       if "1.- ¿El supervisado usa barba?" in df.columns:
#####           df["1- ¿El Supervisado Usa Barba?"] = df["1- ¿El supervisado usa barba?"].apply(question_analisis_exception)
#####           df.drop(columns="1.- ¿El supervisado usa barba?")



    # Constricción de "Columnas" y su "Reemplazo"
    if "marca temporal" in df.columns: # Si existe "marca temporal" en algun header (dataframes.columnas)
        df['Fecha Registro'] = df['marca temporal'].dt.strftime('%d-%m-%Y') # Tomar el dataframe encontrado, transformarlo y validarlo a datetime (formato fecha) y extraer solo el formato fecha
                                                                            # y crear un dataframe nuevo como "Fecha Registro".
        df['Hora Registro'] = df["marca temporal"].dt.time # Tomar el dataframe encontrado, extraer lo que represente algun formato fecha, 
        df = df.drop(columns="marca temporal")    

    run_headers = {
                    "run supervisado (sin puntos, con guion)":"RUT Funcionario",
                    "run supervisado":"RUT Funcionario",
                    "run del supervisado":"RUT Funcionario",
                    "run paciente":"RUT Paciente"               
                    }

    for run_header in list(df.columns): ### Con 'list' creo una ¿instancia de la serie? con lo cual no manipulo el df[serie]  
        if run_header in run_headers:
            cleaned_run_header = run_headers[run_header]
            df[cleaned_run_header] = df[run_header].apply(clean_run)            
            df = df.drop(columns=[run_header])
    
###########################################################################################################################################################################
    
    supervision_date_headers = {
                                "fecha de supervisión":"Fecha De Supervisión",
                                "fecha de supervision":"Fecha De Supervisión",
                                "fecha supervisión":"Fecha De Supervisión",
                                "fecha supervision":"Fecha De Supervisión",                                
                                }
    
    for column in list(df.columns): # Recorro 'columnas'
        try: # Intento:
            if pd.Timestamp(column): # Si dentro de las columnas existe algo parecido a un 'TimeStamp'
                df["Fecha De Supervisión"] = pd.to_datetime(df[column], errors="coerce") # La serie de la columna donde hay TimeStamp, lo transformo a 'Fecha De Supervisión'.
                df["Fecha De Supervisión"] = df["Fecha De Supervisión"].dt.strftime('%d-%m-%Y') # 'Fecha De Supervisión' lo transformo en str de formato fecha.
                df = df.drop(columns=column) # Elimino la columna 'original' donde se encuentre un formato fecha.)
        except ValueError: # Sino encuentro, solo 'paso'.
            pass 
    
    for supervision_date_header in list(df.columns):
        if supervision_date_header in supervision_date_headers:
            cleaned_supervision_date_header = supervision_date_headers[supervision_date_header]
            df[cleaned_supervision_date_header] = pd.to_datetime(df[supervision_date_header],errors="coerce") # Lo encontrado en df[final_col_sdh], lo valido como fecha...
            df[cleaned_supervision_date_header] = df[cleaned_supervision_date_header].dt.strftime('%d-%m-%Y') # Para luego transformarlo en fecha formato texto.
            df = df.drop(columns=[supervision_date_header])
    ### Cuando debo manejar fechas en las celdas de las columnas, debo transformar a pd.to_datetime, despues a df.strftime(%d-%m-%Y)
    
###########################################################################################################################################################################
  
    
    
    supervised_unit_headers = {
                                "unidad o servicio del supervisado":"Unidad/Servicio Del Supervisado",
                                "unidad supervisada":"Unidad/Servicio Supervisado",
                                "unidad o servicio supervisado":"Unidad/Servicio Supervisado" ,
                                "lugar supervisado":"Unidad/Servicio Supervisado"                       
                            }
    
    for og_col_suh in list(df.columns):
        if og_col_suh in supervised_unit_headers:
            final_col_suh = supervised_unit_headers[og_col_suh]
            df[final_col_suh] = df[og_col_suh].apply(unit_normalization)
            df = df.drop(columns=[og_col_suh])

    supervisor_initials = {
                            "iniciales del supervisor":"Iniciales Del Supervisor",
                            "iniciales de supervisor":"Iniciales Del Supervisor",
                            "iniciales supervisor":"Iniciales Del Supervisor",
    }       
    for og_si in df.columns:
        if og_si in supervisor_initials:
            final_si = supervisor_initials[og_si]
            df[final_si] = df[og_si].apply(clean_initials)
            df = df.drop(columns=[og_si])

    if "observaciones" in df.columns:
        df["Observaciones"] = df["observaciones"].apply(empty_cells_normalization)
        df = df.drop(columns="observaciones")

    if "numero de autoclave en supervision" in df.columns:
        df["Número De Autoclave (En Supervición)"] = df["numero de autoclave en supervision"].apply(empty_cells_normalization)
        df = df.drop(columns="numero de autoclave en supervision")

    # Estamento Del Supervisaro (supervised statement)
    supervised_estament = {
                            "estamento del supervisado":"Estamento Del Supervisado",
                            "estamento supervisado":"Estamento Del Supervisado"
                        }
    for og_ss in df.columns:
        if og_ss in supervised_estament:
            final_ss = supervised_estament[og_ss]
            df[final_ss] = df[og_ss]
            df = df.drop(columns=[og_ss])

    if "nombre del paciente" in df.columns:
        df["Nombre Del Paciente"] = df["nombre del paciente"]
        df = df.drop(columns="nombre del paciente")

    installation_date = {
                    "fecha de instalación":"Fecha De Instalación",
                    "fecha de instalacion":"Fecha De Instalación"
    }
    for og_installation_date in df.columns:
        if og_installation_date in installation_date:
            f_installation_date = installation_date[og_installation_date]
            df[f_installation_date] = pd.to_datetime(df[og_installation_date],errors="coerce")
            df[f_installation_date] = df[f_installation_date].dt.strftime('%d-%m-%Y')
            df = df.drop(columns=[og_installation_date])
    ### Cuando debo manejar fechas en las celdas de las columnas, debo transformar a pd.to_datetime, despues a df.strftime(%d-%m-%Y)    

    supervised_room = {
                        "habitación supervisada":"Habitación Supervisada",
                        "habitacion supervisada":"Habitación Supervisada",
    }
    for og_supervised_room in df.columns:
        if og_supervised_room in supervised_room:
            f_supervised_room = supervised_room[og_supervised_room]
            df[f_supervised_room] = df[og_supervised_room]
            df = df.drop(columns=[og_supervised_room])

    
########## Recorrido y Construcción de DataFrames ##########

    priority = ['Fecha De Supervisión','Fecha Registro','Hora Registro','RUT Funcionario','Unidad/Servicio Del Supervisado','Unidad/Servicio Supervisado',
                'Iniciales Del Supervisor','Estamento Del Supervisado','RUT Paciente',"Número De Autoclave (En Supervición)","Nombre Del Paciente","Fecha De Instalación",
                "Habitación Supervisada"]
    firsts = []
    for col in priority:
        if col in df.columns:
            firsts.append(col)
        
    
    rest = []
    for col in df.columns:
        if col not in priority:
            rest.append(col)
    df['Resultado'] = df[rest].apply(question_analisis,axis=1)
    new_cols = firsts + rest + ['Resultado']

    df = df[new_cols]
    st.write(df)



    ##### Bloque ANÁLISIS #####
    st.write("#### Sección Análisis (Total de Años por Unidad)") 

    selected_units = [] # Loǵica: Construye una variable (selected_units) que guarda una de las 2 condiciones resultates del if/elif.
    if "Unidad/Servicio Del Supervisado" in df.columns: # Si el "header" es "Unidad del Supervisado" en la "Series" de la columna:
        selected_units = df["Unidad/Servicio Del Supervisado"].unique() # selected_unit guarda "de esta serie" (df[xcv]) los ¿valores distintos de esta columna? Talves sea "Los distintos valores" de la columna.
        final_unit = st.selectbox("Seleccione Unidad a Analizar: ",selected_units)
        st.write(final_unit)
    elif "Unidad/Servicio Supervisado" in df.columns:   # Lo mismo.
        selected_units = df["Unidad/Servicio Supervisado"].unique()
        final_unit = st.selectbox("Seleccione Unidad a Analizar: ",selected_units)
        st.write(final_unit)  
    else:
        st.write("No Existen Unidades En Control De Vacío")
        st.stop()

    if "Unidad/Servicio Del Supervisado" in df.columns: # Si el "header" es "Unidad del Supervisado" en la "Series" de la columna:
        condition = df["Unidad/Servicio Del Supervisado"] == final_unit # Si por ej, final_unit es "Maternidad", entonces veo todo lo que hay en la series y reviso
                                                                        # que sea == a maternidad. Se guarda en condición.      
    elif "Unidad/Servicio Supervisado" in df.columns:   # Lo mismo, pero para unidad supervisada
        condition = df["Unidad/Servicio Supervisado"] == final_unit

    # En este bloque (Arriba) arroja error al cargar hoja 'control vacío', ya que en esta hoja no existe "Unidad/Servicio Supervisada / Del Supervisado"

    filtered_df = df[condition] # "filetered_df" es la variable que guarda todo lo encontrado en df[condition], si por ejemplo, se encontró "Maternidad" y "Emergencias", "filetered_df"
                                # contendrá ambas unidades provenientes del df[unidad supervisada/del supervisado]
    
    st.write(f"Unidad Seleccionada: {final_unit}")

    st.write(filtered_df)

#################### Sección Resultado Análisis de Unidad Seleccionada ####################

    total = len(filtered_df) ### Guardo la cantad de filas. En "tacto vaginal" son 7, (todas maternidad).
    result = filtered_df["Resultado"] == "Cumple"   # filtro "Resultado" de filteder_df solo si es == a "Cumple". En "result" guardo solo "Cumple" (o guardo que sea True en result??? Tengo dudas de que guarda realmente).
    final_result = filtered_df[result] # Filtro de "result" solo las filas que cumplen la condición anterior "Cumple" y se guarda en final result.
    
    cumplen = len(final_result) # Cuento la cantidad de resultados que "Cumplen".
    no_cumplen = total - cumplen
    porcentaje_cumple = (cumplen / total) * 100
    porcentaje_no_cumple = (no_cumplen / total) * 100

    col1,col2,col3,col4,col5 = st.columns(5)                                                        ####### IMPORTANTE: Desde acá, debo buscar la manera de poder filtrar el análisis por año. 
    col1.metric("Total Supervisados: ", total)                                                      ####### IMPORTANTE: Esta sección debo transformar nuevamente los campos de fecha (pasados a str) a formato fecha.
    col2.metric("Total Supervisado que 'Si Cumplen'", cumplen)
    col3.metric("Porcentaje de Cumplimiento",f"{porcentaje_cumple:.0f}%")
    col4.metric("Total Supervisado que 'No Cumple'",no_cumplen)
    col5.metric("Porcentaje de No Cumplimiento",f"{porcentaje_no_cumple:.0f}%") 
        
    #### Selección De Año ###

    st.write(f"#### Sección Análisis ({final_unit} por Año)") 
    
    if "Fecha De Supervisión" in df.columns: # Si existe fecha de supervisión en las columnas
        
        date_format = pd.to_datetime(filtered_df["Fecha De Supervisión"],format="%d-%m-%Y",errors="coerce") # De filtered_df, extraigo solo lo encontrado en "Fecha De Supervisión"
        extracted_years = date_format.dt.year.unique() # De date_format, solo extraigo los años como datos distintos encontrados. 
        selected_year = st.selectbox("Seleccione El Año A Analizar: ",extracted_years) # Selecciono el año con el selectbox. Esta variable "SOLO GUARDA AÑO" ya extraído de 'fecha de supervisión'.
        years_filtered_df = date_format.dt.year # De 'date_format' extraigo solo el 'año' (Recordar, date format viene con d-m-year)
        definitive_year = years_filtered_df == selected_year # De 'selected_year' (en selectbox) lo comparo con 'years_filtered_df', que son los años extraidos de date_format
        final_df = filtered_df[definitive_year] # De 'filtered_df', que es lo filtrado de 'unidades supervisadas', extraigo las coindicencias con 'año'
        
        st.write(final_df) # Contruyo la matriz con lo filtrado en 'final_df' (unidad -> año)

    total_filtered = len(final_df)
    
    condition_cumplen = final_df["Resultado"] == "Cumple"
    filtered_condition_cumplen = final_df[condition_cumplen]
    filtered_condicion_total_cumplen = len(filtered_condition_cumplen) #### REVISAR PORQUÉ ESTO FUNCIONA
    filtered_condition_no_cumplen = total_filtered - filtered_condicion_total_cumplen
    filtered_condition_porcentaje_cumple = (filtered_condicion_total_cumplen / total_filtered) * 100
    filtered_condition_porcentaje_no_cumple = (filtered_condition_no_cumplen / total_filtered) * 100
    
    col1,col2,col3,col4,col5 = st.columns(5)
    col1.metric("Total Supervisados", total_filtered) 
    col2.metric("Total Supervisados Que 'Si Cumplen'", filtered_condicion_total_cumplen)
    col3.metric("Porcentaje De Cumplimiento", f"{filtered_condition_porcentaje_cumple:.0f}%")
    col4.metric("Total Supervisado que 'No Cumple'",filtered_condition_no_cumplen)
    col5.metric("Porcentaje de No Cumplimiento",f"{filtered_condition_porcentaje_no_cumple:.0f}%") 

    
    if "Fecha De Supervisión" in df.columns:
        years_filterd = date_format.dt.year == selected_year
        years_data_frame = filtered_df[years_filterd]
        year_dates = pd.to_datetime(years_data_frame["Fecha De Supervisión"], format="%d-%m-%Y", errors="coerce")
        year_dates_quarters = year_dates.dt.quarter        
        #st.write(year_dates_quarters)
        
        
        extracted_quarter_index = sorted(year_dates_quarters.unique()) # Extraigo el trimestre de date_format. Date format ¿Ya viene con el año seleccionado?
        selected_quarter_index = st.selectbox("Seleccione Trimestre: ", extracted_quarter_index) # Extraigo los indices separados por cada unidad de indice. Este debe contener 4, por la cantidad de trimestres de un    

        quarter_condition = year_dates_quarters == selected_quarter_index

        quarter_df = years_data_frame[quarter_condition]

        st.write(quarter_df)

        
        #####################################################################
        #### FALTA EXPLICACIÓN A CADA LINEA
        #### FALTA FILTTRAR POR ESTAMENTO  
        
        


        
        
        
        
 
                            
        
        
        
        
        
        
        
    