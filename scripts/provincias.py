# -*- coding: utf-8 -*-
"""Genera las ocho paginas de provincia y su indice.

Cada provincia lleva:
  · un hero con su silueta recortada del mapa y el numero de pase
  · el plato, con foto
  · la historia, el arte, el habla y la costumbre

La silueta sale del mismo GEO que usa el mapa interactivo
(js/mapa-andalucia.js), asi que si se corrige el mapa se corrigen las
ocho paginas. El plato sale de data/menu-data.js. Nada esta duplicado.

Uso:  python scripts/provincias.py
      python scripts/navegacion.py
      python scripts/sitemap.py
"""
import io, os, re, json
import sys

# La consola de Windows usa cp1252 y revienta con tildes y simbolos.
# Esto fuerza UTF-8 en la salida; si no se puede, sustituye en vez de fallar.
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = 'https://www.latarantaoviedo.com'

# ---------------------------------------------------------------- CONTENIDO
# Cada provincia lleva:
#   gancho      la frase que abre la pagina
#   datos       tres cifras para leer de un vistazo: (cifra, etiqueta)
#   conexion    por que ese plato es esa provincia (el plato en si sale de menu-data.js)
#   hist / arte / habla / cost   cuatro bloques; los parrafos se separan con \n\n
#   habla_ej    la palabra, dicha en una frase
#   cost_cuando cuando ocurre la costumbre
# Los datos con cifra son de dominio publico y se pueden comprobar en cualquier
# enciclopedia. Lo que cuenta el propietario no va aqui, va aparte, como testimonio.
P = {
 'jaen': {
   'nombre': 'Jaén', 'lema': 'El mar de olivos', 'pase_n': 1,
   'gancho': 'Aquí empieza el viaje. La tierra del propietario, la del cocinero y la del aceite que cae sobre cada plato de esta casa.',
   'datos': [('+60 millones', 'de olivos en la provincia'),
             ('Nº 1', 'productor de aceite de oliva del mundo'),
             ('208 a. C.', 'la batalla de Baecula')],
   'foto': 'plato-falsa-trufa-jaen.jpg',
   'foto_pie': 'Falsa trufa de paté de perdiz, el pase de Jaén.',
   'conexion': 'El primer pase junta lo que da la provincia: perdiz, piñón y aceite de oliva virgen extra, texturizado, con un toque de flores.',
   'hist_t': 'Cástulo, y debajo el metal',
   'hist': 'Mucho antes del olivo estuvo el mineral. Cástulo, junto a Linares, fue una de las ciudades más poderosas de la Hispania ibera y romana, y lo fue por lo que había debajo: plomo y plata. Según los autores antiguos, de allí era Himilce, la esposa de Aníbal.\n\nVeinte siglos después, las mismas sierras seguían sacando gente de las entrañas de la tierra, y de ahí salió un cante. Y no es la única historia de guerra y de metal de esta provincia: en Santo Tomé, en la Sierra de Cazorla, se libró la batalla de Baecula, que se cuenta más abajo.',
   'arte_t': 'La taranta, el cante de las minas',
   'arte': 'La taranta es el cante minero por excelencia, y Linares una de las cuencas donde se cantó. Nació abajo, en la galería, con la voz quebrada de quien trabaja a oscuras y sin compás fijo, porque en la mina no hay a quién seguir. De ahí viene el nombre de esta casa: un cante de mineros andaluces plantado en la tierra minera del norte.\n\nDe Linares era también Andrés Segovia, que sacó la guitarra de las tabernas y la llevó a las salas de concierto de medio mundo.',
   'arte_nota': 'Jaén tiene además sus propios fandangos, los de La Puerta de Segura, y las jotas de Siles y Albanchez.',
   'habla_p': 'Ochío',
   'habla': 'En Úbeda y en Baeza, el ochío es un pan de aceite con pimentón que se come solo o relleno. Pan de aceituneros: aguanta la mañana entera en el bolsillo del mandil.',
   'habla_ej': '«Ponme un ochío con aceite».',
   'cost_t': 'La recogida',
   'cost': 'Jaén es el mayor productor de aceite de oliva del mundo, y entre noviembre y febrero la provincia entera se para para recoger. El vareo, la cuadrilla, el almuerzo en el tajo. No es una faena: es un calendario que ordena el año y que ha ordenado la vida de las familias durante generaciones.\n\nCuando la aceituna se coge verde, al principio de la campaña, sale el aceite temprano: menos cantidad, más aroma y más intensidad. Es el A.O.V.E. temprano que aparece en nuestra carta.',
   'cost_cuando': 'Noviembre – febrero',
   # Un relato largo, aparte de los cuatro bloques. La parte historica esta
   # contrastada con las excavaciones de la Universidad de Jaen (Bellon Ruiz
   # y otros, 2015). Lo que es testimonio del propietario va como testimonio.
   'extra': {
     'kicker': 'Aceite con historia',
     'titulo': 'Baecula, 208 antes de Cristo',
     'parrafos': [
       'En el año 208 antes de Cristo, en plena segunda guerra púnica, el general romano <b>Escipión el Africano</b> derrotó cerca de Baecula al cartaginés <b>Asdrúbal Barca</b>, hermano de Aníbal. Fue una de las batallas que decidieron quién mandaría en la península.',
       'Las excavaciones de la Universidad de Jaén sitúan aquel campo de batalla en el <b>Cerro de las Albahacas</b>, en <b>Santo Tomé</b>, en la Sierra de Cazorla. Allí han aparecido restos de armamento, monedas de la época y más de un centenar de fíbulas, los broches con que los soldados sujetaban la capa. Como casi todo lo antiguo, el emplazamiento exacto se sigue discutiendo entre los investigadores, pero el cerro es el candidato mejor documentado.',
       'Asdrúbal se retiró con parte de su ejército hacia la Galia, rumbo a Italia, para reunirse con su hermano. La guerra en Hispania se resolvería dos años después, en Ilipa, junto a la actual Sevilla, donde Escipión fundó Itálica.',
       'Santo Tomé es el pueblo de Juan Carlos, el propietario de La Taranta, y allí tiene sus olivares. Él cuenta que sus olivos crecen en ese mismo cerro de las Albahacas, y que al arar la tierra su familia ha ido encontrando huellas de aquel día: monedas de oro, sandalias, puntas de lanza y colmillos de elefante. Un tío suyo halló varias piezas, que según cuenta se llevaron al Museo de Jaén y, cree, al Museo Arqueológico de Madrid. Por eso, cuando habla del aceite que cae sobre cada plato de esta casa, dice que es <b>aceite con historia</b>.',
     ],
     'nota': 'Relato del propietario. Pendiente de confirmar: el nombre del paraje exacto de su finca y en qué museo está cada pieza.',
   },
 },
 'malaga': {
   'nombre': 'Málaga', 'lema': 'La almendra y el mar', 'pase_n': 2,
   'gancho': 'Casi tres mil años mirando al mar, y una provincia que cabe entera en un plato: la almendra, la huerta y la bahía.',
   'datos': [('≈ 3.000 años', 'de puerto'),
             ('1881', 'nace Picasso en Málaga'),
             ('Mayo – sept.', 'la temporada del espeto')],
   'foto': 'almejas-aove.jpg',
   'foto_pie': 'Almejas con aceite de oliva virgen extra, de la cocina de la casa.',
   'conexion': 'El pase de Málaga junta la huerta y el mar: ostra, crema de ajo blanco y boquerón en vinagre. Almendra, vinagre y pescado: tres sabores muy malagueños en un solo bocado.',
   'hist_t': 'Malaka, la de los fenicios',
   'hist': 'Fundada por los fenicios hacia el siglo VIII antes de Cristo, Málaga lleva casi tres mil años siendo puerto. Por ahí entraron el vino, la pasa y el comercio, y por ahí entró también lo que vino después: romanos, bizantinos, el reino nazarí. Una ciudad que siempre ha mirado al agua.\n\nSobre la ciudad sigue en pie la Alcazaba, palacio-fortaleza musulmán del siglo XI, y a sus pies asoma un teatro romano: siglos de capas, una encima de otra. Ya en el XIX, la ciudad vio nacer a Pablo Picasso, en 1881.',
   'arte_t': 'Malagueñas y verdiales',
   'arte': 'La malagueña viene del fandango y se desprendió del compás hasta volverse cante libre, para escuchar sentado y en silencio. Los verdiales son justo lo contrario: fiesta de pandas, con violín, pandereta y platillos, que bajan de los montes a la ciudad y no se escuchan, se aguantan.\n\nDe ahí que en Málaga el cante se escuche y la fiesta se viva: dos maneras de entender la misma tierra.',
   'habla_p': 'Pitufo',
   'habla': 'En Málaga, el bollito de pan del desayuno. Se pide «un pitufo mixto» y nadie se extraña. Fuera de la provincia hay que explicarlo entero. Y el café, «nube», «sombra» o «mitad», según la leche que lleve: pedirlo así es la forma más rápida de que te tomen por malagueño.',
   'habla_ej': '«Un pitufo mixto y un café mitad».',
   'cost_t': 'El espeto',
   'cost': 'Sardinas ensartadas en una caña y clavadas junto a la brasa, en la arena, al borde del agua. Se cuenta por espetos, no por raciones, y se comen con la mano. Solo de mayo a septiembre: fuera de esos meses, dice el refrán, la sardina no está.\n\nSe asan en barcas de madera llenas de arena, con brasas de leña de olivo, de modo que la sardina nunca toca la parrilla. Tiene que ser de verano, gorda y con su grasa en su sitio.',
   'cost_cuando': 'Mayo – septiembre',
 },
 'granada': {
   'nombre': 'Granada', 'lema': 'La Alpujarra y la cueva', 'pase_n': 3,
   'gancho': 'El último reino de al-Ándalus y la sierra donde se refugió su gente. Granada se bebe con los ojos y se come de tapa en tapa, sin pedir.',
   'datos': [('1492', 'cae el reino nazarí'),
             ('1984', 'la Alhambra, Patrimonio de la Humanidad'),
             ('Casi 3.500 m', 'el Mulhacén, el pico más alto de la península')],
   'foto': 'plato-autor.jpg', 'foto_alto': True,
   'foto_pie': 'Cocina de autor de La Taranta.',
   'conexion': 'El pase de Granada lleva la Alpujarra al tartar: chorizo ibérico, espuma de patata, huevo, panceta ibérica y padrón. Los sabores de la sierra, servidos como un bocado de cocina de autor.',
   'hist_t': 'El último reino',
   'hist': 'Granada fue la capital del último reino musulmán de la península y resistió dos siglos y medio más que el resto de al-Ándalus, hasta 1492. De esa demora vienen la Alhambra y el Generalife, y viene también la Alpujarra: las sierras donde se refugiaron los moriscos y donde quedaron sus pueblos encalados, su manera de cultivar y su comida.\n\nTodo empezó en 1238 con Muhámmad I, el fundador de la dinastía nazarí, que eligió la colina de la Sabika para levantar lo que hoy es la Alhambra. Palacios, agua y yeserías que esta casa homenajea en sus arcos.',
   'arte_t': 'La zambra del Sacromonte',
   'arte': 'En las cuevas del Sacromonte, el barrio gitano de Granada, se baila la zambra: un género propio que recrea los momentos de una boda y que no existe igual en ninguna otra parte de Andalucía. Su nombre viene del árabe, y se suele vincular a los rituales nupciales moriscos del siglo XVI.\n\nEn 1922, Manuel de Falla y Federico García Lorca organizaron en Granada el Concurso de Cante Jondo, convencidos de que aquel arte antiguo merecía respeto y cuidado. Es uno de los momentos fundacionales del flamenco moderno.',
   'arte_nota': 'Granada tiene también su propio cante de cabeza, la granaína.',
   'habla_p': 'Soplillos',
   'habla': 'Merengues de almendra de la Alpujarra, ligerísimos, cocidos en horno de leña. El nombre lo dice todo: pesan lo que un soplido.',
   'habla_ej': '«Anda, ponme un soplillo con el café».',
   'cost_t': 'La tapa que no se pide',
   'cost': 'Granada es de las pocas ciudades de España donde la tapa viene con la bebida y no se elige: llega lo que toque, y cambia con cada ronda. Comer de tapas allí es dejarse llevar, y discutir cuál es el mejor bar es deporte local.\n\nY de la Alpujarra viene el jamón de Trevélez, curado a casi 1.500 metros de altura, donde el aire frío y seco hace casi todo el trabajo.',
   'cost_cuando': 'Todo el año',
 },
 'cadiz': {
   'nombre': 'Cádiz', 'lema': 'La bahía y la chirigota', 'pase_n': 4,
   'gancho': 'Tres mil años de puerto y un mes de carnaval. Cádiz es luz, sal y retranca, y su cocina cabe en un cucurucho de papel.',
   'datos': [('≈ 3.000 años', 'de historia, de las ciudades más antiguas de Europa'),
             ('1812', '«La Pepa», la primera Constitución'),
             ('Febrero', 'el Carnaval')],
   'foto': 'plato-cadiz-tortita-camarones.jpg', 'foto_alto': True,
   'foto_pie': 'Tortita de camarones crujiente, el pase de Cádiz.',
   'conexion': 'El pase de Cádiz es el recuerdo de la bahía más frita: una tortita de camarones crujiente y mahonesa de lima. La tortillita nace en San Fernando y Chiclana: harina de garbanzo, camarón vivo y aceite muy caliente.',
   'hist_t': 'La ciudad más vieja',
   'hist': 'Los fenicios fundaron Gadir y Cádiz pasa por ser una de las ciudades habitadas más antiguas de Europa occidental. Tres mil años de puerto: del comercio del garum romano a las flotas de Indias, y de ahí a 1812, cuando entre sus murallas sitiadas se proclamó la primera Constitución española.\n\nSe proclamó el 19 de marzo, día de San José, y por eso se la conoce como «la Pepa». Se redactó con la ciudad cercada por el ejército francés y el mar como única puerta abierta.',
   'arte_t': 'Alegrías, tanguillos y el tango de Cádiz',
   'arte': 'Cádiz es cuna del tango flamenco, uno de los palos viejos de los que descienden otros muchos. Y es la provincia de las alegrías, cante y baile luminosos que suenan a puerto abierto, y de los tanguillos, que son el compás del Carnaval metido dentro del flamenco.\n\nDe San Fernando, en esta misma bahía, era Camarón de la Isla; de Algeciras, Paco de Lucía. Dos de las voces y manos que cambiaron el flamenco, salidas de la misma provincia.',
   'habla_p': 'Quillo',
   'habla': 'De «chiquillo». Sirve para llamar, para asentir, para rematar una frase y para no decir nada. En Cádiz cabe una conversación entera entre dos «quillo».',
   'habla_ej': '«Quillo, ¿tú has visto eso?»',
   'cost_t': 'El Carnaval',
   'cost': 'Durante un mes, la ciudad se organiza en chirigotas, comparsas y coros que compiten cantando lo que ha pasado en el año. Es sátira cantada, escrita en verso, ensayada desde el verano anterior y juzgada por un público que se sabe las letras antes de oírlas.\n\nSe canta en el teatro, pero sobre todo en la calle: en las plazas, en los bares, en cualquier esquina. Quien no lo ha visto cree que es un espectáculo; quien lo ha vivido sabe que es la ciudad entera cantando.',
   'cost_cuando': 'Febrero',
 },
 'cordoba': {
   'nombre': 'Córdoba', 'lema': 'El guiso largo', 'pase_n': 5,
   'gancho': 'En el siglo X, la ciudad más culta de Occidente. Hoy, la de los patios abiertos, el guiso largo y el cante sin prisa.',
   'datos': [('Siglo X', 'capital del Califato'),
             ('1984', 'la Mezquita, Patrimonio de la Humanidad'),
             ('2012', 'los patios, Patrimonio Inmaterial')],
   'foto': 'canelon-flor.jpg', 'foto_alto': True,
   'foto_pie': 'Canelón de rabo de toro con crema trufada, el pase de Córdoba.',
   'conexion': 'El pase de Córdoba toma el guiso más largo, el rabo de toro, y lo enrolla en un canelón con crema trufada y lascas de queso ahumado. Paciencia de fuego lento, presentación de hoy.',
   'hist_t': 'La capital de Occidente',
   'hist': 'En el siglo X, con el Califato, Córdoba fue una de las ciudades más grandes y cultas del mundo conocido. De entonces quedan la Mezquita y, a las afueras, las ruinas de Medina Azahara, la ciudad palatina que se levantó y se destruyó en menos de un siglo. También fue cuna de Séneca, de Averroes y de Maimónides: tres maneras distintas de pensar en la misma ciudad.\n\nEn el centro quedó la Mezquita, a la que siglos después se le abrió una catedral en mitad del bosque de columnas: dos edificios en uno, y por eso no se parece a nada.',
   'arte_t': 'La soleá y el fandango de Lucena',
   'arte': 'La soleá es el cante hondo por excelencia, y en Córdoba tiene casa propia igual que en Sevilla. En Lucena nació además un fandango con nombre y apellido, de los que se cantan despacio y sin prisa por terminar.\n\nCórdoba celebra desde 1956 el Concurso Nacional de Arte Flamenco, cada tres años, uno de los más prestigiosos del género.',
   'habla_p': 'Flamenquín',
   'habla': 'Lomo enrollado con jamón, empanado y frito. Se discute si nació en Andújar o en Bujalance, pero se come en toda la provincia y se pide por su nombre, nunca por su descripción.',
   'habla_ej': '«Dos flamenquines y una de salmorejo».',
   'cost_t': 'Los patios',
   'cost': 'En mayo, los vecinos abren sus patios encalados y llenos de macetas para que entre cualquiera. Es Patrimonio Cultural Inmaterial de la Humanidad desde 2012, y sigue siendo lo que siempre fue: casas particulares con la puerta abierta y el suelo recién regado.\n\nHay concurso, y cada patio compite por ser el que mejor huele y mejor se ve. Pero lo que se gana es lo de menos: se hace para que pase la gente.',
   'cost_cuando': 'Mayo',
 },
 'sevilla': {
   'nombre': 'Sevilla', 'lema': 'La feria de abril', 'pase_n': 6,
   'gancho': 'Fue la puerta de un continente y es la ciudad que mejor sabe convertir una semana en una fiesta.',
   'datos': [('206 a. C.', 'Escipión funda Itálica'),
             ('1503', 'la Casa de Contratación, puerta de las Indias'),
             ('1847', 'la primera Feria de Abril')],
   'foto': 'plato-sevilla-bacalao.jpg',
   'foto_pie': 'Bacalao con patata revolcona y tomate especiado, el pase de Sevilla.',
   'conexion': 'El pase de Sevilla es de barra y de convento: bacalao a baja temperatura, patata revolcona y tomate especiado. Receta de siempre, técnica de ahora.',
   'hist_t': 'El puerto de las Indias',
   'hist': 'Al lado de Sevilla está Itálica, la primera ciudad romana fundada fuera de Italia y cuna de dos emperadores. Pero su siglo fue el XVI: durante casi doscientos años, todo el comercio con América pasó obligatoriamente por su puerto fluvial. Sevilla fue, literalmente, la puerta de un continente.\n\nItálica la fundó Escipión el Africano en el 206 antes de Cristo, tras ganar en Ilipa, para asentar a sus soldados heridos. Es la continuación de la historia de Baecula, que se cuenta en <a href="provincia-jaen.html">la ficha de Jaén</a>.',
   'arte_t': 'La soleá de Triana y las sevillanas',
   'arte': 'Triana es uno de los barrios fundacionales del flamenco, y de allí sale una de las formas de la soleá. Las sevillanas son otra cosa distinta: no son un palo flamenco al uso, sino un baile popular que se aprende de niño, se baila de a dos y se sabe sin haberlo estudiado nunca.\n\nLa Bienal de Flamenco de Sevilla, que se celebra cada dos años desde 1980, es la gran cita internacional del género.',
   'habla_p': 'Pringá',
   'habla': 'Lo que queda del cocido —carne, tocino, morcilla— deshecho y servido dentro de un montadito. Se pide al final, cuando ya no cabe nada. Y siempre cabe.',
   'habla_ej': '«Una pringá, y que no falte el pan».',
   'cost_t': 'La Feria',
   'cost': 'Una semana de abril en la que la ciudad entera se muda a un recinto de casetas, con su alumbrado, su rebujito y sus sevillanas. Tiene reglas no escritas que todo el mundo conoce y que nadie ha explicado nunca a nadie de fuera.\n\nEl rebujito, manzanilla con refresco de limón, corre por las casetas, y los trajes de flamenca se renuevan cada año: lunares, volantes y mantoncillo.',
   'cost_cuando': 'Abril',
 },
 'huelva': {
   'nombre': 'Huelva', 'lema': 'La marisma y la dehesa', 'pase_n': 7,
   'gancho': 'Del borde de Europa salió el viaje más largo. Huelva es marisma, dehesa y fandango, y la tierra del jamón de Jabugo.',
   'datos': [('1492', 'zarpa de Palos la expedición de Colón'),
             ('Doñana', 'Parque Nacional y Patrimonio de la Humanidad'),
             ('2010', 'los fandangos de Huelva, Bien de Interés Cultural')],
   'foto': 'carpaccio-presa.jpg',
   'foto_pie': 'Carpaccio de presa ibérica.',
   'conexion': 'El pase de Huelva viene de la sierra de Aracena: presa ibérica D.O. Jabugo con caldo de jamón y setas. De la dehesa al plato, con el producto como único adorno.',
   'hist_t': 'Tartessos y el viaje',
   'hist': 'La costa de Huelva se asocia al reino de Tartessos, la primera civilización documentada de la península, rica precisamente por los metales de su sierra. Tres mil años después, de uno de sus puertos, Palos de la Frontera, zarpó en 1492 la expedición que cruzó el Atlántico. Dos veces, con mucho tiempo de por medio, Huelva fue el borde del mundo conocido.\n\nLas minas de Riotinto, explotadas desde la Antigüedad y de nuevo a gran escala desde el siglo XIX, dan cuenta de lo mismo: como en Jaén y en Almería, esta tierra se entiende mirando bajo el suelo.',
   'arte_t': 'Los fandangos de Huelva',
   'arte': 'La provincia tiene una variedad de fandangos que no tiene ninguna otra: casi cada pueblo el suyo, y Alosno por encima de todos. Fueron declarados Bien de Interés Cultural en 2010. Se cantan en corro y se reconocen por el pueblo, no por el autor.\n\nEs música de compartir más que de escuchar: se aprende de oído, en familia y en la plaza.',
   'habla_p': 'Choco',
   'habla': 'La sepia. Y «choco con habas», el guiso de la casa: mar y huerta en la misma cazuela. En Huelva no se dice sepia, y quien la dice se delata.',
   'habla_ej': '«Choco con habas, y una cerveza bien fría».',
   'cost_t': 'El Rocío',
   'cost': 'Las hermandades cruzan la marisma a pie, a caballo y en carreta hasta la aldea de El Rocío. Son días de camino, no de viaje: se duerme en el campo y se llega cuando se llega. Es la romería más multitudinaria de España.\n\nSe celebra en Pentecostés, con más de cien hermandades que llegan de toda Andalucía y de otros lugares de España. La Virgen sale en procesión en la madrugada del lunes, entre una multitud que la acompaña.',
   'cost_cuando': 'Mayo o junio (Pentecostés)',
 },
 'almeria': {
   'nombre': 'Almería', 'lema': 'El desierto y el invernadero', 'pase_n': 8,
   'gancho': 'La más seca de Andalucía, la última del mapa y la que cierra el recorrido. Almería es desierto, invernadero y un mar azul sin casi nadie.',
   'datos': [('955', 'Abderramán III funda la ciudad'),
             ('Tabernas', 'el único desierto de Europa'),
             ('1997', 'Cabo de Gata, Reserva de la Biosfera')],
   'foto': 'postre-taranta.jpg',
   'foto_pie': 'Postre de la casa.',
   'conexion': 'El pase de Almería es dulce: buñuelo con crema de vainilla y mousse de chocolate blanco. Cierra el recorrido por las ocho provincias.',
   'hist_t': 'Al-Mariyya, el espejo del mar',
   'hist': 'Almería nació en el siglo X como puerto del Califato de Córdoba, y su nombre árabe se suele traducir como «el espejo del mar» o «la atalaya». De entonces es su Alcazaba, una de las fortalezas musulmanas más grandes de España. Siglos después llegó la otra riqueza: las minas de la Sierra Almagrera, que trajeron gente, dinero y, como en Jaén, un cante.\n\nLa Alcazaba se levantó para vigilar la ciudad y el puerto, y casi mil años después sigue mirando al mar.',
   'arte_t': 'El taranto',
   'arte': 'El taranto es el palo almeriense, hermano de la taranta de la que toma el nombre, pero con el compás algo más marcado. También nació en las minas: las de la Sierra Almagrera. Es, con Jaén, el otro extremo de la ruta minera del flamenco, y el que cierra el círculo de este menú.\n\nJaén y Almería, en los dos extremos del este andaluz, comparten el origen de este cante: el de quienes trabajaban bajo la tierra.',
   'habla_p': 'Gurullos',
   'habla': 'Pasta artesanal, hecha a mano en bolitas pequeñas, con la que se guisa con conejo o con pulpo. Comida de campo y de invierno, en la provincia más seca de Europa.',
   'habla_ej': '«Gurullos con conejo, de cuchara y con pan».',
   'cost_t': 'El desierto y el cine',
   'cost': 'En Tabernas, el único desierto de Europa, se rodaron los spaghetti westerns y media historia del cine de aventuras. Al lado, el mar de plástico de los invernaderos da de comer a media Europa durante el invierno. Dos paisajes imposibles, pegados.\n\nY a pocos kilómetros, el Cabo de Gata, de los pocos tramos de costa sin construir del Mediterráneo español: calas, volcanes antiguos y salinas.',
   'cost_cuando': 'Todo el año',
 },
}

ORDEN = ['jaen', 'malaga', 'granada', 'cadiz', 'cordoba', 'sevilla', 'huelva', 'almeria']


# ------------------------------------------------- Datos que ya estan en el sitio
def geo():
    """Los trazados del mapa interactivo, para no duplicar el dibujo."""
    s = io.open(os.path.join(RAIZ, 'js', 'mapa-andalucia.js'), encoding='utf-8').read()
    bruto = re.search(r'var GEO = (\{.*?\});', s, re.S).group(1)
    return json.loads(bruto)


def pases():
    """El pase de cada provincia, desde la fuente unica de la carta."""
    s = io.open(os.path.join(RAIZ, 'data', 'menu-data.js'), encoding='utf-8').read()
    bloque = re.search(r'window\.PROVINCIAS\s*=\s*\[(.*?)\n\];', s, re.S).group(1)
    out = {}
    for m in re.finditer(r"\{\s*id:\s*'([a-z]+)'(.*?)\}\s*,?\s*(?=\{\s*id:|$)", bloque, re.S):
        pid, cuerpo = m.group(1), m.group(2)

        def campo(n):
            r = re.search(n + r":\s*'((?:[^'\\]|\\.)*)'", cuerpo)
            return r.group(1).replace("\\'", "'") if r else ''

        al = re.search(r"alergenos:\s*\[(.*?)\]", cuerpo, re.S)
        out[pid] = {
            'titular': campo('titular'), 'texto': campo('texto'), 'pase': campo('pase'),
            'apunte': campo('apunte'),
            'alergenos': re.findall(r"'([^']+)'", al.group(1)) if al else [],
        }
    return out


def silueta(trazado, clase='prov-silueta'):
    """La provincia sola, recortada y ajustada a su propio marco."""
    nums = [float(x) for x in re.findall(r'-?\d+\.?\d*', trazado)]
    xs, ys = nums[0::2], nums[1::2]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    m = max(x1 - x0, y1 - y0) * 0.06
    vb = '%.1f %.1f %.1f %.1f' % (x0 - m, y0 - m, (x1 - x0) + 2 * m, (y1 - y0) + 2 * m)
    return ('<svg class="%s" viewBox="%s" aria-hidden="true" focusable="false">'
            '<path d="%s"/></svg>' % (clase, vb, trazado))


def plantilla():
    cab = io.open(os.path.join(RAIZ, 'historia.html'), encoding='utf-8').read()
    inicio = re.search(r'<!doctype html>.*?<body>', cab, re.S).group(0)
    pie = re.search(r'<footer class="pie">.*?</html>', cab, re.S).group(0)
    return inicio, pie


def meta(inicio, titulo, desc, url, img, alt):
    s = inicio
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % titulo, s)
    for pat, val in [
        (r'(<meta name="description" content=")[^"]*(">)', desc),
        (r'(<meta property="og:title" content=")[^"]*(">)', titulo),
        (r'(<meta name="twitter:title" content=")[^"]*(">)', titulo),
        (r'(<meta property="og:description" content=")[^"]*(">)', desc),
        (r'(<meta name="twitter:description" content=")[^"]*(">)', desc),
        (r'(<link rel="canonical" href=")[^"]*(">)', url),
        (r'(<meta property="og:url" content=")[^"]*(">)', url),
        (r'(<meta property="og:image" content=")[^"]*(">)', img),
        (r'(<meta property="og:image:secure_url" content=")[^"]*(">)', img),
        (r'(<meta name="twitter:image" content=")[^"]*(">)', img),
        (r'(<meta property="og:image:alt" content=")[^"]*(">)', alt),
    ]:
        s = re.sub(pat, lambda m, v=val: m.group(1) + v + m.group(2), s, count=1)
    return s


def parrafos(txt):
    """Un texto con parrafos separados por linea en blanco -> varios <p>."""
    return ''.join('        <p>%s</p>\n' % p.strip() for p in txt.split('\n\n') if p.strip())


def extra(d):
    """Un relato largo opcional (hoy, Baecula en la ficha de Jaen)."""
    e = d.get('extra')
    if not e:
        return ''
    ps = ''.join('      <p>%s</p>\n' % p for p in e['parrafos'])
    nota = ('      <p class="apunte">%s</p>\n' % e['nota']) if e.get('nota') else ''
    return ('<section class="seccion fondo-marfil textura-papel">\n'
            '  <div class="contenedor--estrecho">\n'
            '    <article class="prov-relato reveal">\n'
            '      <p class="kicker">%s</p>\n'
            '      <h2>%s</h2>\n'
            '%s%s'
            '    </article>\n'
            '  </div>\n'
            '</section>\n\n' % (e['kicker'], e['titulo'], ps, nota))


# ------------------------------------------------------------------- PAGINAS
def pagina(pid, d, pase, G, inicio, pie, ant, sig):
    nombre = d['nombre']
    titulo = '%s · Las ocho provincias de La Taranta' % nombre
    desc = ('%s en el menú degustación de La Taranta: %s Su historia, su cante, su habla y sus costumbres.'
            % (nombre, pase['pase']))
    s = meta(inicio, titulo, desc[:250],
             '%s/provincia-%s.html' % (DOM, pid),
             '%s/assets/images/compartir-degustacion.jpg' % DOM,
             'El menú degustación de La Taranta')

    alerg = ('<p class="alergenos"><b>Alérgenos</b> %s</p>' % ' · '.join(pase['alergenos'])) \
        if pase['alergenos'] else ''
    apunte = ('<p class="apunte">%s</p>' % pase['apunte']) if pase['apunte'] else ''
    marco = 'marco--alto' if d.get('foto_alto') else 'marco--ancho'
    datos = ''.join('<div class="dato"><strong>%s</strong><span>%s</span></div>' % (c, e)
                    for c, e in d['datos'])
    nota_arte = ('        <p class="prov-ed__nota">%s</p>\n' % d['arte_nota']) if d.get('arte_nota') else ''

    main = (
      '<main id="contenido">\n\n'

      # ---- cabecera
      '<section class="prov-hero">\n'
      '  <div class="contenedor prov-hero__int">\n'
      '    <div class="prov-hero__texto">\n'
      '      <p class="kicker"><a href="provincias.html">Las ocho provincias</a></p>\n'
      '      <p class="prov-hero__num">Pase ' + str(d['pase_n']) + ' de 9</p>\n'
      '      <h1>' + nombre + '</h1>\n'
      '      <p class="prov-hero__lema">' + d['lema'] + '</p>\n'
      '      <p class="lead">' + d['gancho'] + '</p>\n'
      '    </div>\n'
      '    <div class="prov-hero__mapa">' + silueta(G['paths'][pid]) + '</div>\n'
      '  </div>\n'
      '</section>\n\n'

      # ---- tres datos de un vistazo
      '<section class="seccion seccion--compacta fondo-carbon">\n'
      '  <div class="contenedor">\n'
      '    <div class="datos prov-datos reveal">' + datos + '</div>\n'
      '  </div>\n'
      '</section>\n\n'

      # ---- el plato
      '<section class="seccion fondo-carbon textura-azulejo">\n'
      '  <div class="contenedor">\n'
      '    <div class="duo duo--medio">\n'
      '      <div class="reveal">\n'
      '        <div class="marco ' + marco + ' marco--filete arco">'
      '<img src="assets/images/' + d['foto'] + '" alt="' + d['foto_pie'] + '" loading="lazy"></div>\n'
      '        <p class="pie-foto">' + d['foto_pie'] + '</p>\n'
      '      </div>\n'
      '      <div class="reveal" data-delay="1">\n'
      '        <p class="kicker">El plato</p>\n'
      '        <h2>' + pase['titular'] + '</h2>\n'
      '        <p class="lead">' + pase['texto'] + '</p>\n'
      '        <p>' + d['conexion'] + '</p>\n'
      '        <div class="mapa-panel__pase" style="margin-top:1.6rem"><b>El pase</b><p>'
      + pase['pase'] + '</p>' + apunte + alerg + '</div>\n'
      '      </div>\n'
      '    </div>\n'
      '  </div>\n'
      '</section>\n\n'

      # ---- la historia
      '<section class="seccion fondo-marfil textura-papel">\n'
      '  <div class="contenedor">\n'
      '    <div class="prov-ed reveal">\n'
      '      <header class="prov-ed__cab">\n'
      '        <p class="kicker">La historia</p>\n'
      '        <h2>' + d['hist_t'] + '</h2>\n'
      '      </header>\n'
      '      <div class="prov-ed__cuerpo capitular">\n' + parrafos(d['hist']) +
      '      </div>\n'
      '    </div>\n'
      '  </div>\n'
      '</section>\n\n'

      # ---- el arte
      '<section class="seccion fondo-carbon">\n'
      '  <div class="contenedor">\n'
      '    <div class="prov-ed prov-ed--inv reveal">\n'
      '      <header class="prov-ed__cab">\n'
      '        <p class="kicker">El arte</p>\n'
      '        <h2>' + d['arte_t'] + '</h2>\n'
      '      </header>\n'
      '      <div class="prov-ed__cuerpo">\n' + parrafos(d['arte']) + nota_arte +
      '      </div>\n'
      '    </div>\n'
      '  </div>\n'
      '</section>\n\n'

      # ---- la palabra
      '<section class="seccion fondo-marfil">\n'
      '  <div class="contenedor--estrecho prov-palabra centro reveal">\n'
      '    <p class="kicker kicker--centro">El habla</p>\n'
      '    <p class="prov-palabra__voz">' + d['habla_p'] + '</p>\n'
      '    <p class="prov-palabra__def">' + d['habla'] + '</p>\n'
      '    <p class="prov-palabra__ej">' + d['habla_ej'] + '</p>\n'
      '  </div>\n'
      '</section>\n\n'

      # ---- la costumbre
      '<section class="seccion fondo-carbon textura-azulejo">\n'
      '  <div class="contenedor">\n'
      '    <div class="prov-ed prov-ed--inv reveal">\n'
      '      <header class="prov-ed__cab">\n'
      '        <p class="kicker">La costumbre</p>\n'
      '        <h2>' + d['cost_t'] + '</h2>\n'
      '        <p class="prov-cuando"><span>Cuándo</span>' + d['cost_cuando'] + '</p>\n'
      '      </header>\n'
      '      <div class="prov-ed__cuerpo">\n' + parrafos(d['cost']) +
      '      </div>\n'
      '    </div>\n'
      '  </div>\n'
      '</section>\n\n'

      + extra(d) +

      '<section class="seccion fondo-carbon textura-azulejo">\n'
      '  <div class="contenedor centro reveal">\n'
      '    <div class="cenefa cenefa--clara" aria-hidden="true" style="margin-bottom:clamp(2rem,4vw,2.8rem)"></div>\n'
      '    <h2>Las ocho, de una sentá</h2>\n'
      '    <p class="lead" style="margin-inline:auto">' + nombre + ' es el pase número '
      + str(d['pase_n']) + ' del menú degustación. El recorrido entero son las ocho provincias '
      'y un homenaje final que no pertenece a ninguna.</p>\n'
      '    <div class="acciones acciones--centro" style="margin-top:2.2rem">\n'
      '      <a class="boton" href="menu-degustacion.html">Ver el menú degustación</a>\n'
      '      <a class="boton boton--fantasma" href="reservas.html">Reservar mesa</a>\n'
      '    </div>\n'
      '    <nav class="prov-paso" aria-label="Otras provincias">\n'
      '      <a class="prov-paso__ir" href="provincia-' + ant + '.html">'
      + silueta(G['paths'][ant], 'prov-paso__mapa')
      + '<span><em>Anterior</em>' + P[ant]['nombre'] + '</span></a>\n'
      '      <a class="prov-paso__todas" href="provincias.html">Ver las ocho</a>\n'
      '      <a class="prov-paso__ir prov-paso__ir--der" href="provincia-' + sig + '.html">'
      + '<span><em>Siguiente</em>' + P[sig]['nombre'] + '</span>'
      + silueta(G['paths'][sig], 'prov-paso__mapa') + '</a>\n'
      '    </nav>\n'
      '  </div>\n'
      '</section>\n'
      '</main>\n\n')

    return s + '\n' + main + pie


def indice(inicio, pie, datos, G):
    titulo = 'Las ocho provincias andaluzas · La Taranta Oviedo'
    desc = ('El menú degustación de La Taranta recorre las ocho provincias andaluzas en nueve pases. '
            'La historia, el cante, el habla y las costumbres de cada una.')
    s = meta(inicio, titulo, desc, '%s/provincias.html' % DOM,
             '%s/assets/images/compartir-degustacion.jpg' % DOM,
             'El menú degustación de La Taranta')

    # Un indice ligero para quien no use el mapa (teclado, lector de pantalla,
    # buscadores): ocho enlaces con su silueta, sin fotos de platos.
    lista = []
    for pid in ORDEN:
        d = P[pid]
        lista.append(
          '        <li><a class="prov-lista__ir" href="provincia-' + pid + '.html">\n'
          '          ' + silueta(G['paths'][pid], 'prov-lista__mapa') + '\n'
          '          <span class="prov-lista__num">' + str(d['pase_n']) + '</span>\n'
          '          <span class="prov-lista__nombre">' + d['nombre'] + '</span>\n'
          '          <span class="prov-lista__lema">' + d['lema'] + '</span>\n'
          '        </a></li>')

    main = (
      '<main id="contenido">\n\n'
      '<section class="hero hero--interior hero--mapa">\n'
      '  <div class="hero__media">\n'
      '    <img src="assets/images/mapa-andalucia-hero-sm.jpg" srcset="assets/images/mapa-andalucia-hero-sm.jpg 1400w, assets/images/mapa-andalucia-hero.jpg 2048w" sizes="100vw" alt="Mapa ilustrado de Andalucía en estilo de cartografía antigua, con sus ocho provincias" fetchpriority="high">\n'
      '  </div>\n'
      '  <img class="hero__arco" src="assets/logo/isotipo-marfil.png" width="945" height="262" alt="" loading="lazy">\n'
      '  <div class="hero__int">\n'
      '    <p class="kicker">Andalucía, plato a plato</p>\n'
      '    <h1>Las ocho provincias</h1>\n'
      '    <p class="lead">El menú degustación recorre Andalucía entera en nueve pases. Detrás de cada '
      'plato hay una provincia con su historia, su cante, su palabra y su costumbre. Aquí están las ocho, '
      'una por una.</p>\n'
      '  </div>\n'
      '</section>\n\n'

      '<section class="seccion fondo-marfil">\n'
      '  <div class="contenedor">\n'
      '    <div class="centro reveal" style="margin-bottom:clamp(2rem,4vw,3rem)">\n'
      '      <p class="kicker kicker--centro">El mapa</p>\n'
      '      <h2>Elija una provincia</h2>\n'
      '      <p class="lead centro">Siga la ruta del menú, de Jaén a Almería. Toque una provincia para ver '
      'su pase y entrar en su historia.</p>\n'
      '    </div>\n'
      '    <div class="mapa-layout reveal">\n'
      '      <div class="mapa-marco mapa-marco--arte">\n'
      '        <div data-mapa data-mapa-modo="compacto" data-mapa-arte></div>\n'
      '      </div>\n'
      '      <aside class="mapa-panel" data-mapa-panel aria-live="polite"></aside>\n'
      '    </div>\n'
      '    <nav class="prov-lista reveal" aria-label="Las ocho provincias">\n'
      '      <ol>\n'
      + '\n'.join(lista) + '\n'
      '      </ol>\n'
      '    </nav>\n'
      '    <div class="contenedor--estrecho centro reveal" style="margin-top:clamp(3rem,6vw,5rem)">\n'
      '      <p class="kicker kicker--centro">El noveno pase</p>\n'
      '      <h2>Homenaje a la abuela Micaela</h2>\n'
      '      <p class="lead" style="margin-inline:auto">No pertenece a ninguna provincia: es el postre con el que el chef cierra el recorrido.</p>\n'
      '      <p>Helado de A.O.V.E., pestiños y espuma de leche merengada.</p>\n'
      '      <a class="enlace-fino" href="menu-degustacion.html">Verlo en el menú</a>\n'
      '    </div>\n'
      '  </div>\n'
      '</section>\n\n'

      '<section class="seccion fondo-carbon textura-azulejo">\n'
      '  <div class="contenedor centro reveal">\n'
      '    <div class="cenefa cenefa--clara" aria-hidden="true" style="margin-bottom:clamp(2rem,4vw,2.8rem)"></div>\n'
      '    <h2>Las ocho provincias<br>de una sentá</h2>\n'
      '    <p class="lead" style="margin-inline:auto">Nueve pases, dos comensales, cuarenta y ocho horas '
      'de antelación.</p>\n'
      '    <div class="acciones acciones--centro" style="margin-top:2.2rem">\n'
      '      <a class="boton" href="menu-degustacion.html">Ver el menú degustación</a>\n'
      '      <a class="boton boton--fantasma" href="reservas.html">Reservar mesa</a>\n'
      '    </div>\n'
      '  </div>\n'
      '</section>\n'
      '</main>\n\n')

    # El mapa necesita los datos de la carta y el trazado; las provincias
    # sueltas no. Se cargan solo aqui, antes de cerrar el cuerpo.
    scripts = ('<script src="data/menu-data.js"></script>\n'
               '<script src="js/mapa-andalucia.js"></script>\n')
    pie = pie.replace('</body>', scripts + '</body>', 1)
    return s + '\n' + main + pie


def generar():
    os.chdir(RAIZ)
    datos = pases()
    G = geo()
    inicio, pie = plantilla()
    for i, pid in enumerate(ORDEN):
        ant = ORDEN[(i - 1) % len(ORDEN)]
        sig = ORDEN[(i + 1) % len(ORDEN)]
        html = pagina(pid, P[pid], datos[pid], G, inicio, pie, ant, sig)
        io.open('provincia-%s.html' % pid, 'w', encoding='utf-8', newline='').write(html)
        print('  provincia-%s.html' % pid)
    io.open('provincias.html', 'w', encoding='utf-8', newline='').write(indice(inicio, pie, datos, G))
    print('  provincias.html (indice)')
    print('generadas', len(ORDEN) + 1, 'paginas')


if __name__ == '__main__':
    generar()
