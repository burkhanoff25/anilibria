import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, Menu, X, Home, Grid, Calendar, Film, Download, Users } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-[#0f0f14]/95 backdrop-blur-sm border-b border-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
              <Film className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white hidden md:block">AniLiberty</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-6">
            <Link to="/" className="text-gray-300 hover:text-white transition-colors flex items-center gap-2">
              <Home className="w-4 h-4" />
              Главная
            </Link>
            <Link to="/catalog" className="text-gray-300 hover:text-white transition-colors flex items-center gap-2">
              <Grid className="w-4 h-4" />
              Каталог
            </Link>
            <Link to="/schedule" className="text-gray-300 hover:text-white transition-colors flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Расписание
            </Link>
            <Link to="/torrents" className="text-gray-300 hover:text-white transition-colors flex items-center gap-2">
              <Download className="w-4 h-4" />
              Торренты
            </Link>
            <Link to="/team" className="text-gray-300 hover:text-white transition-colors flex items-center gap-2">
              <Users className="w-4 h-4" />
              Команда
            </Link>
          </nav>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="hidden md:flex items-center gap-2 flex-1 max-w-md mx-4">
            <div className="relative flex-1">
              <Input
                type="text"
                placeholder="Поиск аниме..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-gray-900 border-gray-700 text-white placeholder:text-gray-500 pr-10"
              />
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            </div>
          </form>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden text-white"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </Button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden py-4 border-t border-gray-800">
            <nav className="flex flex-col gap-4">
              <Link
                to="/"
                className="text-gray-300 hover:text-white transition-colors flex items-center gap-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                <Home className="w-4 h-4" />
                Главная
              </Link>
              <Link
                to="/catalog"
                className="text-gray-300 hover:text-white transition-colors flex items-center gap-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                <Grid className="w-4 h-4" />
                Каталог
              </Link>
              <Link
                to="/schedule"
                className="text-gray-300 hover:text-white transition-colors flex items-center gap-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                <Calendar className="w-4 h-4" />
                Расписание
              </Link>
              <Link
                to="/torrents"
                className="text-gray-300 hover:text-white transition-colors flex items-center gap-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                <Download className="w-4 h-4" />
                Торренты
              </Link>
              <Link
                to="/team"
                className="text-gray-300 hover:text-white transition-colors flex items-center gap-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                <Users className="w-4 h-4" />
                Команда
              </Link>
            </nav>
            <form onSubmit={handleSearch} className="mt-4">
              <div className="relative">
                <Input
                  type="text"
                  placeholder="Поиск аниме..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="bg-gray-900 border-gray-700 text-white placeholder:text-gray-500 pr-10"
                />
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
              </div>
            </form>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;