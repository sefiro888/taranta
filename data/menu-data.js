/* =========================================================================
   LA TARANTA - Oviedo | Datos de cartas, menu degustacion y provincias
   -------------------------------------------------------------------------
   IMPORTANTE (demo de presentacion):
   - Los platos y precios proceden de las cartas facilitadas por el cliente
     (carta de autor, carta de desayunos y carta de raciones).
     Se consideran PROVISIONALES hasta su confirmacion por el restaurante.
   - No se han anadido ingredientes, alergenos ni platos que no figurasen
     en esas cartas.
   - Las fotografias solo se asocian a un plato cuando el propio restaurante
     lo identifico asi en su Instagram.
   ========================================================================= */

window.LT_AVISO_PRECIOS =
  'Precios y denominaciones tomados de las cartas facilitadas por el restaurante. ' +
  'Pendientes de confirmación antes de la publicación definitiva.';

/* Tres cartas, tres momentos del dia */
window.CARTAS = [
  { id: 'desayunos', nombre: 'Desayunos',
    titular: 'El Patio despierta',
    texto: 'Molletes de Antequera con nuestro AOVE temprano, tortillas recién hechas y el dulce del día. Andalucía también se desayuna.' },
  { id: 'raciones', nombre: 'Raciones y barra',
    titular: 'Para compartir de pie o sentados',
    texto: 'La barra del sur: fritura, jamón, quesos y guisos en media ración o entera. Lo que se pide sin pensar.' },
  { id: 'autor', nombre: 'Carta de autor',
    titular: 'Alta cocina andaluza',
    texto: 'El recetario del sur pasado por la técnica de hoy, en el comedor El Cortijo.' }
];

/* ------------------------------------------------------------------ CARTA */
window.MENU_DATA = {
  categorias: [
    /* --- Desayunos --- */
    { id: 'molletes', carta: 'desayunos', nombre: 'Molletes de Antequera', kicker: 'Con nuestro A.O.V.E. temprano',
      texto: 'El pan tierno de Antequera, abierto y regado con el aceite de oliva virgen extra de la casa.' },
    { id: 'tortillas', carta: 'desayunos', nombre: 'Nuestras tortillas', kicker: 'Recién cuajadas',
      texto: 'Tortilla de patatas de todos los días y la del queso de cabra con cebolla caramelizada.' },

    /* --- Raciones --- */
    { id: 'raciones', carta: 'raciones', nombre: 'Nuestras raciones', kicker: 'Media o entera',
      texto: 'Fritura andaluza, ibéricos, quesos y guisos para compartir en la barra o en la mesa.' },

    /* --- Carta de autor --- */
    { id: 'alacena', carta: 'autor', nombre: 'Productos de nuestra alacena', kicker: 'Empezar por el principio',
      texto: 'El aceite, el jamón, el queso y la conserva: la despensa del sur puesta sobre la mesa sin intermediarios.' },
    { id: 'frios', carta: 'autor', nombre: 'Empezamos con los fríos', kicker: 'Cocina de temple',
      texto: 'Salmorejos, escabeches y tartares donde el AOVE manda y el frío afina el sabor.' },
    { id: 'calientes', carta: 'autor', nombre: 'Seguimos con calientes', kicker: 'Fuego y paciencia',
      texto: 'Brasa, guiso y casquería fina: la parte más honda del recetario andaluz.' },
    { id: 'arroces', carta: 'autor', nombre: 'Nuestros arroces', kicker: 'Para compartir',
      texto: 'Arroces melosos y negros, elaborados al momento para toda la mesa.' },
    { id: 'lonja', carta: 'autor', nombre: 'De la lonja a la mesa', kicker: 'Pescados',
      texto: 'El pescado trabajado con caldos, cremas y brasas del sur.' },
    { id: 'carnes', carta: 'autor', nombre: 'Nuestras carnes', kicker: 'Dehesa y monte',
      texto: 'Ibérico de Jabugo, lechazo, ciervo y vaca madurada.' },
    { id: 'postres', carta: 'autor', nombre: 'Siempre queda hueco para…', kicker: 'Dulces',
      texto: 'Torrijas, leche merengada y AOVE también en el postre.' }
  ],

  platos: [
    /* ======================= DESAYUNOS ======================= */
    { id: 'b1', cat: 'molletes', nombre: 'Aceite y tomate',
      desc: 'Mollete de Antequera con nuestro AOVE temprano y tomate.', precio: 3.20 },
    { id: 'b2', cat: 'molletes', nombre: 'Aceite, tomate y jamón ibérico de bellota',
      desc: 'El desayuno andaluz completo.', precio: 4.50, destacado: true },
    { id: 'b3', cat: 'molletes', nombre: 'Aceite, tomate y panceta ibérica de bellota',
      desc: 'Panceta ibérica de bellota a la plancha.', precio: 4.50 },
    { id: 'b4', cat: 'molletes', nombre: 'Mantequilla y mermelada',
      desc: 'Para quien prefiere empezar el día en dulce.', precio: 3.00 },

    { id: 't1', cat: 'tortillas', nombre: 'Tortilla de patatas',
      desc: 'Pincho de tortilla de la casa.', precio: 3.50 },
    { id: 't2', cat: 'tortillas', nombre: 'Tortilla de patatas de queso de cabra y cebolla caramelizada',
      desc: 'Con queso de cabra y cebolla caramelizada.', precio: 4.00, destacado: true },
    { id: 't3', cat: 'tortillas', nombre: 'Dulce típico del día',
      desc: 'El dulce andaluz que toque cada mañana.', precio: 0.50, unidad: 'unidad' },

    /* ======================= RACIONES ======================== */
    { id: 'n1', cat: 'raciones', nombre: 'Jamón 50% ibérico D.O. Jabugo de cebo',
      desc: 'Y tomate ecológico con AOVE Premium.', precio: 22.00 },
    { id: 'n2', cat: 'raciones', nombre: 'Tabla de quesos andaluces',
      desc: 'Con toques dulces y crujientes.', precio: 26.80, destacado: true,
      img: 'assets/images/tabla-quesos.jpg',
      alt: 'Tabla de quesos andaluces servida sobre un tronco de madera, fotografía publicada por La Taranta' },
    { id: 'n3', cat: 'raciones', nombre: 'Salmorejo cordobés',
      desc: 'Huevo y jamón asado.', precio: 6.50 },
    { id: 'n4', cat: 'raciones', nombre: 'Papas bravas «La Taranta»',
      desc: 'Las de la casa.', precio: 14.00 },
    { id: 'n5', cat: 'raciones', nombre: 'Croquetas melosas de huevos fritos con chorizo',
      desc: 'Melosas por dentro, crujientes por fuera.', precio: 14.50, precioMedia: 9.00,
      unidades: 'Media 5 uds · Entera 10 uds' },
    { id: 'n6', cat: 'raciones', nombre: 'Puntillitas, salsa carbonara y huevo',
      desc: 'Fritura de bahía con carbonara.', precio: 18.00 },
    { id: 'n7', cat: 'raciones', nombre: 'Calamares a la andaluza',
      desc: 'Enharinados y fritos al momento.', precio: 19.50, precioMedia: 11.00, destacado: true,
      img: 'assets/images/calamares-andaluza.jpg',
      alt: 'Ración de calamares a la andaluza, fotografía publicada por La Taranta' },
    { id: 'n8', cat: 'raciones', nombre: 'Cazón en adobo con ali oli cítrico',
      desc: 'El adobo gaditano de toda la vida.', precio: 19.50, precioMedia: 11.00 },
    { id: 'n9', cat: 'raciones', nombre: 'Fritos de bacalao sobre pisto dulce',
      desc: 'Bacalao frito sobre pisto dulce.', precio: 20.00 },
    { id: 'n10', cat: 'raciones', nombre: 'Pollo frito con mayonesa kimchee',
      desc: 'Crujiente, con un punto picante.', precio: 18.00, precioMedia: 10.00 },
    { id: 'n11', cat: 'raciones', nombre: 'Secreto de cerdo ibérico',
      desc: 'Salsa de boletus y papas deluxe.', precio: 23.50 },
    { id: 'n12', cat: 'raciones', nombre: 'Solomillo de cerdo al Jerez',
      desc: 'Con su salsa al vino de Jerez.', precio: 20.00 },
    { id: 'n13', cat: 'raciones', nombre: 'Carrillada de cerdo estofada al Pedro Ximénez',
      desc: 'Sobre cremoso de papas y AOVE.', precio: 20.00 },

    /* ==================== CARTA DE AUTOR ===================== */
    { id: 'a1', cat: 'alacena', nombre: 'Degustación de aceites tempranos de nuestro Jaén',
      desc: 'Acompañados de pan rústico de masa madre.', precio: 20.20 },
    { id: 'a2', cat: 'alacena', nombre: 'Jamón 50% ibérico D.O. Jabugo cebo de campo',
      desc: 'Y tomate ecológico regado con AOVE Premium.', precio: 22.00 },
    { id: 'a3', cat: 'alacena', nombre: 'Tabla de quesos andaluces',
      desc: 'Con toques dulces y crujientes.', precio: 26.80,
      img: 'assets/images/tabla-quesos.jpg',
      alt: 'Tabla de quesos andaluces servida sobre un tronco de madera, fotografía publicada por La Taranta' },
    { id: 'a4', cat: 'alacena', nombre: 'Anchoa del Cantábrico',
      desc: 'Falsa aceituna de queso curado de oveja y caviar de AOVE.', precio: 27.20, destacado: true,
      img: 'assets/images/falsa-aceituna-anchoa.jpg',
      alt: 'Falsa aceituna de queso con anchoa del Cantábrico, servida sobre un tronco, fotografía publicada por La Taranta' },
    { id: 'a5', cat: 'alacena', nombre: 'Lingote de foie micuit',
      desc: 'Turrón, membrillo y queso caramelizado con toques a violeta y manzana.', precio: 25.50 },
    { id: 'a6', cat: 'alacena', nombre: 'Lomo de jabalí adobado en orza',
      desc: 'Sobre hummus de berenjena asada a fuego vivo.', precio: 18.50 },

    { id: 'f1', cat: 'frios', nombre: 'Salmorejo cremoso de manzana',
      desc: 'AOVE texturizado, berberecho y tierra de aceituna negra.', precio: 8.50, destacado: true },
    { id: 'f2', cat: 'frios', nombre: 'Perdiz en escabeche',
      desc: 'Brotes tiernos, mango, cherries asados y helado de queso Payoyo regado con su jugo.', precio: 19.00 },
    { id: 'f3', cat: 'frios', nombre: 'Tartar de trucha Aguasmulas de Cazorla',
      desc: 'Gazpacho andaluz, cebolla encurtida en remolacha, aguacate y aire de pepino.', precio: 22.00 },
    { id: 'f4', cat: 'frios', nombre: 'Ensalada de cecina asada',
      desc: 'Burrata, canónigos, tomate seco y vinagreta de albahaca y miel.', precio: 16.00 },
    { id: 'f5', cat: 'frios', nombre: 'Carpaccio de presa ibérica D.O. Jabugo',
      desc: 'Anacardos, mayonesa de soja, emulsión de mostaza y queso ahumado.', precio: 18.50 },

    { id: 'c1', cat: 'calientes', nombre: 'Pulpo a la parrilla',
      desc: 'Crema de cuarrécano con toque picante y esponja de plácton.', precio: 27.80,
      nota: 'Grafía de «cuarrécano» y «plácton» según la carta original: pendiente de confirmar.' },
    { id: 'c2', cat: 'calientes', nombre: 'Mollejas de cordero salteadas',
      desc: 'Sepia, alcachofas y jugo de ostras.', precio: 26.00, destacado: true,
      img: 'assets/images/mollejas-cordero.jpg',
      alt: 'Mollejas de cordero salteadas con sepia y alcachofas, servidas en cazuela de barro, fotografía publicada por La Taranta' },
    { id: 'c3', cat: 'calientes', nombre: 'Guiso de manitas de cerdo',
      desc: 'Setas de temporada, parmentier, yema de coral y trufa.', precio: 21.00 },
    { id: 'c4', cat: 'calientes', nombre: 'Croquetas melosas de rabo de toro',
      desc: 'Velo de panceta ibérica y gel de cebolla caramelizada.', precio: 18.00,
      unidades: '6 unidades' },

    { id: 'r1', cat: 'arroces', nombre: 'Arroz meloso de lagarto ibérico',
      desc: 'Anguila ahumada, alioli de pimientos verdes y foie fresco.', precio: 18.50,
      unidad: 'persona', minimo: 2, espera: '20 minutos aproximadamente' },
    { id: 'r2', cat: 'arroces', nombre: 'Arroz negro de gamba roja',
      desc: 'Vieira a la brasa y mayonesa de kimchee.', precio: 20.50,
      unidad: 'persona', minimo: 2, espera: '20 minutos aproximadamente', destacado: true,
      img: 'assets/images/plato-arroz-negro.jpg',
      alt: 'Arroz negro de gamba roja con vieira a la brasa, fotografía publicada por La Taranta en su Instagram' },

    { id: 'p1', cat: 'lonja', nombre: 'Lubina', desc: 'Ajoatao y caldo de jamón ibérico.', precio: 28.00 },
    { id: 'p2', cat: 'lonja', nombre: 'Lomo de atún rojo', desc: 'Verduras en tempura y crema de pimientos asados.', precio: 32.00 },
    { id: 'p3', cat: 'lonja', nombre: 'Corvina soasada', desc: 'Crema de lombarda, langostinos de Sanlúcar y alga codium.', precio: 30.00 },
    { id: 'p4', cat: 'lonja', nombre: 'Rodaballo a la brasa', desc: 'Crema de azafrán, almendra, sidra, espárragos verdes y almejas.', precio: 34.00, destacado: true },

    { id: 'm1', cat: 'carnes', nombre: 'Solomillo de ciervo', desc: 'Seta shiitake y salsa de oporto.', precio: 30.00 },
    { id: 'm2', cat: 'carnes', nombre: 'Paletilla de lechazo a baja temperatura',
      desc: 'Patatas al ajillo, piñones tostados y glaseado de su jugo.', precio: 36.00 },
    { id: 'm3', cat: 'carnes', nombre: 'Abanico ibérico D.O. Jabugo a la brasa',
      desc: 'Salsa teriyaki y patata chafada con A.O.V.E.', precio: 29.00 },
    { id: 'm4', cat: 'carnes', nombre: 'Carrillada de ternera estofada al oloroso',
      desc: 'Sobre crema de patata y A.O.V.E.', precio: 28.00 },
    { id: 'm5', cat: 'carnes', nombre: 'Chuletón de vaca clandestina', desc: 'Con papas y padrón.',
      precio: 55.00, unidad: 'kg', destacado: true },

    { id: 'd1', cat: 'postres', nombre: 'Espuma de leche merengada', desc: 'Crema de galletas y helado de Baileys.', precio: 7.00 },
    { id: 'd2', cat: 'postres', nombre: 'Tarta de queso cremosa', desc: 'Dulce de leche, chocolate blanco texturizado y frutos rojos liofilizados.', precio: 7.00 },
    { id: 'd3', cat: 'postres', nombre: 'Torrija brioche caliente', desc: 'Cremosa de vainilla y anís estrellado, crumble de almendra y helado de A.O.V.E.', precio: 7.00, destacado: true },
    { id: 'd4', cat: 'postres', nombre: 'Brownie de chocolate', desc: 'Helado de pistacho y sopa de chocolate y avellana.', precio: 8.00 },
    { id: 'd5', cat: 'postres', nombre: 'Milhoja crujiente', desc: 'Semifrío de chocolate blanco, helado de plátano y piña liofilizada.', precio: 8.00 }
  ]
};

/* --------------------------------------------- PROVINCIAS - MENU DEGUSTACION
   Nueve pases, uno por provincia andaluza, mas el homenaje final.             */
window.PROVINCIAS = [
  { id: 'jaen', nombre: 'Jaén', orden: 1,
    titular: 'Simplemente Jaén',
    texto: 'La tierra del propietario y del cocinero, y la del aceite. El mar de olivos abre el viaje.',
    pase: 'Falsa trufa de paté de perdiz, piñones, A.O.V.E. texturizado y toque de flores.',
    img: 'assets/images/plato-falsa-trufa-jaen.jpg',
    alt: 'Falsa trufa de paté de perdiz, primer pase del menú degustación, fotografía publicada por La Taranta en su Instagram' },
  { id: 'malaga', nombre: 'Málaga', orden: 2,
    titular: 'Málaga la bella',
    texto: 'La almendra y el vinagre, el mar y la huerta: el ajoblanco servido sobre una ostra.',
    pase: 'Ostra, crema de ajo blanco y boquerón en vinagre.' },
  { id: 'granada', nombre: 'Granada', orden: 3,
    titular: 'De visita por la Alpujarra de Granada',
    texto: 'Chorizo ibérico, patata, huevo y padrón: la tapa alpujarreña llevada al tartar.',
    pase: 'Tartar de chorizo ibérico, espuma de patata, huevo, panceta ibérica y padrón.' },
  { id: 'cadiz', nombre: 'Cádiz', orden: 4,
    titular: 'De chirigotas por Cádiz',
    texto: 'La bahía en un bocado crujiente, con un punto cítrico que despierta.',
    pase: 'Tortita de camarones crujiente y mayonesa de lima.' },
  { id: 'cordoba', nombre: 'Córdoba', orden: 5,
    titular: 'Córdoba la llana',
    texto: 'Guiso largo de toda la vida convertido en canelón, con trufa y queso ahumado.',
    pase: 'Canelón de rabo de toro, crema trufada y lascas de queso ahumado.' },
  { id: 'sevilla', nombre: 'Sevilla', orden: 6,
    titular: 'Paseando por Sevilla en la Feria de Abril',
    texto: 'Tradición de barra y de convento: bacalao, tomate y patata revolcona con técnica de hoy.',
    pase: 'Bacalao a baja temperatura, patata revolcona y tomate especiado.' },
  { id: 'huelva', nombre: 'Huelva', orden: 7,
    titular: 'Pisando las arenas del Rocío a Huelva',
    texto: 'De la sierra de Aracena llega el ibérico, trabajado aquí con caldo de jamón y setas.',
    pase: 'Presa ibérica D.O. Jabugo, caldo de jamón y setas.' },
  { id: 'almeria', nombre: 'Almería', orden: 8,
    titular: 'Un toque dulce de Almería',
    texto: 'Cierra el recorrido por el sur un buñuelo caliente de crema de vainilla.',
    pase: 'Buñuelo con crema de vainilla y mousse de chocolate blanco.' }
];

window.HOMENAJE = {
  nombre: 'Homenaje a Micaela',
  pase: 'Helado de A.O.V.E., pestiños y espuma de leche merengada.',
  texto: 'El último pase no pertenece a ninguna provincia: pertenece a una cocina de casa. Cierra el viaje donde empiezan todas las cocinas del sur.'
};

/* ------------------------------------------- FICHA DEL MENU DEGUSTACION
   Datos facilitados por el restaurante.                                  */
window.MENU_FICHA = {
  precio: 75.00,
  pases: 9,
  antelacion: '48 horas',
  maridaje: 'Selección de vinos del sur: finos, manzanillas, olorosos y amontillados. Se añade aparte para potenciar los sabores del menú.'
};

/* ------------------------------------------------------------------ POEMA
   Poema pintado sobre azulejo en la pared del restaurante.
   Autoria: Virginia A. M., escritora. Granada, 2024.
   Transcrito de la fotografia del panel ceramico facilitada por el cliente.
   ANTES DE PUBLICAR: confirmar con el restaurante la autorizacion de la
   autora para reproducir el texto en la web, y su nombre completo.          */
window.POEMA = {
  titulo: 'La Taranta',
  autora: 'Virginia A. M.',
  oficio: 'Escritora',
  lugar: 'Granada, 2024',
  estrofas: [
    ['En tierras andaluzas, la Taranta nace,',
     'baile ancestral que el corazón enlaza.',
     'En Jaén, Granada y Almería se siente,',
     'el duende flamenco, la pasión latente.'],
    ['La Taranta es cante que brota del alma,',
     'lamento profundo que al cielo reclama.',
     'Gritos de dolor, de amor y de vida,',
     'se funden en baile, en melodía querida.'],
    ['En cada compás, en cada taconeo,',
     'se escucha el eco de un tiempo añejo.',
     'Gente de tierra, de sol y de mar,',
     'viven la Taranta, la saben bailar.'],
    ['Así en Andalucía, la Taranta se vive,',
     'sentimiento profundo que el alma motiva.',
     'En cada palma, en cada guitarra,',
     'resuena el eco de una tierra que canta.']
  ]
};
