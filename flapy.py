import pygame
import random
import sys

pygame.init()

LEBAR, TINGGI = 400, 600
layar = pygame.display.set_mode((LEBAR, TINGGI))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font_besar = pygame.font.SysFont("arial", 48, bold=True)
font_kecil = pygame.font.SysFont("arial", 22)

GRAVITASI = 0.5
LONCAT = -8
LEBAR_PIPA = 70
CELAH = 160
KECEPATAN = 3
JARAK_PIPA = 220
TINGGI_TANAH = 60

LANGIT = (112, 197, 206)
HIJAU = (60, 180, 60)
HIJAU_TUA = (30, 120, 30)
TANAH = (222, 184, 135)


class Burung:
    def __init__(self):
        self.x = 80
        self.y = TINGGI // 2
        self.v = 0
        self.r = 15

    def loncat(self):
        self.v = LONCAT

    def update(self):
        self.v += GRAVITASI
        self.y += self.v

    def rect(self):
        return pygame.Rect(self.x - self.r, int(self.y) - self.r, self.r * 2, self.r * 2)

    def gambar(self):
        y = int(self.y)
        pygame.draw.circle(layar, (255, 220, 0), (self.x, y), self.r)
        pygame.draw.circle(layar, (255, 255, 255), (self.x + 6, y - 4), 5)
        pygame.draw.circle(layar, (0, 0, 0), (self.x + 8, y - 4), 2)
        pygame.draw.polygon(layar, (255, 120, 0), [(self.x + 12, y), (self.x + 24, y + 3), (self.x + 12, y + 6)])


class Pipa:
    def __init__(self, x):
        self.x = x
        self.tinggi_atas = random.randint(80, TINGGI - TINGGI_TANAH - CELAH - 80)
        self.lewat = False

    def update(self):
        self.x -= KECEPATAN

    def rect_atas(self):
        return pygame.Rect(self.x, 0, LEBAR_PIPA, self.tinggi_atas)

    def rect_bawah(self):
        y = self.tinggi_atas + CELAH
        return pygame.Rect(self.x, y, LEBAR_PIPA, TINGGI - TINGGI_TANAH - y)

    def gambar(self):
        for r in (self.rect_atas(), self.rect_bawah()):
            pygame.draw.rect(layar, HIJAU, r)
            pygame.draw.rect(layar, HIJAU_TUA, r, 3)


def teks_tengah(teks, font, warna, y):
    gambar = font.render(teks, True, warna)
    layar.blit(gambar, gambar.get_rect(center=(LEBAR // 2, y)))


def reset():
    return Burung(), [Pipa(LEBAR + 100), Pipa(LEBAR + 100 + JARAK_PIPA)], 0


burung, pipa_list, skor = reset()
mulai = False
mati = False
terbaik = 0

while True:
    tekan = False
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if e.key == pygame.K_SPACE:
                tekan = True
        if e.type == pygame.MOUSEBUTTONDOWN:
            tekan = True

    if tekan:
        if mati:
            burung, pipa_list, skor = reset()
            mati = False
            mulai = False
        else:
            mulai = True
            burung.loncat()

    if mulai and not mati:
        burung.update()
        for p in pipa_list:
            p.update()

        if pipa_list[0].x + LEBAR_PIPA < 0:
            pipa_list.pop(0)
            pipa_list.append(Pipa(pipa_list[-1].x + JARAK_PIPA))

        for p in pipa_list:
            if not p.lewat and p.x + LEBAR_PIPA < burung.x:
                p.lewat = True
                skor += 1
            if burung.rect().colliderect(p.rect_atas()) or burung.rect().colliderect(p.rect_bawah()):
                mati = True

        if burung.y + burung.r >= TINGGI - TINGGI_TANAH or burung.y - burung.r <= 0:
            mati = True

        if mati:
            terbaik = max(terbaik, skor)

    layar.fill(LANGIT)
    for p in pipa_list:
        p.gambar()
    pygame.draw.rect(layar, TANAH, (0, TINGGI - TINGGI_TANAH, LEBAR, TINGGI_TANAH))
    pygame.draw.line(layar, HIJAU, (0, TINGGI - TINGGI_TANAH), (LEBAR, TINGGI - TINGGI_TANAH), 5)
    burung.gambar()

    teks_tengah(str(skor), font_besar, (255, 255, 255), 60)

    if not mulai:
        teks_tengah("Tekan SPASI untuk mulai", font_kecil, (255, 255, 255), TINGGI // 2 + 70)
    if mati:
        teks_tengah("GAME OVER", font_besar, (220, 40, 40), TINGGI // 2 - 40)
        teks_tengah(f"Skor: {skor}   Terbaik: {terbaik}", font_kecil, (255, 255, 255), TINGGI // 2 + 10)
        teks_tengah("Tekan SPASI untuk main lagi", font_kecil, (255, 255, 255), TINGGI // 2 + 45)

    pygame.display.flip()
    clock.tick(60)
    