import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Youtube, Heart, Download, Clock, Play } from 'lucide-react';
import { Button } from '../components/ui/button';
import ReleaseCard from '../components/ReleaseCard';
import { mockReleases, mockGenres, mockFranchises, mockVideos, mockTorrents } from '../mock';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-[#0f0f14]">
      {/* Hero Promo Banner */}
      <section className="relative h-[400px] overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/50 via-pink-900/50 to-blue-900/50" />
        <img
          src="https://cdn.anilibria.tv/storage/media/promotions/images/promo.webp"
          alt="Promo"
          className="absolute inset-0 w-full h-full object-cover opacity-30"
          onError={(e) => {
            e.target.style.display = 'none';
          }}
        />
        <div className="relative container mx-auto px-4 h-full flex flex-col justify-center items-center text-center">
          <Youtube className="w-16 h-16 text-white mb-4" />
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            AniLiberty на YouTube
          </h1>
          <p className="text-lg text-gray-300 max-w-2xl mb-6">
            Если вы смотрите аниме на нашем сайте и вам интересно, как всё это создаётся — загляните на наш YouTube.
            Мы там показываем закулисье работы, делимся трейлерами и стримами.
          </p>
          <Button
            size="lg"
            className="bg-red-600 hover:bg-red-700 text-white"
            onClick={() => window.open('https://youtube.com', '_blank')}
          >
            Подписывайся!
          </Button>
        </div>
      </section>

      <div className="container mx-auto px-4">
        {/* New Episodes */}
        <section className="py-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl md:text-3xl font-bold text-white">Новые эпизоды</h2>
            <Link
              to="/catalog"
              className="text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1"
            >
              Все релизы
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <p className="text-gray-400 mb-8">Самые новые и свежие эпизоды в любимой озвучке</p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {mockReleases.map((release) => (
              <ReleaseCard key={release.id} release={release} />
            ))}
          </div>
        </section>

        {/* Support Banner */}
        <section className="py-12">
          <div className="relative rounded-2xl overflow-hidden bg-gradient-to-r from-purple-900/50 to-pink-900/50 p-8 md:p-12">
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-4">
                <Heart className="w-8 h-8 text-pink-400" />
                <h2 className="text-2xl md:text-3xl font-bold text-white">Поддержите AniLiberty!</h2>
              </div>
              <p className="text-gray-300 mb-6 max-w-2xl">
                Поддержите команду проекта. Получите доступ в закрытый чат в Telegram, а также специальный статус на нашем Discord сервере
              </p>
              <Button
                size="lg"
                className="bg-purple-600 hover:bg-purple-700 text-white"
                onClick={() => window.open('/support', '_self')}
              >
                Поддержать
              </Button>
            </div>
          </div>
        </section>

        {/* Latest Videos */}
        <section className="py-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl md:text-3xl font-bold text-white">Последние видео</h2>
            <Link
              to="/videos"
              className="text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1"
            >
              Все видео
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <p className="text-gray-400 mb-8">Самые интересные видео ролики от любимой команды</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {mockVideos.map((video) => (
              <div
                key={video.id}
                className="group relative rounded-xl overflow-hidden bg-gray-900 cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/20"
              >
                <div className="relative aspect-video">
                  <img
                    src={video.preview}
                    alt={video.title}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/400x225/1f1f2e/8b5cf6?text=Video';
                    }}
                  />
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center">
                      <Play className="w-6 h-6 text-white ml-1" fill="white" />
                    </div>
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="text-white text-sm font-medium line-clamp-2 mb-2">
                    {video.title}
                  </h3>
                  <p className="text-gray-400 text-xs mb-2">{video.author}</p>
                  {video.views > 0 && (
                    <div className="flex items-center gap-3 text-xs text-gray-500">
                      <span>{video.likes} •</span>
                      <span>{video.views} просмотров</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Franchises */}
        <section className="py-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl md:text-3xl font-bold text-white">Франшизы</h2>
            <Link
              to="/franchises"
              className="text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1"
            >
              Все франшизы
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <p className="text-gray-400 mb-8">Самые интересные и захватывающие франшизы в любимой озвучке</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {mockFranchises.map((franchise) => (
              <Link
                key={franchise.id}
                to={`/franchise/${franchise.id}`}
                className="group relative rounded-xl overflow-hidden bg-gray-900 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/20"
              >
                <div className="relative aspect-[16/9]">
                  <img
                    src={franchise.image}
                    alt={franchise.name}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/600x338/1f1f2e/8b5cf6?text=Franchise';
                    }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
                  <div className="absolute bottom-0 left-0 right-0 p-4">
                    <h3 className="text-white font-semibold text-lg mb-1">{franchise.name}</h3>
                    <p className="text-gray-300 text-sm mb-2">{franchise.original_name}</p>
                    <p className="text-gray-400 text-xs">
                      {franchise.years} • {franchise.seasons} сезона • {franchise.episodes} эпизодов
                    </p>
                    <p className="text-gray-500 text-xs mt-1">{franchise.duration}</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* Genres */}
        <section className="py-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl md:text-3xl font-bold text-white">Жанры</h2>
            <Link
              to="/genres"
              className="text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1"
            >
              Все жанры
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <p className="text-gray-400 mb-8">Список жанров на любой вкус и цвет</p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {mockGenres.map((genre) => (
              <Link
                key={genre.id}
                to={`/catalog?genre=${genre.id}`}
                className="group relative rounded-xl overflow-hidden bg-gray-900 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/20"
              >
                <div className="relative aspect-[3/4]">
                  <img
                    src={genre.image}
                    alt={genre.name}
                    className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/300x400/1f1f2e/8b5cf6?text=' + genre.name;
                    }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
                  <div className="absolute bottom-0 left-0 right-0 p-4">
                    <h3 className="text-white font-semibold text-lg mb-1">{genre.name}</h3>
                    <p className="text-gray-400 text-sm">{genre.count} релизов</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* Torrents */}
        <section className="py-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl md:text-3xl font-bold text-white">Торренты</h2>
            <Link
              to="/torrents"
              className="text-purple-400 hover:text-purple-300 transition-colors flex items-center gap-1"
            >
              Все торренты
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <p className="text-gray-400 mb-8">Самые свежие торренты: любимая озвучка + оригинальное качество</p>
          <div className="space-y-3">
            {mockTorrents.slice(0, 4).map((torrent) => (
              <div
                key={torrent.id}
                className="bg-gray-900 rounded-xl p-4 hover:bg-gray-800 transition-colors"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-white font-medium">{torrent.release}</h3>
                      {torrent.badge && (
                        <span className="px-2 py-0.5 rounded text-xs bg-green-600/20 text-green-400">
                          {torrent.badge}
                        </span>
                      )}
                    </div>
                    <p className="text-gray-400 text-sm">Эпизоды: {torrent.episodes}</p>
                  </div>
                  <div className="flex items-center gap-6 text-sm">
                    <div className="text-gray-400">
                      <span className="text-white font-medium">{torrent.size}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-green-400">↑ {torrent.seeders}</span>
                      <span className="text-red-400">↓ {torrent.leechers}</span>
                      <span className="text-blue-400"><Download className="w-4 h-4 inline" /> {torrent.downloads}</span>
                    </div>
                    <div className="text-gray-400 text-xs hidden lg:block">
                      {torrent.quality} • {torrent.codec}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default HomePage;