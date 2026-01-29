import React, { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Play, Pause, Volume2, VolumeX, Maximize, Settings, SkipBack, SkipForward, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Slider } from '../components/ui/slider';
import { mockReleases, mockEpisodes } from '../mock';

const WatchPage = () => {
  const { releaseId, episodeNumber } = useParams();
  const navigate = useNavigate();
  const release = mockReleases.find(r => r.id === parseInt(releaseId)) || mockReleases[0];
  const currentEpisode = mockEpisodes.find(e => e.episode_number === parseInt(episodeNumber)) || mockEpisodes[0];
  
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(100);
  const [isMuted, setIsMuted] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [showControls, setShowControls] = useState(true);
  const videoRef = useRef(null);
  const controlsTimeoutRef = useRef(null);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleVolumeChange = (value) => {
    setVolume(value[0]);
    setIsMuted(value[0] === 0);
  };

  const handlePreviousEpisode = () => {
    const prevEpisode = parseInt(episodeNumber) - 1;
    if (prevEpisode >= 1) {
      navigate(`/watch/${releaseId}/${prevEpisode}`);
    }
  };

  const handleNextEpisode = () => {
    const nextEpisode = parseInt(episodeNumber) + 1;
    if (nextEpisode <= mockEpisodes.length) {
      navigate(`/watch/${releaseId}/${nextEpisode}`);
    }
  };

  const handleMouseMove = () => {
    setShowControls(true);
    if (controlsTimeoutRef.current) {
      clearTimeout(controlsTimeoutRef.current);
    }
    controlsTimeoutRef.current = setTimeout(() => {
      if (isPlaying) {
        setShowControls(false);
      }
    }, 3000);
  };

  useEffect(() => {
    return () => {
      if (controlsTimeoutRef.current) {
        clearTimeout(controlsTimeoutRef.current);
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#0f0f14]">
      {/* Back Button */}
      <div className="container mx-auto px-4 py-4">
        <Button
          variant="ghost"
          className="text-gray-400 hover:text-white"
          onClick={() => navigate(`/release/${releaseId}`)}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          К релизу
        </Button>
      </div>

      <div className="container mx-auto px-4 pb-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Video Player */}
          <div className="lg:col-span-2">
            {/* Player Container */}
            <div
              className="relative bg-black rounded-xl overflow-hidden aspect-video group"
              onMouseMove={handleMouseMove}
              onMouseLeave={() => isPlaying && setShowControls(false)}
            >
              {/* Video Placeholder */}
              <div className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-purple-900/20 to-pink-900/20">
                <div className="text-center">
                  <Play className="w-24 h-24 text-white/50 mx-auto mb-4" />
                  <p className="text-white/70 text-lg">Видеоплеер (демо)</p>
                  <p className="text-white/50 text-sm mt-2">
                    Эпизод {episodeNumber}: {currentEpisode.title}
                  </p>
                </div>
              </div>

              {/* Controls Overlay */}
              <div
                className={`absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/50 transition-opacity duration-300 ${
                  showControls ? 'opacity-100' : 'opacity-0'
                }`}
              >
                {/* Top Bar */}
                <div className="absolute top-0 left-0 right-0 p-4">
                  <h2 className="text-white font-semibold">
                    {release.title} - Эпизод {episodeNumber}
                  </h2>
                  <p className="text-gray-300 text-sm">{currentEpisode.title}</p>
                </div>

                {/* Center Play Button */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <button
                    onClick={handlePlayPause}
                    className="w-20 h-20 rounded-full bg-purple-600/80 hover:bg-purple-600 flex items-center justify-center transition-all transform hover:scale-110"
                  >
                    {isPlaying ? (
                      <Pause className="w-10 h-10 text-white" fill="white" />
                    ) : (
                      <Play className="w-10 h-10 text-white ml-1" fill="white" />
                    )}
                  </button>
                </div>

                {/* Bottom Controls */}
                <div className="absolute bottom-0 left-0 right-0 p-4">
                  {/* Progress Bar */}
                  <div className="mb-4">
                    <Slider
                      value={[currentTime]}
                      max={100}
                      step={0.1}
                      className="cursor-pointer"
                      onValueChange={(value) => setCurrentTime(value[0])}
                    />
                    <div className="flex justify-between text-xs text-white mt-1">
                      <span>{formatTime(currentTime)}</span>
                      <span>{currentEpisode.duration}</span>
                    </div>
                  </div>

                  {/* Control Buttons */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {/* Play/Pause */}
                      <Button
                        size="icon"
                        variant="ghost"
                        className="text-white hover:bg-white/20"
                        onClick={handlePlayPause}
                      >
                        {isPlaying ? (
                          <Pause className="w-5 h-5" />
                        ) : (
                          <Play className="w-5 h-5" />
                        )}
                      </Button>

                      {/* Previous Episode */}
                      <Button
                        size="icon"
                        variant="ghost"
                        className="text-white hover:bg-white/20"
                        onClick={handlePreviousEpisode}
                        disabled={parseInt(episodeNumber) === 1}
                      >
                        <SkipBack className="w-5 h-5" />
                      </Button>

                      {/* Next Episode */}
                      <Button
                        size="icon"
                        variant="ghost"
                        className="text-white hover:bg-white/20"
                        onClick={handleNextEpisode}
                        disabled={parseInt(episodeNumber) === mockEpisodes.length}
                      >
                        <SkipForward className="w-5 h-5" />
                      </Button>

                      {/* Volume */}
                      <div className="flex items-center gap-2">
                        <Button
                          size="icon"
                          variant="ghost"
                          className="text-white hover:bg-white/20"
                          onClick={() => setIsMuted(!isMuted)}
                        >
                          {isMuted || volume === 0 ? (
                            <VolumeX className="w-5 h-5" />
                          ) : (
                            <Volume2 className="w-5 h-5" />
                          )}
                        </Button>
                        <Slider
                          value={[isMuted ? 0 : volume]}
                          max={100}
                          step={1}
                          className="w-24"
                          onValueChange={handleVolumeChange}
                        />
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      {/* Settings */}
                      <Button
                        size="icon"
                        variant="ghost"
                        className="text-white hover:bg-white/20"
                      >
                        <Settings className="w-5 h-5" />
                      </Button>

                      {/* Fullscreen */}
                      <Button
                        size="icon"
                        variant="ghost"
                        className="text-white hover:bg-white/20"
                      >
                        <Maximize className="w-5 h-5" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Episode Info */}
            <div className="mt-6 bg-gray-900 rounded-xl p-6">
              <h2 className="text-2xl font-bold text-white mb-2">
                Эпизод {episodeNumber}: {currentEpisode.title}
              </h2>
              <p className="text-gray-400 mb-4">
                {release.title} ({release.original_title})
              </p>
              <div className="flex items-center gap-4 text-sm text-gray-400">
                <span>Длительность: {currentEpisode.duration}</span>
                <span>•</span>
                <span>Дата выхода: {new Date(currentEpisode.release_date).toLocaleDateString('ru-RU')}</span>
              </div>
            </div>
          </div>

          {/* Episodes List */}
          <div className="lg:col-span-1">
            <div className="bg-gray-900 rounded-xl p-4 sticky top-20">
              <h3 className="text-white font-semibold mb-4">Все эпизоды</h3>
              <div className="space-y-2 max-h-[600px] overflow-y-auto">
                {mockEpisodes.map((episode) => (
                  <button
                    key={episode.id}
                    onClick={() => navigate(`/watch/${releaseId}/${episode.episode_number}`)}
                    className={`w-full text-left p-3 rounded-lg transition-colors ${
                      episode.episode_number === parseInt(episodeNumber)
                        ? 'bg-purple-600 text-white'
                        : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium">Эпизод {episode.episode_number}</span>
                      <span className="text-xs">{episode.duration}</span>
                    </div>
                    <p className="text-sm opacity-80 line-clamp-1">{episode.title}</p>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WatchPage;