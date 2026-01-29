import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import CatalogPage from './pages/CatalogPage';
import ReleasePage from './pages/ReleasePage';
import WatchPage from './pages/WatchPage';
import SchedulePage from './pages/SchedulePage';
import TorrentsPage from './pages/TorrentsPage';
import { Toaster } from './components/ui/sonner';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/catalog" element={<CatalogPage />} />
            <Route path="/release/:id" element={<ReleasePage />} />
            <Route path="/watch/:releaseId/:episodeNumber" element={<WatchPage />} />
            <Route path="/schedule" element={<SchedulePage />} />
            <Route path="/torrents" element={<TorrentsPage />} />
          </Routes>
        </main>
        <Footer />
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;