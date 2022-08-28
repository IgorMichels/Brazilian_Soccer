from scrape import *
import sys

if __name__ == '__main__':
    max_year = 2022
    competitions = [('CdB', '424'),
                    ('Serie_A', '142'),
                    ('Serie_B', '242'),
                    ('Serie_C', '342'),
                    ('Serie_D', '542')]
    if '-s' in sys.argv:
        make_directories(competitions, max_year)

        start_scrape = time()
        n = len(glob('*/*/CSVs/*.csv'))
        max_time = 120
        added = 0
        it = 1
        k = 0
        while n != k:
            files = glob('*/*/CSVs/*.csv')
            k = len(files)
            if it == 1:
                scrape(competitions, max_year, files, max_time)
            else:
                scrape(competitions, max_year, files, max_time / 2)
    
            n = len(glob('*/*/CSVs/*.csv'))
            added += n - k
            it += 1
        
        end_scrape = time()
        if added > 0 or '-e' in sys.argv:
            start_extract = time()
            cont_fail = extract(competitions, max_year)
            catch_squads(competitions, max_year)
            end_extract = time()
            clear()
            print(f'Scrape finalizado em {end_scrape - start_scrape:.2f} segundos!',
                  f'Extração finalizada em {end_extract - start_extract:.2f} segundos!',
                  f'{added} jogos foram adicionados a base.',
                  f'{cont_fail} jogos falharam ao extrair as informações.',
                  '-' * 58,
                  f'Tempo total: {end_extract - start_scrape:.2f} segundos.',
                  sep = '\n')
        else:
            clear()
            print(f'Scrape finalizado em {end_scrape - start_scrape:.2f} segundos!',
                  'Nenhum jogo foi adicionado a base.',
                  sep = '\n')
                  
    elif '-e' in sys.argv:
        start_extract = time()
        cont_fail = extract(competitions, max_year)
        catch_squads(competitions, max_year)
        end_extract = time()
        clear()
        print(f'Extração finalizada em {end_extract - start_extract:.2f} segundos!',
              f'{cont_fail} jogos falharam ao extrair as informações.',
              sep = '\n')
