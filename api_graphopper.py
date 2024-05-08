import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "68ffce78-0b2c-4198-ac85-d29e658cf76c"

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        region = json_data["hits"][0].get("state", "")
        country = json_data["hits"][0].get("country", "")

    else:
        print("Error al obtener la geolocalización. Por favor, inténtelo de nuevo.")
        lat = "null"
        lng = "null"
        name = "null"
        region = "null"
        country = "null"
    return json_status, name, region, country, lat, lng

def main():
    while True:
        print("\nMenú principal:")
        print("1. Obtener geolocalización")
        print("2. Calcular ruta")
        print("3. Salir")
        choice = input("Ingrese su elección: ")

        if choice == "1":
            location = input("Ingrese una ubicación: ")
            status, name, region, country, lat, lng = geocoding(location, key)
            if status == 200:
                print("Información de la ubicación:")
                print("------------------------------")
                print("Ciudad:", name)
                print("Región/Estado:", region)
                print("País:", country)
                print("Latitud:", lat)
                print("Longitud:", lng)
            else:
                print("Error al obtener la geolocalización. Por favor, inténtelo de nuevo.")

        elif choice == "2":
            loc1 = input("Ubicación Inicial: ")
            origen = geocoding(loc1, key)
            print(origen)
            loc2 = input("Ubicación Final: ")
            destino = geocoding(loc2, key)
            print(destino)

            if origen[0] == 200 and destino[0] == 200:
                op = "&point=" + str(origen[4]) + "%2C" + str(origen[5])
                dp = "&point=" + str(destino[4]) + "%2C" + str(destino[5])

                vehicle = input("Seleccione el modo de transporte (auto, bicicleta, pie): ").lower()
                if vehicle == "auto":
                    vehicle_param = "car"
                elif vehicle == "bicicleta":
                    vehicle_param = "bike"
                elif vehicle == "pie":
                    vehicle_param = "foot"
                else:
                    print("Modo de transporte inválido. Por favor, inténtelo de nuevo.")
                    continue

                caminos_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle_param}) + op + dp
                caminos_status = requests.get(caminos_url).status_code
                caminos_data = requests.get(caminos_url).json()
                print("El estado de la API " + str(caminos_status) + "\nCalculo de la ruta:\n" + caminos_url)

                if caminos_status == 200:
                    distancia_km = caminos_data['paths'][0]['distance'] / 1000  # Convertir a kilómetros
                    distancia_millas = distancia_km * 0.621371  # Convertir a millas
                    tiempo_segundos = caminos_data['paths'][0]['time'] / 1000  # Convertir a segundos
                    horas = int(tiempo_segundos // 3600)
                    minutos = int((tiempo_segundos % 3600) // 60)
                    segundos = int(tiempo_segundos % 60)
                    print(f"Distancia: {distancia_km:.2f} km ({distancia_millas:.2f} millas)")
                    print(f"Tiempo estimado: {horas:02d}:{minutos:02d}:{segundos:02d} (h:m:s)")
                else:
                    print("Error al calcular la ruta.")

                continue_input = input("¿Quieres continuar? (y/n): ")
                if continue_input.lower() != "y":
                    break

        elif choice == "3":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()