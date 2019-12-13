import pygame, sys, random

pygame.init()
ekraani_pind = pygame.display.set_mode( (800, 800) )
pygame.display.set_caption('Automäng')

# taust
tee = pygame.Rect(160,0,480,800) # x koordinaat, y koordinaat, laius, kõrgus
pidevjoon1 = pygame.Rect(318,0,4,800)
pidevjoon2 = pygame.Rect(478,0,4,800)

# taimer
võtab_aega = pygame.time.get_ticks() 
sekundid = (pygame.time.get_ticks()-võtab_aega) / 1000
taimeri_font = pygame.font.Font('Quicksand-VariableFont_wght.ttf', 40)
taimer_pildina = taimeri_font.render(str(sekundid), 1, [0,0,0])

auto = pygame.image.load('auto_lihtne.png') # mõõtmed 136x190
autovastu = pygame.image.load('auto_vastu.png')

#autode algpositsioonid
# mängija auto
x = 332
y = 580
#vasakpoolne rida, vastutulev auto
x1 = 172
y1 = -200
#parempoolne rida, vastutulev auto
x2 = 492
y2 = -200

#vastutulevate autode kiirus
kiirus = 4
       
auto_asukohad = [(172,520), (332,520), (492,520)]

#edetabel, mis salvestab parima aja
f = open('parim_aeg.txt')
parim_tulemus = float(f.read())
f.close()
parima_tulemuse_tekst = 'Parim: ' + str(parim_tulemus)
parima_font = pygame.font.Font('Quicksand-VariableFont_wght.ttf', 20)
parim_ekraanil = parima_font.render(parima_tulemuse_tekst, 1, [0,0,0])


#mängu põhiosa
main = True
while main == True:
    
    ekraani_pind.fill((0,255,0))
    pygame.draw.rect(ekraani_pind, (120,120,120), tee)
    pygame.draw.rect(ekraani_pind, (255,255,255), pidevjoon1)
    pygame.draw.rect(ekraani_pind, (255,255,255), pidevjoon2)
    ekraani_pind.blit(auto, (x, y)) # alustab keskmisel rajal
    ekraani_pind.blit(autovastu,(x1,y1))
    ekraani_pind.blit(autovastu,(x2,y2))
    taimer_pildina = taimeri_font.render(str(sekundid), 1, [0,0,0])
    ekraani_pind.blit(taimer_pildina, (30, 30))
    parim_ekraanil = parima_font.render(parima_tulemuse_tekst, 1, [0,0,0])
    ekraani_pind.blit(parim_ekraanil, (20, 100))
    pygame.display.flip()
    
    # taimer
    sekundid_uus = (pygame.time.get_ticks()-võtab_aega) / 1000
    sekundid = sekundid_uus
    
    # autod liiguvad suvaliselt
    if y1 < 800: # kui auto peab veel alla sõitma
        y1 += kiirus
    elif y1 >= 800: # kui auto on alla jõudnud
        x1 = auto_asukohad[random.randint(0,2)][0] # valib suvalise rea
        while x1 == x2: # kui real on juba auto, valib uue rea
            x1 = auto_asukohad[random.randint(0,2)][0]
        y1 = -200
        
    if y2 < 800: # kui auto peab veel alla sõitma
        y2 += kiirus
    elif y2 >= 800: # kui auto on alla jõudnud
        x2 = auto_asukohad[random.randint(0,2)][0] # valib suvalise rea
        while x2 == x1: # kui real on juba auto, valib uue rea
            x2 = auto_asukohad[random.randint(0,2)][0]
        y2 = -800
    
    #autod hakkavad kiiremini vastu tulema 
    if sekundid > 10:
        kiirus = 4.3
    if sekundid > 15:
        kiirus = 4.6
    if sekundid > 20:
       kiirus = 4.9
    if sekundid > 25:
       kiirus = 5.2
    if sekundid > 30:
       kiirus = 5.5
        
    #kui vastutulev auto sõidab otsa
    if (x1 == x and y1 >= 390 and y1 <= 710) or (x2 == x and y2 >= 390 and y2 <= 710): # kui ühe vastutuleva auto rida on sama punase auto omaga
        print('\nMäng läbi! Sinu aeg oli', sekundid, 'sekundit.')
        if sekundid >= parim_tulemus:
            print('See on siiani parim tulemus! Palju õnne!')
            f_uuesti = open('parim_aeg.txt', 'w')
            f_uuesti.write(str(sekundid)) # iga kord, kui tuleb uus parim aeg, kirjutab failis vana üle
            f_uuesti.close()
        else:
            print('Siiani parim tulemus on', str(parim_tulemus) + '. Proovi veel, kas sul õnnestub seda ületada.')
        main = False
    
    #auto liigutamine paremale-vasakule
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x > 172: # et ei sõidaks vasakult teelt välja
                    x -= 160
                    ekraani_pind.blit(auto, (x, y))
            if event.key == pygame.K_RIGHT:
                if x < 492: # et ei sõidaks paremalt teelt välja
                    x += 160
                    ekraani_pind.blit(auto, (x, y))     


pygame.quit()
