import React from 'react';
import { Link } from 'react-router-dom';
import { Play, Star } from 'lucide-react';

const ReleaseCard = ({ release }) => {
  return (
    <Link
      to={`/release/${release.id}`}
      className="group relative block rounded-xl overflow-hidden bg-gray-900 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-purple-500/20"
    >
      {/* Poster */}
      <div className="relative aspect-[2/3] overflow-hidden">
        <img
          src={release.poster}
          alt={release.title}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/300x450/1f1f2e/8b5cf6?text=Anime';
          }}
        />
        
        {/* Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-16 h-16 rounded-full bg-purple-600 flex items-center justify-center transform scale-0 group-hover:scale-100 transition-transform duration-300">
              <Play className="w-8 h-8 text-white ml-1" fill="white" />
            </div>
          </div>
        </div>

        {/* Episode Count Badge */}
        {release.episodes_count && (
          <div className="absolute top-2 right-2 px-2 py-1 rounded-lg bg-black/70 backdrop-blur-sm text-xs text-white font-medium">
            {release.episodes_count} эп.
          </div>
        )}

        {/* Rating Badge */}
        {release.rating && (
          <div className="absolute top-2 left-2 px-2 py-1 rounded-lg bg-black/70 backdrop-blur-sm text-xs text-white font-medium flex items-center gap-1">
            <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
            {release.rating}
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-4">
        <h3 className="text-white font-semibold text-sm line-clamp-2 mb-1 group-hover:text-purple-400 transition-colors">
          {release.title}
        </h3>
        <p className="text-gray-400 text-xs line-clamp-1 mb-2">
          {release.original_title}
        </p>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <span>{release.year}</span>
          <span>•</span>
          <span>{release.season}</span>
          <span>•</span>
          <span>{release.type}</span>
        </div>
        {release.genres && release.genres.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {release.genres.slice(0, 2).map((genre, index) => (
              <span
                key={index}
                className="px-2 py-0.5 rounded text-xs bg-purple-600/20 text-purple-400"
              >
                {genre}
              </span>
            ))}
          </div>
        )}
      </div>
    </Link>
  );
};

export default ReleaseCard;