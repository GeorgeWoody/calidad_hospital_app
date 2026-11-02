import streamlit as st
import pandas as pd

priority =  ['Fecha De Registro'
            ,'Hora De Registro',
            'Fecha De Supervisión',
            'RUT Funcionario',
            'RUT Paciente',
            'Unidad/Servicio Del Supervisado',
            'Unidad/Servicio Supervisado',
            'Lugar Supervisado',
            'Estamento Del Supervisado',
            "Indicación Médica de CUP Es Congruente Con Criterios Locales De Indicación (Monitoreo Hemodinámico, Post Cirugía Urológica, Retención Aguda De Orina)",
            "Iniciales Del Supervisor/a"
]

rest = []

headers_normalization = {
                "fecha de supervisión":"Fecha De Supervisión",
                "fecha de supervision":"Fecha De Supervisión",
                "fecha supervisión":"Fecha De Supervisión",
                "fecha supervision":"Fecha De Supervisión", 

                "run supervisado (sin puntos, con guion)":"RUT Funcionario",
                "run supervisado":"RUT Funcionario",
                "run del supervisado":"RUT Funcionario",
                "run paciente":"RUT Paciente",
                "rut paciente":"RUT Paciente",

                "unidad o servicio del supervisado":"Unidad/Servicio Del Supervisado",
                "unidad supervisada":"Unidad/Servicio Supervisado",
                "unidad o servicio supervisado":"Unidad/Servicio Supervisado" ,

                "estamento del supervisado":"Estamento Del Supervisado",
                "estamento supervisado":"Estamento Del Supervisado",
                
                "lugar supervisado":"Lugar Supervisado",

                "habitación supervisada": "Habitación Supervisada",
                "habitación supervisado": "Habitación Supervisada",

                "mecanismo de transmisión":"Mecanismo De Transmisión",
                "mecanismo transmisión":"Mecanismo De Transmisión",
                "mecanismo de transmision":"Mecanismo De Transmisión",
                "mecanismo transmisión":"Mecanismo De Transmisión",

                "nombre del paciente":"Nombre Del Paciente",
                "nombre paciente":"Nombre Del Paciente",

                "fecha de instalación":"Fecha De Instalación",
                "fecha instalación":"Fecha De Instalación",
                "fecha de instalacion":"Fecha De Instalación",
                "fecha instalacion":"Fecha De Instalación",

                "indicacion médica de cup escrita en ficha clinica":"Indicación Médica De 'CUP' (Escrita En Ficha Clínica)",
                "indicación médica de cup es congruente con los criterios  locales de indicacion (monitoreo hemodinamico, post cirugia urologica, retencion aguda de orina)":"Indicación Médica de CUP Es Congruente Con Criterios Locales De Indicación (Monitoreo Hemodinámico, Post Cirugía Urológica, Retención Aguda De Orina)",            

                "número de autoclave en supervisión": "Número De AutoClave En Supervisión",
                "numero de autoclave en supervision": "Número De AutoClave En Supervisión",
                "número de autoclave en supervision": "Número De AutoClave En Supervisión",
                "numero de autoclave en supervisión": "Número De AutoClave En Supervisión",

                "iniciales del supervisor":"Iniciales Del Supervisor/a",
                "iniciales de supervisor":"Iniciales Del Supervisor/a",
                "iniciales de supervisora":"Iniciales Del Supervisor/a",
                "iniciales supervisor":"Iniciales Del Supervisor/a",
                "iniciales supervisora":"Iniciales Del Supervisor/a",
                
} 

staff = {

        "administrativo":"Administrativo",

        "asistente dental":"Asistente Dental",

        "auxiliar de alimentación":"Auxiliar De Alimentación",
        "auxiliar de alimentacion":"Auxiliar De Alimentación",

        "auxiliar de servicio":"Auxiliar De Servicio",
        
        "conductor ambulancia":"Conductor De Ambulancia",
        "conductor de ambulancia":"Conductor De Ambulancia",
        "chofer ambulancia":"Conductor De Ambulancia",
        "chofer de ambulancia":"Conductor De Ambulancia",
        
        "enfermer@":"Enfermero/Enfermera",
        "enfermero":"Enfermero/Enfermera",
        "enfermera":"Enfermero/Enfermera",

        "fonoaudiologo":"Fonoaudiólogo/Fonoaudióloga",
        "fonoaudiologa":"Fonoaudiólogo/Fonoaudióloga",
        "fonoaudiolog@":"Fonoaudiólogo/Fonoaudióloga",
        "fonoaudiólogo":"Fonoaudiólogo/Fonoaudióloga",
        "fonoaudióloga":"Fonoaudiólogo/Fonoaudióloga",
        "fonoaudiólog@":"Fonoaudiólogo/Fonoaudióloga",

        "kinesiólogo":"Kinesiólogo/Kinesióloga",
        "kinesióloga":"Kinesiólogo/Kinesióloga",
        "kinesiologo":"Kinesiólogo/Kinesióloga",
        "kinesiologa":"Kinesiólogo/Kinesióloga",
        "kinesiólog@":"Kinesiólogo/Kinesióloga",
        "kinesiolog@":"Kinesiólogo/Kinesióloga",

        "martron/a":"Matrón/Matrona",
        "matrón/a":"Matrón/Matrona",
        "matron/a":"Matrón/Matrona",
        "matrón":"Matrón/Matrona",
        "matrona":"Matrón/Matrona",
        "matron":"Matrón/Matrona",
        
        "médico":"Médico/Médica",
        "medico":"Médico/Médica",
        "médica":"Médico/Médica",
        "medica":"Médico/Médica",
        "médic@":"Médico/Médica",
        "medic@":"Médico/Médica",
        
        "médico odontólogo":"Médico Odontólogo/Odontóloga",
        "médico odontologo":"Médico Odontólogo/Odontóloga",
        "medico odontólogo":"Médico Odontólogo/Odontóloga",
        "médica odontóloga":"Médico Odontólogo/Odontóloga",
        "médica odontologa":"Médico Odontólogo/Odontóloga",
        "medica odontóloga":"Médico Odontólogo/Odontóloga",

        "odontólogo":"Odontólogo/Odontóloga",
        "odontologo":"Odontólogo/Odontóloga",
        "odontóloga":"Odontólogo/Odontóloga",
        "odontologa":"Odontólogo/Odontóloga",
        "odontolog@":"Odontólogo/Odontóloga",

        "nutricionista":"Nutricionista",
    
        "tens":"TENS",

        "trabajador social":"Trabajador/Trabajadora Social",
        "trabajadora social":"Trabajador/Trabajadora Social",
}

units = {
        "unidad de emergencia": "Emergencia",
        "unidad emergencia": "Emergencia",
        "emergencia": "Emergencia",
        "pabellon": "Pabellón",
        "pabellón": "Pabellón",
        "pabellon / esterilizacion": "Pabellón/Esterilización",
        "pabellón / esterilización": "Pabellón/Esterilización",
        "pabellon/esterilizacion": "Pabellón/Esterilización",
        "pabellón/esterilización": "Pabellón/Esterilización",
        "maternidad": "Maternidad",
        "policlinico": "Policlínico",
        "policlínico": "Policlínico",
        "dental": "Dental",
        "medicina": "Médico-Quirúrgico",
        "alimentacion": "Alimentación",
        "alimentación": "Alimentación",
        "esterilizacion": "Esterilización",
        "esterilización": "Esterilización",
        "servicios generales": "Servicios Generales",
        "box de atencion": "BOX De Atención",
        "box de atención": "BOX De Atención",
}

answers = {
            "si":"Si",
            "no":"No"
}
