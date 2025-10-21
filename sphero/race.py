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

def rij_segment(api, afstand_cm, heading, snelheid_mps):
    api.set_heading(heading % 360)
    time.sleep(0.2) # Sphero tijd om te draaien
    api.set_speed(int(snelheid_mps * 100))
    duur = afstand_cm / 100 / snelheid_mps
    time.sleep(duur)
    api.set_speed(0)
    time.sleep(0.5) # iets langere pauze voor stabiliteit

def draai_heading(current_heading, graden):
    new_heading = (current_heading + graden) % 360
    return new_heading

def main(naam):
    toy = verbind_met_sphero(naam)
    with SpheroEduAPI(toy) as api:
        print("Zet de Sphero met LED richting het startpaneel (0°), druk ENTER om te starten.")
        input()
        api.set_front_led(Color(0, 255, 0))
        api.set_heading(0)

        snelheid_mps = 1.3  # realistische snelheid in meter/s
        heading = 0

        parcours = [
            {"afstand": 250, "draai": 90},    # 5x50cm rechtdoor +90°
            {"afstand": 200, "draai": 90},    # 4x50cm rechtdoor +90°
            {"afstand": 100, "draai": 90},    # 2x50cm rechtdoor +90°
            {"afstand": 100, "draai": -90},   # 2x50cm rechtdoor -90°
            {"afstand": 200, "draai": -90},   # 4x50cm rechtdoor -90°
            {"afstand": 75,  "draai": 90},    # 1.5x50cm rechtdoor +90°
            {"afstand": 100, "draai": 90},    # 2x50cm rechtdoor +90°
            {"afstand": 200, "draai": 90},    # 4x50cm rechtdoor +90°
            {"afstand": 200, "draai": 0}      # 4x50cm rechtdoor, geen draai
        ]

        print("Start autonome ronde!")
        starttijd = time.time()

        for segment in parcours:
            rij_segment(api, segment["afstand"], heading, snelheid_mps)
            heading = draai_heading(heading, segment["draai"])
            time.sleep(0.2)

        eindtijd = time.time()
        print(f"Ronde voltooid in {eindtijd - starttijd:.2f} seconden.")
        api.set_front_led(Color(255, 0, 0))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Gebruik: python race.py <sphero_naam>")
        exit(1)
    main(sys.argv[1])
