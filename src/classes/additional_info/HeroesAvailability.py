class HeroesAvailability:

    # alternative no-argument constructor
    @classmethod
    def create_default(cls):
        return cls(
            orrin= True,
            valeska= True,
            edric= True,
            sylvia= True,
            lord_haart= False,
            sorsha= True,
            christian= True,
            tyris= True,
            rion= True,
            adela= True,
            cuthbert= True,
            adelaide= True,
            ingham= True,
            sanya= True,
            loynis= True,
            caitlin= True,
            mephala= True,
            ufretin= True,
            jenova= True,
            ryland= True,
            thorgrim= True,
            ivor= True,
            clancy= True,
            kyrre= True,
            coronius= True,
            uland= True,
            elleshar= True,
            gem= True,
            malcom= True,
            melodia= True,
            alagar= True,
            aeris= True,
            piquedram= True,
            thane= True,
            josephine= True,
            neela= True,
            torosar= True,
            fafner= True,
            rissa= True,
            iona= True,
            astral= True,
            halon= True,
            serena= True,
            daremyth= True,
            theodorus= True,
            solmyr= True,
            cyra= True,
            aine= True,
            fiona= True,
            rashka= True,
            marius= True,
            ignatius= True,
            octavia= True,
            calh= True,
            pyre= True,
            nymus= True,
            ayden= True,
            xyron= True,
            axsis= True,
            olema= True,
            calid= True,
            ash= True,
            zydar= True,
            xarfax= True,
            straker= True,
            vokial= True,
            moandor= True,
            charna= True,
            tamika= True,
            isra= True,
            clavius= True,
            galthran= True,
            septienna= True,
            aislinn= True,
            sandro= True,
            nimbus= True,
            thant= True,
            xsi= True,
            vidomina= True,
            nagash= True,
            lorelei= True,
            arlach= True,
            dace= True,
            ajit= True,
            damacon= True,
            gunnar= True,
            synca= True,
            shakti= True,
            alamar= True,
            jaegar= True,
            malekith= True,
            jeddite= True,
            geon= True,
            deemer= True,
            sephinroth= True,
            darkstorm= True,
            yog= True,
            gurnisson= True,
            jabarkas= True,
            shiva= True,
            gretchin= True,
            krellion= True,
            crag_hack= True,
            tyraxor= True,
            gird= True,
            vey= True,
            dessa= True,
            terek= True,
            zubin= True,
            gundula= True,
            oris= True,
            saurug= True,
            bron= True,
            drakon= True,
            wystan= True,
            tazar= True,
            alkin= True,
            korbac= True,
            gerwulf= True,
            broghild= True,
            mirlanda= True,
            rosic= True,
            voy= True,
            verdish= True,
            merist= True,
            styg= True,
            andra= True,
            tiva= True,
            pasis= True,
            thunar= True,
            ignissa= True,
            lacus= True,
            monere= True,
            erdamon= True,
            fiur= True,
            kalt= True,
            luna= True,
            brissa= True,
            ciele= True,
            labetha= True,
            inteus= True,
            aenain= True,
            gelare= True,
            grindan= True,
            sir_mullich= True,
            adrienne= False,
            catherine= False,
            dracon= False,
            gelu= False,
            kilgor= False,
            haart_lich= False,
            mutare= False,
            roland= False,
            mutare_drake= False,
            boragus= False,
            xeron= False,
            padding_156= False,
            padding_157= False,
            padding_158= False,
            padding_159= False
        )

    def __init__(
        self,
        orrin: bool, valeska: bool, edric: bool, sylvia: bool, lord_haart: bool,
        sorsha: bool, christian: bool, tyris: bool, rion: bool, adela: bool,
        cuthbert: bool, adelaide: bool, ingham: bool, sanya: bool, loynis: bool,
        caitlin: bool, mephala: bool, ufretin: bool, jenova: bool, ryland: bool,
        thorgrim: bool, ivor: bool, clancy: bool, kyrre: bool, coronius: bool,
        uland: bool, elleshar: bool, gem: bool, malcom: bool, melodia: bool,
        alagar: bool, aeris: bool, piquedram: bool, thane: bool, josephine: bool,
        neela: bool, torosar: bool, fafner: bool, rissa: bool, iona: bool,
        astral: bool, halon: bool, serena: bool, daremyth: bool, theodorus: bool,
        solmyr: bool, cyra: bool, aine: bool, fiona: bool, rashka: bool,
        marius: bool, ignatius: bool, octavia: bool, calh: bool, pyre: bool,
        nymus: bool, ayden: bool, xyron: bool, axsis: bool, olema: bool,
        calid: bool, ash: bool, zydar: bool, xarfax: bool, straker: bool,
        vokial: bool, moandor: bool, charna: bool, tamika: bool, isra: bool,
        clavius: bool, galthran: bool, septienna: bool, aislinn: bool, sandro: bool,
        nimbus: bool, thant: bool, xsi: bool, vidomina: bool, nagash: bool,
        lorelei: bool, arlach: bool, dace: bool, ajit: bool, damacon: bool,
        gunnar: bool, synca: bool, shakti: bool, alamar: bool, jaegar: bool,
        malekith: bool, jeddite: bool, geon: bool, deemer: bool, sephinroth: bool,
        darkstorm: bool, yog: bool, gurnisson: bool, jabarkas: bool, shiva: bool,
        gretchin: bool, krellion: bool, crag_hack: bool, tyraxor: bool, gird: bool,
        vey: bool, dessa: bool, terek: bool, zubin: bool, gundula: bool,
        oris: bool, saurug: bool, bron: bool, drakon: bool, wystan: bool,
        tazar: bool, alkin: bool, korbac: bool, gerwulf: bool, broghild: bool,
        mirlanda: bool, rosic: bool, voy: bool, verdish: bool, merist: bool,
        styg: bool, andra: bool, tiva: bool, pasis: bool, thunar: bool,
        ignissa: bool, lacus: bool, monere: bool, erdamon: bool, fiur: bool,
        kalt: bool, luna: bool, brissa: bool, ciele: bool, labetha: bool,
        inteus: bool, aenain: bool, gelare: bool, grindan: bool, sir_mullich: bool,
        adrienne: bool, catherine: bool, dracon: bool, gelu: bool, kilgor: bool,
        haart_lich: bool, mutare: bool, roland: bool, mutare_drake: bool, boragus: bool,
        xeron: bool, padding_156: bool, padding_157: bool, padding_158: bool, padding_159: bool
    ):
        self.orrin = orrin
        self.valeska = valeska
        self.edric = edric
        self.sylvia = sylvia
        self.lord_haart = lord_haart
        self.sorsha = sorsha
        self.christian = christian
        self.tyris = tyris
        self.rion = rion
        self.adela = adela
        self.cuthbert = cuthbert
        self.adelaide = adelaide
        self.ingham = ingham
        self.sanya = sanya
        self.loynis = loynis
        self.caitlin = caitlin
        self.mephala = mephala
        self.ufretin = ufretin
        self.jenova = jenova
        self.ryland = ryland
        self.thorgrim = thorgrim
        self.ivor = ivor
        self.clancy = clancy
        self.kyrre = kyrre
        self.coronius = coronius
        self.uland = uland
        self.elleshar = elleshar
        self.gem = gem
        self.malcom = malcom
        self.melodia = melodia
        self.alagar = alagar
        self.aeris = aeris
        self.piquedram = piquedram
        self.thane = thane
        self.josephine = josephine
        self.neela = neela
        self.torosar = torosar
        self.fafner = fafner
        self.rissa = rissa
        self.iona = iona
        self.astral = astral
        self.halon = halon
        self.serena = serena
        self.daremyth = daremyth
        self.theodorus = theodorus
        self.solmyr = solmyr
        self.cyra = cyra
        self.aine = aine
        self.fiona = fiona
        self.rashka = rashka
        self.marius = marius
        self.ignatius = ignatius
        self.octavia = octavia
        self.calh = calh
        self.pyre = pyre
        self.nymus = nymus
        self.ayden = ayden
        self.xyron = xyron
        self.axsis = axsis
        self.olema = olema
        self.calid = calid
        self.ash = ash
        self.zydar = zydar
        self.xarfax = xarfax
        self.straker = straker
        self.vokial = vokial
        self.moandor = moandor
        self.charna = charna
        self.tamika = tamika
        self.isra = isra
        self.clavius = clavius
        self.galthran = galthran
        self.septienna = septienna
        self.aislinn = aislinn
        self.sandro = sandro
        self.nimbus = nimbus
        self.thant = thant
        self.xsi = xsi
        self.vidomina = vidomina
        self.nagash = nagash
        self.lorelei = lorelei
        self.arlach = arlach
        self.dace = dace
        self.ajit = ajit
        self.damacon = damacon
        self.gunnar = gunnar
        self.synca = synca
        self.shakti = shakti
        self.alamar = alamar
        self.jaegar = jaegar
        self.malekith = malekith
        self.jeddite = jeddite
        self.geon = geon
        self.deemer = deemer
        self.sephinroth = sephinroth
        self.darkstorm = darkstorm
        self.yog = yog
        self.gurnisson = gurnisson
        self.jabarkas = jabarkas
        self.shiva = shiva
        self.gretchin = gretchin
        self.krellion = krellion
        self.crag_hack = crag_hack
        self.tyraxor = tyraxor
        self.gird = gird
        self.vey = vey
        self.dessa = dessa
        self.terek = terek
        self.zubin = zubin
        self.gundula = gundula
        self.oris = oris
        self.saurug = saurug
        self.bron = bron
        self.drakon = drakon
        self.wystan = wystan
        self.tazar = tazar
        self.alkin = alkin
        self.korbac = korbac
        self.gerwulf = gerwulf
        self.broghild = broghild
        self.mirlanda = mirlanda
        self.rosic = rosic
        self.voy = voy
        self.verdish = verdish
        self.merist = merist
        self.styg = styg
        self.andra = andra
        self.tiva = tiva
        self.pasis = pasis
        self.thunar = thunar
        self.ignissa = ignissa
        self.lacus = lacus
        self.monere = monere
        self.erdamon = erdamon
        self.fiur = fiur
        self.kalt = kalt
        self.luna = luna
        self.brissa = brissa
        self.ciele = ciele
        self.labetha = labetha
        self.inteus = inteus
        self.aenain = aenain
        self.gelare = gelare
        self.grindan = grindan
        self.sir_mullich = sir_mullich
        self.adrienne = adrienne
        self.catherine = catherine
        self.dracon = dracon
        self.gelu = gelu
        self.kilgor = kilgor
        self.haart_lich = haart_lich
        self.mutare = mutare
        self.roland = roland
        self.mutare_drake = mutare_drake
        self.boragus = boragus
        self.xeron = xeron
        self.padding_156 = padding_156
        self.padding_157 = padding_157
        self.padding_158 = padding_158
        self.padding_159 = padding_159

    def to_dict(self) -> dict:
        return {
            'orrin': self.orrin,
            'valeska': self.valeska,
            'edric': self.edric,
            'sylvia': self.sylvia,
            'lord_haart': self.lord_haart,
            'sorsha': self.sorsha,
            'christian': self.christian,
            'tyris': self.tyris,
            'rion': self.rion,
            'adela': self.adela,
            'cuthbert': self.cuthbert,
            'adelaide': self.adelaide,
            'ingham': self.ingham,
            'sanya': self.sanya,
            'loynis': self.loynis,
            'caitlin': self.caitlin,
            'mephala': self.mephala,
            'ufretin': self.ufretin,
            'jenova': self.jenova,
            'ryland': self.ryland,
            'thorgrim': self.thorgrim,
            'ivor': self.ivor,
            'clancy': self.clancy,
            'kyrre': self.kyrre,
            'coronius': self.coronius,
            'uland': self.uland,
            'elleshar': self.elleshar,
            'gem': self.gem,
            'malcom': self.malcom,
            'melodia': self.melodia,
            'alagar': self.alagar,
            'aeris': self.aeris,
            'piquedram': self.piquedram,
            'thane': self.thane,
            'josephine': self.josephine,
            'neela': self.neela,
            'torosar': self.torosar,
            'fafner': self.fafner,
            'rissa': self.rissa,
            'iona': self.iona,
            'astral': self.astral,
            'halon': self.halon,
            'serena': self.serena,
            'daremyth': self.daremyth,
            'theodorus': self.theodorus,
            'solmyr': self.solmyr,
            'cyra': self.cyra,
            'aine': self.aine,
            'fiona': self.fiona,
            'rashka': self.rashka,
            'marius': self.marius,
            'ignatius': self.ignatius,
            'octavia': self.octavia,
            'calh': self.calh,
            'pyre': self.pyre,
            'nymus': self.nymus,
            'ayden': self.ayden,
            'xyron': self.xyron,
            'axsis': self.axsis,
            'olema': self.olema,
            'calid': self.calid,
            'ash': self.ash,
            'zydar': self.zydar,
            'xarfax': self.xarfax,
            'straker': self.straker,
            'vokial': self.vokial,
            'moandor': self.moandor,
            'charna': self.charna,
            'tamika': self.tamika,
            'isra': self.isra,
            'clavius': self.clavius,
            'galthran': self.galthran,
            'septienna': self.septienna,
            'aislinn': self.aislinn,
            'sandro': self.sandro,
            'nimbus': self.nimbus,
            'thant': self.thant,
            'xsi': self.xsi,
            'vidomina': self.vidomina,
            'nagash': self.nagash,
            'lorelei': self.lorelei,
            'arlach': self.arlach,
            'dace': self.dace,
            'ajit': self.ajit,
            'damacon': self.damacon,
            'gunnar': self.gunnar,
            'synca': self.synca,
            'shakti': self.shakti,
            'alamar': self.alamar,
            'jaegar': self.jaegar,
            'malekith': self.malekith,
            'jeddite': self.jeddite,
            'geon': self.geon,
            'deemer': self.deemer,
            'sephinroth': self.sephinroth,
            'darkstorm': self.darkstorm,
            'yog': self.yog,
            'gurnisson': self.gurnisson,
            'jabarkas': self.jabarkas,
            'shiva': self.shiva,
            'gretchin': self.gretchin,
            'krellion': self.krellion,
            'crag_hack': self.crag_hack,
            'tyraxor': self.tyraxor,
            'gird': self.gird,
            'vey': self.vey,
            'dessa': self.dessa,
            'terek': self.terek,
            'zubin': self.zubin,
            'gundula': self.gundula,
            'oris': self.oris,
            'saurug': self.saurug,
            'bron': self.bron,
            'drakon': self.drakon,
            'wystan': self.wystan,
            'tazar': self.tazar,
            'alkin': self.alkin,
            'korbac': self.korbac,
            'gerwulf': self.gerwulf,
            'broghild': self.broghild,
            'mirlanda': self.mirlanda,
            'rosic': self.rosic,
            'voy': self.voy,
            'verdish': self.verdish,
            'merist': self.merist,
            'styg': self.styg,
            'andra': self.andra,
            'tiva': self.tiva,
            'pasis': self.pasis,
            'thunar': self.thunar,
            'ignissa': self.ignissa,
            'lacus': self.lacus,
            'monere': self.monere,
            'erdamon': self.erdamon,
            'fiur': self.fiur,
            'kalt': self.kalt,
            'luna': self.luna,
            'brissa': self.brissa,
            'ciele': self.ciele,
            'labetha': self.labetha,
            'inteus': self.inteus,
            'aenain': self.aenain,
            'gelare': self.gelare,
            'grindan': self.grindan,
            'sir_mullich': self.sir_mullich,
            'adrienne': self.adrienne,
            'catherine': self.catherine,
            'dracon': self.dracon,
            'gelu': self.gelu,
            'kilgor': self.kilgor,
            'haart_lich': self.haart_lich,
            'mutare': self.mutare,
            'roland': self.roland,
            'mutare_drake': self.mutare_drake,
            'boragus': self.boragus,
            'xeron': self.xeron,
            'padding_156': self.padding_156,
            'padding_157': self.padding_157,
            'padding_158': self.padding_158,
            'padding_159': self.padding_159
        }