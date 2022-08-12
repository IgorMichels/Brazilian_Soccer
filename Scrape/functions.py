import re

def treat_club(club):
    club = club.replace('Saf ', '')
    club = club.replace('S.a.f ', '')
    club = club.replace('S.A.F ', '')
    club = club.replace('Fc ', '')
    club = club.replace('FC ', '')
    club = club.replace('Futebol Clube ', '')
    club = club.replace('FUTEBOL CLUBE ', '')
    club = club.replace('F. C. ', '')
    club = club.replace('A.c. ', '')
    club = club.replace('Ltda ', '')
    club = club.replace('Associacao Desportiva ', '')
    club = club.replace('Esporte Clube ', '')
    club = club.replace('Sociedade Esportiva ', '')
    club = club.replace('-ap', '')
    club = club.replace('Sport Club ', '')
    club = club.replace('- Vn ', '')
    club = club.replace('- VN ', '')
    club = club.replace('Atletico', 'Atlético')
    club = club.replace('Vitoria', 'Vitória')
    club = club.replace('A.b.c. / RN', 'ABC / RN')
    club = club.replace('Abc / RN', 'ABC / RN')
    club = club.replace('AVAÍ / SC', 'Avaí / SC')
    club = club.replace('A.s.a. / AL', 'ASA / AL')
    club = club.replace('America / MG', 'América / MG')
    club = club.replace('América de Natal / RN', 'América / RN')
    club = club.replace('AMÉRICA / RN', 'América / RN')
    club = club.replace('Atlético / PR', 'Athletico Paranaense / PR')
    club = club.replace('ATLETICO / PR', 'Athletico Paranaense / PR')
    club = club.replace('Atlético / PR', 'Athletico Paranaense / PR')
    club = club.replace('Sobradinho (df) / DF', 'Sobradinho / DF')
    club = club.replace('ÁGUIA NEGRA / MS', 'Águia Negra / MS')
    club = club.replace('Aguia Negra / MS', 'Águia Negra / MS')
    club = club.replace('Aguia / PA', 'Águia de Marabá / PA')
    club = club.replace('Ypiranga Rs / RS', 'Ypiranga / RS')
    club = club.replace('Villa Nova A.c. / MG', 'Villa Nova / MG')
    club = club.replace('Veranopolis / RS', 'Veranópolis / RS')
    club = club.replace('União / MT', 'União de Rondonópolis / MT')
    club = club.replace('Ser Caxias / RS', 'Caxias / RS')
    club = club.replace('Sampaio Correa / MA', 'Sampaio Corrêa / MA')
    club = club.replace('SAMPAIO CORREA / MA', 'Sampaio Corrêa / MA')
    club = club.replace('SANTOS / SP', 'Santos / SP')
    club = club.replace('Bragantino / SP', 'Red Bull Bragantino / SP')
    club = club.replace('MURICI / AL', 'Murici / AL')
    club = club.replace('River / PI', 'Ríver / PI')
    club = club.replace('River A.c. / PI', 'Ríver / PI')
    club = club.replace('RÍVER / PI', 'Ríver / PI')
    club = club.replace('REAL NOROESTE / ES', 'Real Noroeste / ES')
    club = club.replace('Real Noroeste Capixaba / ES', 'Real Noroeste / ES')
    club = club.replace('PONTE PRETA / SP', 'Ponte Preta / SP')
    club = club.replace('PIAUÍ / PI', 'Piauí / PI')
    club = club.replace('Operario / PR', 'Operário / PR')
    club = club.replace('Luziania / DF', 'Luziânia / DF')
    club = club.replace('INDEPENDENTE / PA', 'Independente / PA')
    club = club.replace('Independente Tucuruí / PA', 'Independente / PA')
    club = club.replace('Guarany de Sobral / CE', 'Guarany / CE')
    club = club.replace('Guarani de Juazeiro / CE', 'Guarani / CE')
    club = club.replace('Crb / AL', 'CRB / AL')
    club = club.replace('Criciuma / SC', 'Criciúma / SC')
    club = club.replace('Csa / AL', 'CSA / AL')
    club = club.replace('FIGUEIRENSE / SC', 'Figueirense / SC')
    club = club.replace('FORTALEZA / CE', 'Fortaleza / CE')
    club = club.replace('C. R. B. / AL', 'CRB / AL')
    club = club.replace('C.r.a.c. / GO', 'CRAC / GO')
    club = club.replace('C.r.b. / AL', 'CRB / AL')
    club = club.replace('C.s.a. / AL', 'CSA / AL')
    club = club.replace('CAXIAS / RS', 'Caxias / RS')
    club = club.replace('CORITIBA / PR', 'Coritiba / PR')
    club = club.replace('CRICIÚMA / SC', 'Criciúma / SC')
    club = club.replace('Atlético Cearense / CE', 'Atlético / CE')
    club = club.replace('Atlético Roraima / RR', 'Atlético / RR')
    club = club.replace('BOTAFOGO / PB', 'Botafogo / PB')
    club = club.replace('BOTAFOGO / RJ', 'Botafogo / RJ')
    club = club.replace('Asa / AL', 'ASA / AL')
    club = club.replace('A.s.s.u. / RN', 'ASSU / RN')
    club = club.replace('Xv de Piracicaba / SP', 'XV de Piracicaba / SP')
    club = club.replace('Urt / MG', 'URT / MG')
    club = club.replace('Arapongas Esporte Clube / PR', 'Arapongas / PR')
    club = club.replace('Jacobina Ec / BA', 'Jacobina / BA')
    club = club.replace('Ge Juventus / SC', 'Juventus / SC')
    club = club.replace('TREZE / PB', 'Treze / PB')
    club = club.replace('S.francisco / PA', 'S. Francisco / PA')
    club = club.replace('Pstc / PR', 'PSTC / PR')
    club = club.replace('Prospera / SC', 'Próspera / SC')
    club = club.replace('Marilia / SP', 'Marília / SP')
    club = club.replace('Macae / RJ', 'Macaé / RJ')
    club = club.replace('Macapa / AP', 'Macapá / AP')
    club = club.replace('G.a.s / RR', 'G.A.S. / RR')
    club = club.replace('Cse / AL', 'CSE / AL')
    club = club.replace('Ca Patrocinense / MG', 'Atlético Patrocinense / MG')
    
    return club
    
def catch_teams(text):
    return re.findall('Jogo: (\D+ \/ [A-Z]{2}) X (\D+ \/ [A-Z]{2})', text)

def final_result(text):
    result = re.findall('Resultado\s*Final:\s*(\d+\s*[xX]\s*\d+)', text)
    if len(result) == 0:
        result = re.findall('Resultado\s*do\s*2º\s*Tempo:\s*(\d+\s*[xX]\s*\d+)', text)
    
    return result

def catch_players(text):
    club_1, club_2 = catch_teams(text)[0]
    club = club_1
    players = re.findall('(\d+\D+[P|A|)|T|R]\s*\d{6})', text)
    for i in range(len(players)):
        if i > 0 and 'T(g)' in players[i]:
            club = club_2
        
        players[i] = [players[i], club]
            
    return players

def catch_goals(text):
    result = final_result(text)
    if len(result) == 0: return []
    result = result[0].split()
    
    # tempo normal
    goals  = re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*NR[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*PN[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*CT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*FT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    
        # sem o número do jogador
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*NR[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*PN[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*CT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*FT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    
    # acréscimos
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*NR[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*PN[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*CT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*FT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    
        # sem o número do jogador
    goals += re.findall('\+\d+\s*\dT\s*NR[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\+\d+\s*\dT\s*PN[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\+\d+\s*\dT\s*CT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    goals += re.findall('\+\d+\s*\dT\s*FT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}', text)
    
    if len(goals) == int(result[0]) + int(result[-1]): return goals
    
    goals  = re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*NR[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*PN[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*CT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*\d+\s*FT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    
        # sem o número do jogador
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*NR[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*PN[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*CT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\d{2}:\d{2}\s*\dT\s*FT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    
    # acréscimos
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*NR[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*PN[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*CT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\+\d+\s*\dT\s*\d+\s*FT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    
        # sem o número do jogador
    goals += re.findall('\+\d+\s*\dT\s*NR[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\+\d+\s*\dT\s*PN[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\+\d+\s*\dT\s*CT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    goals += re.findall('\+\d+\s*\dT\s*FT[a-zA-ZÀ-ÿ\-\.\s]+', text)
    
    return goals
    
def find_changes(text):
    regex  = '\d{2}:\d{2}\s*\dT[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}\s*'
    regex += '\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\.\s]+\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\. ]+|'
    regex += '\d{2}:\d{2}\s*[a-zA-ZÀ-ÿ\-\.\s]+\/[A-Z]{2}\s*'
    regex += '\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\.\s]+\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\. ]+|'
    regex += '\d{2}:\d{2}\s*[a-zA-ZÀ-ÿ\-\.\s]+\s*'
    regex += '\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\.\s]+\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\. ]+|'
    regex += '\d{2}:\d{2}\s*\dT\s*[a-zA-ZÀ-ÿ\-\.\s]+\s*'
    regex += '\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\.\s]+\d+\s*\-\s*[a-zA-ZÀ-ÿ\-\. ]+'
    subs = re.findall(regex, text)
    
    return subs
