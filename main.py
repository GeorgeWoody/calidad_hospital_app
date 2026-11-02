import streamlit as st
import pandas as pd

from normalization import (normalize_headers, normalize_timestamps_marca_temporal,
                           normalize_timestamps_fecha_supervision, priority_columns,
                           clean_run, normalize_staff, normalize_units, clean_initials)
from config import headers_normalization, priority, rest, staff, units

st.set_page_config(layout="wide")
st.title("Calidad App - Hospital Mario Sánchez")

uploaded_file = st.file_uploader("Sube tu Excel", type="xlsx")

def load_sheet(uploaded_file, sheet):
    """Lee y normaliza una hoja antes de aplicar los filtros."""
    df = pd.read_excel(uploaded_file, sheet_name=sheet).fillna("")
    df.columns = df.columns.astype(str).str.strip().str.lower()
    df = normalize_headers(df, headers_normalization)
    df = normalize_timestamps_marca_temporal(df)
    df = normalize_timestamps_fecha_supervision(df)
    for column in ("RUT Funcionario", "RUT Paciente"):
        if column in df.columns:
            df[column] = df[column].apply(clean_run)
    if "Estamento Del Supervisado" in df.columns:
        df = normalize_staff(df, staff)
    df = normalize_units(df, units)
    if "Iniciales Del Supervisor/a" in df.columns:
        df["Iniciales Del Supervisor/a"] = df["Iniciales Del Supervisor/a"].apply(clean_initials)
    columns = priority_columns(df, priority, rest)
    return df[columns]

def apply_filter(df, column, selected):
    """Aplica un filtro multiselección; una selección vacía significa todos."""
    if column and selected:
        return df[df[column].isin(selected)]
    return df

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet = st.selectbox("Selecciona la hoja", xls.sheet_names)
    df = load_sheet(xls, sheet)
    st.write(f"Registros cargados: {len(df)}")
    filtered_df = df

    unit_column = next((c for c in ("Unidad/Servicio Del Supervisado",
                                    "Unidad/Servicio Supervisado") if c in df.columns), None)
    if unit_column:
        values = sorted(v for v in df[unit_column].unique() if str(v).strip())
        selected = st.multiselect("Filtrar por unidad", values)
        filtered_df = apply_filter(filtered_df, unit_column, selected)

    date_column = "Fecha De Supervisión" if "Fecha De Supervisión" in df.columns else None
    if date_column:
        dates = pd.to_datetime(filtered_df[date_column], dayfirst=True, errors="coerce")
        years = sorted(dates.dt.year.dropna().astype(int).unique())
        selected_years = st.multiselect("Filtrar por año", years)
        if selected_years:
            filtered_df = filtered_df[pd.to_datetime(
                filtered_df[date_column], dayfirst=True, errors="coerce"
            ).dt.year.isin(selected_years)]

        dates = pd.to_datetime(filtered_df[date_column], dayfirst=True, errors="coerce")
        quarters = sorted(dates.dt.quarter.dropna().astype(int).unique())
        selected_quarters = st.multiselect("Filtrar por trimestre", quarters,
                                           format_func=lambda q: f"{q}° trimestre")
        if selected_quarters:
            filtered_df = filtered_df[pd.to_datetime(
                filtered_df[date_column], dayfirst=True, errors="coerce"
            ).dt.quarter.isin(selected_quarters)]

    if "Estamento Del Supervisado" in df.columns:
        values = sorted(v for v in filtered_df["Estamento Del Supervisado"].unique()
                        if str(v).strip())
        selected = st.multiselect("Filtrar por estamento", values)
        filtered_df = apply_filter(filtered_df, "Estamento Del Supervisado", selected)

    total = len(filtered_df)
    cumplen = int((filtered_df["Resultado"] == "Cumple").sum())
    no_cumplen = total - cumplen
    porcentaje = (cumplen / total * 100) if total else 0
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total supervisados", total)
    col2.metric("Cumplen", cumplen)
    col3.metric("No cumplen", no_cumplen)
    col4.metric("Cumplimiento", f"{porcentaje:.0f}%")

    st.subheader("Resultado filtrado")
    st.dataframe(filtered_df, use_container_width=True)
