import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Clock, Play } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { mockSchedule } from '../mock';

const SchedulePage = () => {
  const [selectedDay, setSelectedDay] = useState('today');

  const renderScheduleItems = (items) => {
    if (items.length === 0) {
      return (
        <div className="text-center py-12 text-gray-400">
          На этот день релизов не запланировано
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((item, index) => (
          <Link
            key={`${item.id}-${index}`}
            to={`/release/${item.id}`}
            className="group relative rounded-xl overflow-hidden bg-gray-900 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/20"
          >
            <div className="relative aspect-video">
              <img
                src={item.poster}
                alt={item.title}
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/400x225/1f1f2e/8b5cf6?text=Episode';
                }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
              
              {/* Play Button Overlay */}
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-14 h-14 rounded-full bg-purple-600 flex items-center justify-center">
                  <Play className="w-7 h-7 text-white ml-1" fill="white" />
                </div>
              </div>

              {/* Episode Badge */}
              <div className="absolute top-3 left-3 px-3 py-1.5 rounded-lg bg-black/70 backdrop-blur-sm text-white text-sm font-medium">
                Эпизод {item.episode}
              </div>

              {/* Duration Badge */}
              <div className="absolute top-3 right-3 px-2 py-1 rounded-lg bg-black/70 backdrop-blur-sm text-white text-xs flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {item.duration}
              </div>

              {/* Title */}
              <div className="absolute bottom-0 left-0 right-0 p-4">
                <h3 className="text-white font-semibold text-lg line-clamp-2 group-hover:text-purple-400 transition-colors">
                  {item.title}
                </h3>
              </div>
            </div>
          </Link>
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#0f0f14]">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Calendar className="w-8 h-8 text-purple-400" />
            <h1 className="text-3xl md:text-4xl font-bold text-white">Расписание релизов</h1>
          </div>
          <p className="text-gray-400">
            Список релизов, над которыми команда трудится прямо сейчас
          </p>
        </div>

        {/* Tabs */}
        <Tabs value={selectedDay} onValueChange={setSelectedDay}>
          <TabsList className="bg-gray-900 border-gray-800 mb-8">
            <TabsTrigger value="yesterday" className="data-[state=active]:bg-purple-600">
              Вчера
            </TabsTrigger>
            <TabsTrigger value="today" className="data-[state=active]:bg-purple-600">
              Сегодня
            </TabsTrigger>
            <TabsTrigger value="tomorrow" className="data-[state=active]:bg-purple-600">
              Завтра
            </TabsTrigger>
          </TabsList>

          <TabsContent value="yesterday">
            {renderScheduleItems(mockSchedule.yesterday)}
          </TabsContent>

          <TabsContent value="today">
            {renderScheduleItems(mockSchedule.today)}
          </TabsContent>

          <TabsContent value="tomorrow">
            {renderScheduleItems(mockSchedule.tomorrow)}
          </TabsContent>
        </Tabs>

        {/* Info Box */}
        <div className="mt-12 bg-gradient-to-r from-purple-900/20 to-pink-900/20 rounded-xl p-6 border border-purple-500/20">
          <h3 className="text-white font-semibold text-lg mb-2">Информация о расписании</h3>
          <p className="text-gray-300 text-sm">
            Расписание может изменяться. Время выхода эпизодов указано приблизительно.
            Подпишитесь на наши социальные сети, чтобы не пропустить выход новых эпизодов!
          </p>
        </div>
      </div>
    </div>
  );
};

export default SchedulePage;