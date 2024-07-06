class statistique:
    def __init__(self, PV, MP, DEX, CON, INT, SAG, CRO, CHA, PRE, MOV_speed, ATT_speed, ARM_magi, ARM_phys, PENE_phys, PENE_magi, ATK_phys, ATK_mag):
        self._PV = PV
        self._MP = MP
        self._DEX = DEX
        self._CON = CON
        self._INT = INT
        self._SAG = SAG
        self._CRO = CRO
        self._CHA = CHA
        self._PRE = PRE
        self._MOV_speed = MOV_speed
        self._ATT_speed = ATT_speed
        self._ARM_magi = ARM_magi
        self._ARM_phys = ARM_phys
        self._PENE_phys = PENE_phys
        self._PENE_magi = PENE_magi
        self._ATK_phys = ATK_phys
        self._ATK_mag = ATK_mag

    # Getters
    @property
    def PV(self):
        return self._PV

    @property
    def MP(self):
        return self._MP

    @property
    def DEX(self):
        return self._DEX

    @property
    def CON(self):
        return self._CON

    @property
    def INT(self):
        return self._INT

    @property
    def SAG(self):
        return self._SAG

    @property
    def CRO(self):
        return self._CRO

    @property
    def CHA(self):
        return self._CHA

    @property
    def PRE(self):
        return self._PRE

    @property
    def MOV_speed(self):
        return self._MOV_speed

    @property
    def ATT_speed(self):
        return self._ATT_speed

    @property
    def ARM_magi(self):
        return self._ARM_magi

    @property
    def ARM_phys(self):
        return self._ARM_phys

    @property
    def PENE_phys(self):
        return self._PENE_phys

    @property
    def PENE_magi(self):
        return self._PENE_magi

    @property
    def ATK_phys(self):
        return self._ATK_phys

    @property
    def ATK_mag(self):
        return self._ATK_mag

    # Setters
    @PV.setter
    def PV(self, value):
        self._PV = value

    @MP.setter
    def MP(self, value):
        self._MP = value

    @DEX.setter
    def DEX(self, value):
        self._DEX = value

    @CON.setter
    def CON(self, value):
        self._CON = value

    @INT.setter
    def INT(self, value):
        self._INT = value

    @SAG.setter
    def SAG(self, value):
        self._SAG = value

    @CRO.setter
    def CRO(self, value):
        self._CRO = value

    @CHA.setter
    def CHA(self, value):
        self._CHA = value

    @PRE.setter
    def PRE(self, value):
        self._PRE = value

    @MOV_speed.setter
    def MOV_speed(self, value):
        self._MOV_speed = value

    @ATT_speed.setter
    def ATT_speed(self, value):
        self._ATT_speed = value

    @ARM_magi.setter
    def ARM_magi(self, value):
        self._ARM_magi = value

    @ARM_phys.setter
    def ARM_phys(self, value):
        self._ARM_phys = value

    @PENE_phys.setter
    def PENE_phys(self, value):
        self._PENE_phys = value

    @PENE_magi.setter
    def PENE_magi(self, value):
        self._PENE_magi = value

    @ATK_phys.setter
    def ATK_phys(self, value):
        self._ATK_phys = value

    @ATK_mag.setter
    def ATK_mag(self, value):
        self._ATK_mag = value

    def __str__(self):
        return (f"PV: {self.PV}, MP: {self.MP}, DEX: {self.DEX}, CON: {self.CON}, INT: {self.INT}, "
                f"SAG: {self.SAG}, CRO: {self.CRO}, CHA: {self.CHA}, PRE: {self.PRE}, MOV_speed: {self.MOV_speed}, "
                f"ATT_speed: {self.ATT_speed}, ARM_magi: {self.ARM_magi}, ARM_phys: {self.ARM_phys}, "
                f"PENE_phys: {self.PENE_phys}, PENE_magi: {self.PENE_magi}, ATK_phys: {self.ATK_phys}, "
                f"ATK_mag: {self.ATK_mag}")
"""
# Exemple d'initialisation d'une instance de la classe Statistique
stats = statistique(
    PV=100, MP=50, DEX=15, CON=20, INT=25, SAG=18, CRO=10, CHA=12, PRE=14, MOV_speed=7,
    ATT_speed=1.5, ARM_magi=8, ARM_phys=10, PENE_phys=5, PENE_magi=4, ATK_phys=12, ATK_mag=14
)

print(stats)
"""
