import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Play, Star, Calendar, Clock, Download, Heart, Share2, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { mockReleases, mockEpisodes } from '../mock';

const ReleasePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const release = mockReleases.find(r => r.id === parseInt(id)) || mockReleases[0];
  const [selectedTab, setSelectedTab] = useState('episodes');

  return (
    <div className="min-h-screen bg-[#0f0f14]">
      {/* Back Button */}
      <div className="container mx-auto px-4 py-4">
        <Button
          variant="ghost"
          className="text-gray-400 hover:text-white"
          onClick={() => navigate(-1)}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Назад
        </Button>
      </div>

      {/* Hero Section */}
      <div className="relative h-[500px] overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0">
          <img
            src={release.poster}
            alt={release.title}
            className="w-full h-full object-cover blur-xl scale-110 opacity-30"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#0f0f14] via-[#0f0f14]/80 to-transparent" />
        </div>

        {/* Content */}
        <div className="relative container mx-auto px-4 h-full flex items-end pb-8">
          <div className="flex flex-col md:flex-row gap-8 w-full">
            {/* Poster */}
            <div className="w-64 flex-shrink-0">
              <div className="rounded-xl overflow-hidden shadow-2xl">
                <img
                  src={release.poster}
                  alt={release.title}
                  className="w-full"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/300x450/1f1f2e/8b5cf6?text=Anime';
                  }}
                />
              </div>
            </div>

            {/* Info */}
            <div className="flex-1">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
                {release.title}
              </h1>
              <p className="text-xl text-gray-300 mb-4">{release.original_title}</p>

              {/* Meta Info */}
              <div className="flex flex-wrap items-center gap-4 mb-6">
                <div className="flex items-center gap-1 text-white">
                  <Star className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                  <span className="font-semibold">{release.rating}</span>
                </div>
                <span className="text-gray-400">{release.year}</span>
                <span className="text-gray-400">{release.season}</span>
                <span className="text-gray-400">{release.type}</span>
                <span className="px-2 py-1 rounded bg-gray-800 text-gray-300 text-sm">
                  {release.age_rating}
                </span>
              </div>

              {/* Genres */}
              <div className="flex flex-wrap gap-2 mb-6">
                {release.genres.map((genre, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 rounded-lg bg-purple-600/20 text-purple-400 text-sm"
                  >
                    {genre}
                  </span>
                ))}
              </div>

              {/* Description */}
              <p className="text-gray-300 text-lg mb-6 max-w-3xl">
                {release.description}
              </p>

              {/* Actions */}
              <div className="flex flex-wrap gap-3">
                <Button
                  size="lg"
                  className="bg-purple-600 hover:bg-purple-700 text-white"
                  onClick={() => navigate(`/watch/${release.id}/1`)}
                >
                  <Play className="w-5 h-5 mr-2" fill="white" />
                  Смотреть
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-gray-700 text-white hover:bg-gray-800"
                >
                  <Heart className="w-5 h-5 mr-2" />
                  В избранное
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="border-gray-700 text-white hover:bg-gray-800"
                >
                  <Share2 className="w-5 h-5 mr-2" />
                  Поделиться
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs Section */}
      <div className="container mx-auto px-4 py-8">
        <Tabs value={selectedTab} onValueChange={setSelectedTab}>
          <TabsList className="bg-gray-900 border-gray-800">
            <TabsTrigger value="episodes" className="data-[state=active]:bg-purple-600">
              Эпизоды ({mockEpisodes.length})
            </TabsTrigger>
            <TabsTrigger value="info" className="data-[state=active]:bg-purple-600">
              Информация
            </TabsTrigger>
            <TabsTrigger value="similar" className="data-[state=active]:bg-purple-600">
              Похожие
            </TabsTrigger>
          </TabsList>

          {/* Episodes */}
          <TabsContent value="episodes" className="mt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {mockEpisodes.map((episode) => (
                <div
                  key={episode.id}
                  className="group relative rounded-xl overflow-hidden bg-gray-900 cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/20"
                  onClick={() => navigate(`/watch/${release.id}/${episode.episode_number}`)}
                >
                  <div className="relative aspect-video">
                    <img
                      src={episode.preview}
                      alt={episode.title}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        e.target.src = 'https://via.placeholder.com/400x225/1f1f2e/8b5cf6?text=Episode+' + episode.episode_number;
                      }}
                    />
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <div className="w-14 h-14 rounded-full bg-purple-600 flex items-center justify-center">
                        <Play className="w-7 h-7 text-white ml-1" fill="white" />
                      </div>
                    </div>
                    <div className="absolute top-2 left-2 px-2 py-1 rounded bg-black/70 backdrop-blur-sm text-white text-sm font-medium">
                      Эпизод {episode.episode_number}
                    </div>
                    <div className="absolute bottom-2 right-2 px-2 py-1 rounded bg-black/70 backdrop-blur-sm text-white text-xs flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {episode.duration}
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="text-white font-medium mb-1">{episode.title}</h3>
                    <p className="text-gray-400 text-sm">
                      {new Date(episode.release_date).toLocaleDateString('ru-RU')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          {/* Info */}
          <TabsContent value="info" className="mt-6">
            <div className="bg-gray-900 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-4">О релизе</h3>
              <div className="space-y-3 text-gray-300">
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Название:</span>
                  <span>{release.title}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Оригинальное:</span>
                  <span>{release.original_title}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Год:</span>
                  <span>{release.year}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Сезон:</span>
                  <span>{release.season}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Тип:</span>
                  <span>{release.type}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Жанры:</span>
                  <span>{release.genres.join(', ')}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Эпизодов:</span>
                  <span>{release.episodes_count}</span>
                </div>
                <div className="flex items-start">
                  <span className="text-gray-400 w-40">Рейтинг:</span>
                  <span>{release.rating} / 10</span>
                </div>
              </div>
            </div>
          </TabsContent>

          {/* Similar */}
          <TabsContent value="similar" className="mt-6">
            <div className="text-center py-12 text-gray-400">
              Похожие релизы скоро появятся здесь
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default ReleasePage;