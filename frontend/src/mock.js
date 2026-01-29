// Mock data for AniLibria clone

export const mockReleases = [
  {
    id: 1,
    title: "Звёздное дитя 3",
    original_title: "Oshi no Ko 3rd Season",
    poster: "https://anilibria.top/storage/releases/posters/10089/PKg3Ru0WTMgTSSXhIpJICXjdE5DNvvLE.webp",
    year: 2026,
    season: "Зима",
    type: "ТВ",
    age_rating: "16+",
    genres: ["Драма", "Сейнен"],
    episodes_count: 3,
    description: "Продолжение истории о мире шоу-бизнеса и его тёмных сторонах.",
    rating: 8.9
  },
  {
    id: 2,
    title: "Золотое божество: Финал",
    original_title: "Golden Kamuy: Saishuushou",
    poster: "https://anilibria.top/storage/releases/posters/10101/sw12FMAEHueKiQUdcGZYy7hUquAybwPY.webp",
    year: 2026,
    season: "Зима",
    type: "ТВ",
    age_rating: "18+",
    genres: ["Приключения", "Сейнен", "Исторический"],
    episodes_count: 4,
    description: "Финальный сезон легендарного приключения в поисках золота Айнов.",
    rating: 9.2
  },
  {
    id: 3,
    title: "Какой сейчас Тамон?!",
    original_title: "Tamon-kun ima docchi!?",
    poster: "https://anilibria.top/storage/releases/posters/10104/y8HvWLLIoObzdveAXRm3tyUy0RMsFtq2.webp",
    year: 2026,
    season: "Зима",
    type: "ТВ",
    age_rating: "16+",
    genres: ["Комедия", "Романтика", "Сёдзе"],
    episodes_count: 5,
    description: "Романтическая комедия о запутанных чувствах и недопониманиях.",
    rating: 7.8
  },
  {
    id: 4,
    title: "Смертельная игра ради еды на столе",
    original_title: "Shibou Yuugi de Meshi wo Kuu",
    poster: "https://anilibria.top/storage/releases/posters/10097/1SvcEB9t8SZempPTOfvxDb1fTCzbbA0O.webp",
    year: 2026,
    season: "Зима",
    type: "ТВ",
    age_rating: "18+",
    genres: ["Экшен", "Драма", "Психология"],
    episodes_count: 4,
    description: "Жестокая игра на выживание с высокими ставками.",
    rating: 8.5
  },
  {
    id: 5,
    title: "Будни 29-летнего одинокого искателя приключений",
    original_title: "29-sai Dokushin Chuuken Boukensha no Nichijou",
    poster: "https://anilibria.top/storage/releases/posters/10120/7lKy7wUtnoEdAtkObWZOjYx9FkbscG7u.webp",
    year: 2026,
    season: "Зима",
    type: "ТВ",
    age_rating: "16+",
    genres: ["Фэнтези", "Приключения", "Комедия"],
    episodes_count: 4,
    description: "Повседневная жизнь опытного искателя приключений средних лет.",
    rating: 7.2
  },
  {
    id: 6,
    title: "Дочь владыки демонов слишком добра",
    original_title: "Maou no Musume wa Yasashisugiru!!",
    poster: "https://anilibria.top/storage/releases/posters/10125/mBS3uOgYwjM32PBEPvKGzHlbAELKFpUv.webp",
    year: 2026,
    season: "Зима",
    type: "ТВ",
    age_rating: "12+",
    genres: ["Фэнтези", "Комедия", "Сёнен"],
    episodes_count: 4,
    description: "Дочь повелителя демонов оказывается неожиданно доброй и милой.",
    rating: 7.5
  }
];

export const mockEpisodes = [
  {
    id: 1,
    episode_number: 1,
    title: "Начало новой главы",
    duration: "24:35",
    release_date: "2026-01-15",
    preview: "https://cdn.anilibria.tv/storage/releases/episodes/preview1.webp"
  },
  {
    id: 2,
    episode_number: 2,
    title: "Тайны прошлого",
    duration: "23:48",
    release_date: "2026-01-22",
    preview: "https://cdn.anilibria.tv/storage/releases/episodes/preview2.webp"
  },
  {
    id: 3,
    episode_number: 3,
    title: "Поворотный момент",
    duration: "25:31",
    release_date: "2026-01-29",
    preview: "https://cdn.anilibria.tv/storage/releases/episodes/preview3.webp"
  }
];

export const mockGenres = [
  { id: 1, name: "Сёнен", count: 308, image: "https://cdn.anilibria.tv/storage/anime/genres/images/4/genre.webp" },
  { id: 2, name: "Романтика", count: 445, image: "https://cdn.anilibria.tv/storage/anime/genres/images/11/genre.webp" },
  { id: 3, name: "Меха", count: 56, image: "https://cdn.anilibria.tv/storage/anime/genres/images/2/genre.webp" },
  { id: 4, name: "Вампиры", count: 46, image: "https://cdn.anilibria.tv/storage/anime/genres/images/24/genre.webp" },
  { id: 5, name: "Сверхъестественное", count: 296, image: "https://cdn.anilibria.tv/storage/anime/genres/images/28/genre.webp" },
  { id: 6, name: "Боевые искусства", count: 21, image: "https://cdn.anilibria.tv/storage/anime/genres/images/15/genre.webp" }
];

export const mockFranchises = [
  {
    id: 1,
    name: "Рыцари Сидонии",
    original_name: "Sidonia no Kishi",
    years: "2014 — 2015",
    seasons: 2,
    episodes: 24,
    duration: "9 часов 43 минуты",
    image: "https://cdn.anilibria.tv/storage/anime/franchises/images/franchise1.webp"
  },
  {
    id: 2,
    name: "Связь принцесс: Повторное погружение",
    original_name: "Princess Connect! Re:Dive",
    years: "2020 — 2022",
    seasons: 2,
    episodes: 25,
    duration: "9 часов 53 минуты",
    image: "https://cdn.anilibria.tv/storage/anime/franchises/images/franchise2.webp"
  },
  {
    id: 3,
    name: "Фури-Кури",
    original_name: "FLCL",
    years: "2018 — 2023",
    seasons: 4,
    episodes: 18,
    duration: "7 часов",
    image: "https://cdn.anilibria.tv/storage/anime/franchises/images/franchise3.webp"
  }
];

export const mockVideos = [
  {
    id: 1,
    title: "Песня Аказы (Клинок рассекающий демонов)",
    author: "Люпин",
    views: 0,
    likes: 0,
    preview: "https://cdn.anilibria.tv/storage/media/videos/previews/video1.webp"
  },
  {
    id: 2,
    title: 'Денжи и Резе "Ещё раз" [ЧЕЛОВЕК-БЕНЗОПИЛА]',
    author: "Либриечка Сильв",
    views: 1772,
    likes: 30,
    preview: "https://cdn.anilibria.tv/storage/media/videos/previews/video2.webp"
  },
  {
    id: 3,
    title: "Террормен — русский трейлер (ЗИМА 2026)",
    author: "AniLiberty",
    views: 1024,
    likes: 19,
    preview: "https://cdn.anilibria.tv/storage/media/videos/previews/video3.webp"
  },
  {
    id: 4,
    title: "ЭТА ФАРФОРОВАЯ КУКЛА ЗАЛЕТЕЛА 2 ЗА 18 МИНУТ (ПЕРЕОЗВУЧКА)",
    author: "Sharon [AniLibria.TV]",
    views: 161649,
    likes: 1171,
    preview: "https://cdn.anilibria.tv/storage/media/videos/previews/video4.webp"
  }
];

export const mockTorrents = [
  {
    id: 1,
    release: "Звёздное дитя 3",
    episodes: "1-3",
    size: "4.39 GB",
    seeders: 0,
    leechers: 3,
    downloads: 1092,
    quality: "1080p",
    codec: "x264/AVC",
    date: "29.01.2026, 18:03"
  },
  {
    id: 2,
    release: "Золотое божество: Финал",
    episodes: "1-4",
    size: "8.33 GB",
    seeders: 10,
    leechers: 9,
    downloads: 364,
    quality: "1080p",
    codec: "x264/AVC",
    date: "29.01.2026, 15:30"
  },
  {
    id: 3,
    release: "Смертельная игра ради еды на столе",
    episodes: "1-4",
    size: "784.44 MB",
    seeders: 25,
    leechers: 2,
    downloads: 725,
    quality: "1080p",
    codec: "x265/HEVC",
    badge: "HEVC",
    date: "29.01.2026, 13:31"
  },
  {
    id: 4,
    release: "Какой сейчас Тамон?!",
    episodes: "1-5",
    size: "1.12 GB",
    seeders: 24,
    leechers: 6,
    downloads: 614,
    quality: "1080p",
    codec: "x265/HEVC",
    badge: "HEVC",
    date: "29.01.2026, 11:19"
  }
];

export const mockSchedule = {
  yesterday: [
    {
      id: 1,
      title: "Звёздное дитя 3",
      episode: 2,
      duration: "24:35",
      poster: "https://cdn.anilibria.tv/storage/releases/posters/10100/poster.webp"
    }
  ],
  today: [
    {
      id: 1,
      title: "Звёздное дитя 3",
      episode: 3,
      duration: "25:31",
      poster: "https://cdn.anilibria.tv/storage/releases/posters/10100/poster.webp"
    },
    {
      id: 2,
      title: "Какой сейчас Тамон?!",
      episode: 5,
      duration: "23:40",
      poster: "https://cdn.anilibria.tv/storage/releases/posters/10104/poster.webp"
    }
  ],
  tomorrow: [
    {
      id: 1,
      title: "Золотое божество: Финал",
      episode: 5,
      duration: "24:12",
      poster: "https://cdn.anilibria.tv/storage/releases/posters/10101/poster.webp"
    }
  ]
};