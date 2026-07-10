# importa_dadus.py
import os
import django
import csv
import sys

# Konfigura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naran_projetu.settings')  # TROKA HO NARAN PROJETU
django.setup()

from main.models import RegistuMenbroKmbo  # TROKA HO NARAN APLIKASAUN

def importa_csv(ficheiro_csv):
    """
    Importa dadus husi CSV ba database lokal
    """
    print("="*50)
    print(f"KOMESA IMPORTA DADUS HUSI: {ficheiro_csv}")
    print("="*50)
    
    # Verifika se ficheiro existe
    if not os.path.exists(ficheiro_csv):
        print(f"ERU: Ficheiro {ficheiro_csv} la hetan!")
        return
    
    sucessu = 0
    erru = 0
    linha_atual = 0
    
    with open(ficheiro_csv, 'r', encoding='utf-8') as file:
        # Lee CSV
        reader = csv.DictReader(file)
        
        # Hatudu koluna sira
        print(f"Koluna sira: {reader.fieldnames}")
        print("-"*50)
        
        # Prosesa linha ida-idak
        for linha in reader:
            linha_atual += 1
            
            try:
                # Limpa dadus
                telefone = linha.get('telefone', '')
                if telefone == '':
                    telefone = None
                    
                email = linha.get('email', '')
                if email == '':
                    email = None
                
                # Verifika se dadus importante iha
                if not linha['naran_kompletu'] or not linha['nomor_eleitoral_bi']:
                    print(f"⚠ Linha {linha_atual}: Naran ka nomor kartaun mamuk, skip...")
                    erru += 1
                    continue
                
                # Kria ka atualiza rejistu
                obj, kria = RegistuMenbroKmbo.objects.update_or_create(
                    nomor_eleitoral_bi=linha['nomor_eleitoral_bi'],
                    defaults={
                        'naran_kompletu': linha['naran_kompletu'],
                        'idade': linha['idade'],
                        'generu': linha['generu'],
                        'hela_fatin_atual': linha['hela_fatin_atual'],
                        'posto': linha['posto'],
                        'habilitasaun_literaria': linha['habilitasaun_literaria'],
                        'servisu_hanesan': linha['servisu_hanesan'],
                        'fatin_servisu': linha['fatin_servisu'],
                        'telefone': telefone,
                        'email': email,
                    }
                )
                
                if kria:
                    sucessu += 1
                    print(f"✓ {linha_atual}: Kria - {linha['naran_kompletu'][:30]}")
                else:
                    sucessu += 1
                    print(f"↻ {linha_atual}: Atualiza - {linha['naran_kompletu'][:30]}")
                    
            except Exception as e:
                erru += 1
                print(f"✗ {linha_atual}: Erru - {str(e)[:50]}")
    
    print("="*50)
    print(f"REMATA: {sucessu} sucessu, {erru} erru")
    print("="*50)

if __name__ == "__main__":
    # Se fornese argumentu, uja nia; se lae, uja dadus_kmbo.csv
    if len(sys.argv) > 1:
        ficheiro = sys.argv[1]
    else:
        ficheiro = "dadus_kmbo.csv"
    
    importa_csv(ficheiro)