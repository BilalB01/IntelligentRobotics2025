import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

def verbind_met_sphero(naam):
    toy = scanner.find_toy(toy_name=naam)
    if not toy:
        print("Geen Sphero gevonden.")
        exit(1)
    print(f"Verbonden met Sphero '{naam}'")
    return toy

def rij_segment(api, afstand_cm, heading, snelheid):
    api.set_heading(heading % 360)
    api.set_speed(snelheid)
    snelheid_mps = 1.3  # pas aan na testen
    duur = afstand_cm / 100 / snelheid_mps
    time.sleep(duur)
    api.set_speed(0)
    time.sleep(0.3)  # korte pauze na stoppen

def draai_heading(current_heading, graden):
    # graden positief = rechts draaien, negatief = links draaien
    new_heading = (current_heading + graden) % 360
    return new_heading

def main(naam):
    toy = verbind_met_sphero(naam)
    with SpheroEduAPI(toy) as api:
        print("Zet de Sphero met LED richting het startpaneel (0°), druk ENTER om te starten.")
        input()
        api.set_front_led(Color(0, 255, 0))
        api.set_heading(0)

        snelheid = 150
        heading = 0

        # Definieer het parcours als lijst van (aantal_stappen, draai_graden)
        # draai_graden = 0 betekent rechtdoor zonder draaien
        parcours = [
            (5, 90),   # 5x50cm rechtdoor +90° rechts
            (4, 90),   # 4x50cm rechtdoor +90° rechts
            (2, 90),   # 2x50cm rechtdoor +90° rechts
            (2, -90),  # 2x50cm rechtdoor -90° links
            (4, -90),  # 4x50cm rechtdoor -90° links
            (1.5, 90), # 1.5x50cm rechtdoor +90° rechts
            (2, 90),   # 2x50cm rechtdoor +90° rechts
            (4, 90),   # 4x50cm rechtdoor +90° rechts
            (4, 0)     # 4x50cm rechtdoor einde, geen draai
        ]

        print("Start autonome ronde!")
        starttijd = time.time()

        for stappen, draai in parcours:
            afstand = stappen * 50  # 50cm per stap
            rij_segment(api, afstand, heading, snelheid)
            heading = draai_heading(heading, draai)

        eindtijd = time.time()
        print(f"Ronde voltooid in {eindtijd - starttijd:.2f} seconden.")
        api.set_front_led(Color(255, 0, 0))  # rood einde

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Gebruik: python race.py <sphero_naam>")
        exit(1)
    main(sys.argv[1])
