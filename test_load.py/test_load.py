from utils.csv_data_loader import CsvDataLoader

if __name__ == "__main__":
    print("Iniciando prueba de carga...")
    loader = CsvDataLoader()
    
    for i, row in enumerate(loader.read(), start=1):
        if i > 3:
            break
        print(f"Transacción {i}:", row)