import React from 'react';
import { Link } from 'react-router-dom';
import { Film, Youtube, MessageCircle } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-[#0a0a0e] border-t border-gray-800 mt-20">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Logo & Description */}
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center">
                <Film className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">AniLiberty</span>
            </Link>
            <p className="text-gray-400 text-sm max-w-md">
              AniLiberty — так звучит аниме! Смотрите аниме онлайн в русской озвучке совершенно бесплатно.
            </p>
            <div className="flex gap-4 mt-6">
              <a
                href="https://youtube.com"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 rounded-lg bg-gray-800 hover:bg-gray-700 flex items-center justify-center transition-colors"
              >
                <Youtube className="w-5 h-5 text-gray-300" />
              </a>
              <a
                href="https://t.me"
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 rounded-lg bg-gray-800 hover:bg-gray-700 flex items-center justify-center transition-colors"
              >
                <MessageCircle className="w-5 h-5 text-gray-300" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Навигация</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/catalog" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Каталог аниме
                </Link>
              </li>
              <li>
                <Link to="/schedule" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Расписание
                </Link>
              </li>
              <li>
                <Link to="/torrents" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Торренты
                </Link>
              </li>
              <li>
                <Link to="/team" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Команда
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-white font-semibold mb-4">Поддержка</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/support" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Поддержать проект
                </Link>
              </li>
              <li>
                <Link to="/faq" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Частые вопросы
                </Link>
              </li>
              <li>
                <Link to="/contacts" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Контакты
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-gray-400 hover:text-white transition-colors text-sm">
                  Политика конфиденциальности
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>© 2026 AniLiberty. Все права защищены.</p>
          <p className="mt-2">Сайт не содержит аниме, только ссылки на них.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;