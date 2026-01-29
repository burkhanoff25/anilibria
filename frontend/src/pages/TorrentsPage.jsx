import React from 'react';
import { Download, ArrowUpCircle, ArrowDownCircle, HardDrive, Clock } from 'lucide-react';
import { Button } from '../components/ui/button';
import { mockTorrents } from '../mock';

const TorrentsPage = () => {
  return (
    <div className="min-h-screen bg-[#0f0f14]">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Download className="w-8 h-8 text-purple-400" />
            <h1 className="text-3xl md:text-4xl font-bold text-white">Торренты</h1>
          </div>
          <p className="text-gray-400">
            Самые свежие торренты: любимая озвучка + оригинальное качество
          </p>
        </div>

        {/* Torrents List */}
        <div className="space-y-4">
          {mockTorrents.map((torrent) => (
            <div
              key={torrent.id}
              className="bg-gray-900 rounded-xl p-6 hover:bg-gray-800 transition-colors"
            >
              {/* Title & Badge */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-white font-semibold text-lg">{torrent.release}</h3>
                    {torrent.badge && (
                      <span className="px-3 py-1 rounded-lg text-xs bg-green-600/20 text-green-400 font-medium">
                        {torrent.badge}
                      </span>
                    )}
                  </div>
                  <p className="text-gray-400 text-sm">Эпизоды: {torrent.episodes}</p>
                </div>
                <Button className="bg-purple-600 hover:bg-purple-700 text-white">
                  <Download className="w-4 h-4 mr-2" />
                  Скачать
                </Button>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {/* Size */}
                <div className="flex items-center gap-2">
                  <HardDrive className="w-4 h-4 text-gray-400" />
                  <div>
                    <p className="text-xs text-gray-400">Размер</p>
                    <p className="text-white font-medium">{torrent.size}</p>
                  </div>
                </div>

                {/* Seeders */}
                <div className="flex items-center gap-2">
                  <ArrowUpCircle className="w-4 h-4 text-green-400" />
                  <div>
                    <p className="text-xs text-gray-400">Сиды</p>
                    <p className="text-green-400 font-medium">{torrent.seeders}</p>
                  </div>
                </div>

                {/* Leechers */}
                <div className="flex items-center gap-2">
                  <ArrowDownCircle className="w-4 h-4 text-red-400" />
                  <div>
                    <p className="text-xs text-gray-400">Личеры</p>
                    <p className="text-red-400 font-medium">{torrent.leechers}</p>
                  </div>
                </div>

                {/* Downloads */}
                <div className="flex items-center gap-2">
                  <Download className="w-4 h-4 text-blue-400" />
                  <div>
                    <p className="text-xs text-gray-400">Скачивания</p>
                    <p className="text-blue-400 font-medium">{torrent.downloads}</p>
                  </div>
                </div>

                {/* Date */}
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-gray-400" />
                  <div>
                    <p className="text-xs text-gray-400">Дата</p>
                    <p className="text-white font-medium text-xs">{torrent.date}</p>
                  </div>
                </div>
              </div>

              {/* Quality Info */}
              <div className="mt-4 pt-4 border-t border-gray-800">
                <div className="flex flex-wrap gap-2 text-sm">
                  <span className="px-3 py-1 rounded-lg bg-gray-800 text-gray-300">
                    {torrent.quality}
                  </span>
                  <span className="px-3 py-1 rounded-lg bg-gray-800 text-gray-300">
                    {torrent.codec}
                  </span>
                  <span className="px-3 py-1 rounded-lg bg-gray-800 text-gray-300">
                    WEBRip
                  </span>
                  <span className="px-3 py-1 rounded-lg bg-gray-800 text-gray-300">
                    8-bit
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Info Box */}
        <div className="mt-12 bg-gradient-to-r from-purple-900/20 to-pink-900/20 rounded-xl p-6 border border-purple-500/20">
          <h3 className="text-white font-semibold text-lg mb-2">Информация</h3>
          <div className="text-gray-300 text-sm space-y-2">
            <p>• Все торренты содержат русскую озвучку от команды AniLiberty</p>
            <p>• HEVC версии имеют меньший размер при сохранении качества</p>
            <p>• Для просмотра HEVC может потребоваться современный плеер</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TorrentsPage;