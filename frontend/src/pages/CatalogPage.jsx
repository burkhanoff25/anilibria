import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Filter, X } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Checkbox } from '../components/ui/checkbox';
import ReleaseCard from '../components/ReleaseCard';
import { mockReleases, mockGenres } from '../mock';

const CatalogPage = () => {
  const [searchParams] = useSearchParams();
  const [showFilters, setShowFilters] = useState(false);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedYear, setSelectedYear] = useState('all');
  const [selectedSeason, setSelectedSeason] = useState('all');
  const [sortBy, setSortBy] = useState('newest');

  const years = ['2026', '2025', '2024', '2023', '2022', '2021', '2020'];
  const seasons = ['Зима', 'Весна', 'Лето', 'Осень'];

  const handleGenreToggle = (genreId) => {
    setSelectedGenres(prev =>
      prev.includes(genreId)
        ? prev.filter(id => id !== genreId)
        : [...prev, genreId]
    );
  };

  const clearFilters = () => {
    setSelectedGenres([]);
    setSelectedYear('all');
    setSelectedSeason('all');
    setSortBy('newest');
  };

  return (
    <div className="min-h-screen bg-[#0f0f14]">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">Каталог аниме</h1>
          <p className="text-gray-400">Найдите своё идеальное аниме среди сотен релизов</p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Filters Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            {/* Mobile Filter Toggle */}
            <Button
              variant="outline"
              className="w-full lg:hidden mb-4 border-gray-700 text-white"
              onClick={() => setShowFilters(!showFilters)}
            >
              <Filter className="w-4 h-4 mr-2" />
              Фильтры
            </Button>

            {/* Filters */}
            <div className={`${showFilters ? 'block' : 'hidden'} lg:block space-y-6`}>
              {/* Clear Filters */}
              <div className="flex items-center justify-between">
                <h3 className="text-white font-semibold">Фильтры</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-purple-400 hover:text-purple-300 p-0 h-auto"
                  onClick={clearFilters}
                >
                  Очистить
                </Button>
              </div>

              {/* Sort By */}
              <div>
                <label className="text-gray-400 text-sm mb-2 block">Сортировка</label>
                <Select value={sortBy} onValueChange={setSortBy}>
                  <SelectTrigger className="bg-gray-900 border-gray-700 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="newest">Новинки</SelectItem>
                    <SelectItem value="popular">Популярные</SelectItem>
                    <SelectItem value="rating">По рейтингу</SelectItem>
                    <SelectItem value="name">По названию</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Year */}
              <div>
                <label className="text-gray-400 text-sm mb-2 block">Год</label>
                <Select value={selectedYear} onValueChange={setSelectedYear}>
                  <SelectTrigger className="bg-gray-900 border-gray-700 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Все годы</SelectItem>
                    {years.map(year => (
                      <SelectItem key={year} value={year}>{year}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Season */}
              <div>
                <label className="text-gray-400 text-sm mb-2 block">Сезон</label>
                <Select value={selectedSeason} onValueChange={setSelectedSeason}>
                  <SelectTrigger className="bg-gray-900 border-gray-700 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Все сезоны</SelectItem>
                    {seasons.map(season => (
                      <SelectItem key={season} value={season}>{season}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Genres */}
              <div>
                <label className="text-gray-400 text-sm mb-3 block">Жанры</label>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {mockGenres.map(genre => (
                    <div key={genre.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={`genre-${genre.id}`}
                        checked={selectedGenres.includes(genre.id)}
                        onCheckedChange={() => handleGenreToggle(genre.id)}
                        className="border-gray-600"
                      />
                      <label
                        htmlFor={`genre-${genre.id}`}
                        className="text-sm text-gray-300 cursor-pointer flex-1"
                      >
                        {genre.name} ({genre.count})
                      </label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Results */}
          <div className="flex-1">
            {/* Results Count */}
            <div className="mb-6 flex items-center justify-between">
              <p className="text-gray-400">Найдено релизов: <span className="text-white font-medium">{mockReleases.length}</span></p>
            </div>

            {/* Releases Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {mockReleases.map((release) => (
                <ReleaseCard key={release.id} release={release} />
              ))}
            </div>

            {/* Load More */}
            <div className="mt-8 text-center">
              <Button
                variant="outline"
                className="border-gray-700 text-white hover:bg-gray-800"
              >
                Загрузить ещё
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CatalogPage;