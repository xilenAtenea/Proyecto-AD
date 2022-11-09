def popup_html(d):

    link_apto= d['link']
    price= d[' precio']
    numero_h= d[' cant_habitaciones']
    id_apart = d[' id_apto']




    html= """<!DOCTYPE html>
        <html>
            <body>
                <a href=""" + link_apto + """> Ir a FincaRaiz </a><br />
                <span> $""" + str(price) + """ </span><br />
                <span> <strong> No. Habitaciones: </strong>""" + str(numero_h)+"""</span> <br />
                <a href="/aptos/formulario/""" + str(id_apart)+"""" target="_top">
                    <input type="button" value="POSTULARME" />
                </a>
            </body>
        </html>
    
    """

    return html