from datetime import datetime
from scrape import *
import sys

if __name__ == '__main__':
    scraping = False
    if scraping:
        now = datetime.now()
        if now.strftime('%d') == '01':
            min_year = 2013
        else:
            min_year = int(now.strftime('%Y'))
    
        max_year = int(now.strftime('%Y'))
        competitions = [('CdB', '424'),
                        ('Serie_A', '142'),
                        ('Serie_B', '242'),
                        ('Serie_C', '342'),
                        ('Serie_D', '542')]
                    
        if '-a' in sys.argv:
            cleaning = False
        else:
            cleaning = True
    
        if '-s' in sys.argv or len(sys.argv) == 1:
            make_directories(competitions, min_year, max_year)

            with open('scrape.log', 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Scraping]   - Iniciando extração das súmulas.\n')
        
            start_scrape = time()
            n = len(glob('*/*/CSVs/*.csv'))
            max_time = 30
            added = 0
            it = 1
            k = 0
            while n != k:
                files = glob('*/*/CSVs/*.csv')
                k = len(files)
                if it == 1:
                    scrape(competitions, min_year, max_year, files, max_time, cleaning = cleaning)
                else:
                    scrape(competitions, min_year, max_year, files, max_time / 2, cleaning = cleaning)
    
                n = len(glob('*/*/CSVs/*.csv'))
                added += n - k
                it += 1
        
            end_scrape = time()
            with open('scrape.log', 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Scraping]   - Finalizada extração das súmulas.\n')
                if added == 0:
                    f.write('                                   [INFO] Nenhuma súmula foi adicionada.\n')
                elif added == 1:
                    f.write('                                   [INFO] 1 súmula foi adicionada.\n')
                else:
                    f.write(f'                                   [INFO] {added} súmulas foram adicionadas.\n')
            
            if added > 0 or '-e' in sys.argv:
                start_extract = time()
                with open('scrape.log', 'a') as f:
                    f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Extração]   - Iniciada extração das informações.\n')
            
                cont_fail = extract(competitions, min_year, max_year, cleaning = cleaning)
                with open('scrape.log', 'a') as f:
                    f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Extração]   - Finalizada extração das informações.\n')
                    if cont_fail == 1:
                        f.write('                                   [INFO] 1 jogo falhou ao ser extraído.\n')
                    elif cont_fail > 0:
                        f.write(f'                                   [INFO] {cont_fail} jogos falharam ao serem extraídos.\n')
                    else:
                        f.write('                                   [INFO] Todos os jogos foram extraídos com sucesso!\n')
                    
                    f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Escalações] - Iniciada geração das escalações.\n')
                
                catch_squads(competitions, min_year, max_year, cleaning = cleaning)
                with open('scrape.log', 'a') as f:
                    f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Escalações] - Finalizada geração das escalações.\n')
                
                end_extract = time()
                if cleaning: clear()
                print(f'Scrape finalizado em {end_scrape - start_scrape:.2f} segundos!',
                      f'Extração finalizada em {end_extract - start_extract:.2f} segundos!',
                      f'{added} jogos foram adicionados a base.',
                      f'{cont_fail} jogos falharam ao extrair as informações.',
                      '-' * 58,
                      f'Tempo total: {end_extract - start_scrape:.2f} segundos.',
                      sep = '\n')
            else:
                if cleaning: clear()
                print(f'Scrape finalizado em {end_scrape - start_scrape:.2f} segundos!',
                      'Nenhum jogo foi adicionado a base.',
                      sep = '\n')
                  
        elif '-e' in sys.argv:
            start_extract = time()
            with open('scrape.log', 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Extração]   - Iniciada extração das informações.\n')
        
            cont_fail = extract(competitions, min_year, max_year, cleaning = cleaning)
            with open('scrape.log', 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Extração]   - Finalizada extração das informações.\n')
                if cont_fail == 1:
                    f.write('                                   [INFO] 1 jogo falhou ao ser extraído.\n')
                elif cont_fail > 0:
                    f.write(f'                                   [INFO] {cont_fail} jogos falharam ao serem extraídos.\n')
                else:
                    f.write('                                   [INFO] Todos os jogos foram extraídos com sucesso!\n')
                
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Escalações] - Iniciada geração das escalações.\n')
        
            catch_squads(competitions, min_year, max_year, cleaning = cleaning)
            with open('scrape.log', 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [Escalações] - Finalizada geração das escalações.\n')
                
            end_extract = time()
            if cleaning: clear()
            print(f'Extração finalizada em {end_extract - start_extract:.2f} segundos!',
                  f'{cont_fail} jogos falharam ao extrair as informações.',
                  sep = '\n')
              
        with open('scrape.log', 'a') as f:
            f.write('\n')
            f.write('-' * 85 + '\n')
            f.write('\n')
    else:
        with open('scrape.log', 'a') as f:
            f.write('Scraping desabilitado.')
            f.write('\n')
            f.write('-' * 85 + '\n')
            f.write('\n')
