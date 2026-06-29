import random
import string

MAYUSCULAS = string.ascii_uppercase
MINUSCULAS = string.ascii_lowercase
NUMEROS    = string.digits
SIMBOLOS   = "!@#$%^&*()_+-=[]{}|;:,.<>?"
VERSION    = 1

NIVELES_FORTALEZA = (
    "🔴 MUY DÉBIL",
    "🟠 DÉBIL",
    "🟡 MEDIA",
    "🟢 FUERTE",
    "💪 MUY FUERTE"
)

TIPOS_CARACTERES = ("Mayúsculas (A-Z)", "Minúsculas (a-z)", "Números (0-9)", "Símbolos (!@#$...)")

MAPA_CARACTERES = {
    "mayusculas": MAYUSCULAS,
    "minusculas": MINUSCULAS,
    "numeros":    NUMEROS,
    "simbolos":   SIMBOLOS
}

historial_sesion = {
    "total_generadas": 0,
    "fortalezas":      [],
    "longitudes":      []
}



def construir_pool(opciones):
    """Construye el conjunto de caracteres según las opciones elegidas."""
    pool = ""
    for clave, incluir in opciones.items():   
        if incluir:                            
            pool += MAPA_CARACTERES[clave]     
    return pool


def generar_contrasena(longitud, pool):
    """Genera una contraseña aleatoria a partir del pool dado."""
    contrasena = ""
    for _ in range(longitud):          
        contrasena += random.choice(pool)
    return contrasena


def evaluar_fortaleza(longitud, num_tipos):
    """Evalúa la fortaleza usando la tupla NIVELES_FORTALEZA."""
    
    if longitud >= 16 and num_tipos == 4:
        indice = 4
    elif longitud >= 12 and num_tipos >= 3:
        indice = 3
    elif longitud >= 10 and num_tipos >= 2:
        indice = 2
    elif longitud >= 8:
        indice = 1
    else:
        indice = 0
    return NIVELES_FORTALEZA[indice]   


def pedir_si_no(mensaje):
    """Pide al usuario una respuesta s/n."""
    while True:                        # UNIDAD 3: while
        respuesta = input(mensaje + " (s/n): ").strip().lower()
        if respuesta == "s":           # UNIDAD 3: if / elif / else
            return True
        elif respuesta == "n":
            return False
        else:
            print("  ⚠ Escribe 's' para sí o 'n' para no.")


def pedir_entero(mensaje, minimo, maximo):
    """Pide un número entero dentro de un rango."""
    while True:                        
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:   
                return valor
            else:
                print(f"  ⚠ Debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("  ⚠ Ingresa un número válido.")


def configurar_opciones():
    """Solicita las opciones de generación al usuario."""
    print("\n📋 CONFIGURACIÓN DE LA CONTRASEÑA\n")
    longitud = pedir_entero("  Longitud de la contraseña (8-64): ", 8, 64)
    cantidad = pedir_entero("  ¿Cuántas contraseñas deseas generar? (1-10): ", 1, 10)

    print()
    print("  Tipos de caracteres disponibles:")
    for i, tipo in enumerate(TIPOS_CARACTERES):   
        print(f"    {i+1}. {tipo}")

    print()
    opciones = {
        "mayusculas": pedir_si_no("  ¿Incluir Mayúsculas? (A-Z)"),
        "minusculas": pedir_si_no("  ¿Incluir minúsculas? (a-z)"),
        "numeros":    pedir_si_no("  ¿Incluir Números?    (0-9)"),
        "simbolos":   pedir_si_no("  ¿Incluir Símbolos?   (!@#$...)")
    }
    return longitud, cantidad, opciones


def mostrar_resultados(contrasenas, fortaleza, longitud):
    """Muestra la lista de contraseñas generadas y la fortaleza."""
    print("\n" + "-" * 55)
    print("  ✅ CONTRASEÑAS GENERADAS")
    print("-" * 55)
    for i, c in enumerate(contrasenas, 1):   
        print(f"  {i}. {c}")
    print("-" * 55)
    print(f"  Fortaleza estimada: {fortaleza}")
    print("-" * 55)

  
    historial_sesion["total_generadas"] += len(contrasenas)
    historial_sesion["fortalezas"].append(fortaleza)
    historial_sesion["longitudes"].append(longitud)


def mostrar_historial():
    """Muestra el resumen de la sesión desde el diccionario historial."""
    print("\n" + "=" * 55)
    print("  📊 RESUMEN DE LA SESIÓN")
    print("=" * 55)
    print(f"  Total contraseñas generadas : {historial_sesion['total_generadas']}")
    print(f"  Longitudes usadas           : {historial_sesion['longitudes']}")
    print("  Fortalezas obtenidas:")
    for f in historial_sesion["fortalezas"]:   
        print(f"    → {f}")
    print("=" * 55)


def mostrar_bienvenida():
    """Muestra el encabezado del programa."""
    print("\n" + "=" * 55)
    print(f"   🔐  GENERADOR SEGURO DE CONTRASEÑAS v{VERSION}  🔐")
    print("=" * 55)
    print("  Protege tu identidad digital con contraseñas")
    print("  seguras y personalizadas.")
    print("=" * 55)


def menu_principal():
    """Función principal: controla el flujo completo del programa."""
    mostrar_bienvenida()

    continuar = True
    while continuar:                       

        longitud, cantidad, opciones = configurar_opciones()
        pool = construir_pool(opciones)

        if not pool:                        
            print("\n  ⚠ Debes seleccionar al menos un tipo de carácter.\n")
            continue                       

        contrasenas = []
        for _ in range(cantidad):           
            nueva = generar_contrasena(longitud, pool)
            contrasenas.append(nueva)       

        num_tipos = sum(1 for v in opciones.values() if v)
        fortaleza = evaluar_fortaleza(longitud, num_tipos)
        mostrar_resultados(contrasenas, fortaleza, longitud)

        continuar = pedir_si_no("\n  ¿Deseas generar más contraseñas?")
        if not continuar:                   
            break                           

    mostrar_historial()
    print("\n  👋 ¡Hasta luego! Usa contraseñas únicas para cada cuenta.\n")


if __name__ == "__main__":
    menu_principal()