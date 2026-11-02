
def clean_run():

    #run = str("13985742-9") Mio
    #run = str("16756562-K") Fernanda
    run = str("4959453-9")
    result_sum = 0
    index = 0
    
    series = [2,3,4,5,6,7]
    cleaned_run = ''.join(c for c in run if c.isdigit() or c == 'K' or c == 'k')
    
    body = cleaned_run[:-1]
    dv = cleaned_run[-1].lower()
    
    body_reversed = list(reversed(body)) 
    # 'reversed' devuelve un objeto iterable. A ese objeto iterable lo listo con 'list'.
    
    for body_factor in body_reversed: 
        body_factor = int(body_factor)

        serie_factor = series[index % len(series)]

        result_mult = serie_factor * body_factor
        result_sum = result_mult + result_sum

        index = index + 1 

    body_residual = result_sum % 11
    dv_result = 11 - body_residual

    if dv_result == 10:
        dv_result = 'k'
    elif dv_result == 11:
        dv_result = '0'
    
    if dv != str(dv_result):
        print(f"El dígito verificador {dv} es incorrecto, el resultado del cálculo es {dv_result}")
    else:
        print(f"El dígito verificador {dv} es correcto")


clean_run()

