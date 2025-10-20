import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';

const EventsList = () => {
  const [events, setEvents] = useState({ current: [], previous: [] });
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // 'all', 'current', 'previous'

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await fetch('/api/events');
      const data = await response.json();
      setEvents(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching events:', error);
      setLoading(false);
    }
  };

  const filterEvents = (eventsList) => {
    return eventsList.filter(event =>
      event.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      event.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      event.location.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const handleRegister = async (eventId) => {
    try {
      const response = await fetch(`/register_event/${eventId}`, {
        method: 'POST',
      });
      if (response.ok) {
        fetchEvents(); // Refresh events
        alert('Úspěšně jste se zaregistrovali na akci!');
      } else {
        const data = await response.json();
        alert(data.message || 'Chyba při registraci');
      }
    } catch (error) {
      console.error('Error registering:', error);
      alert('Chyba při registraci');
    }
  };

  const EventCard = ({ event, isPrevious }) => (
    <div className="event-card" style={{ 
      opacity: isPrevious ? 0.7 : 1,
      animation: 'fadeIn 0.5s ease-in'
    }}>
      <div className="event-header">
        <h3>{event.title}</h3>
        <span className={`event-status ${isPrevious ? 'past' : 'upcoming'}`}>
          {isPrevious ? 'Proběhlo' : 'Nadcházející'}
        </span>
      </div>
      <div className="event-details">
        <p className="event-description">{event.description}</p>
        <div className="event-info">
          <div className="info-item">
            <span className="icon">📅</span>
            <span>{new Date(event.date).toLocaleDateString('cs-CZ')}</span>
          </div>
          <div className="info-item">
            <span className="icon">⏰</span>
            <span>{event.time}</span>
          </div>
          <div className="info-item">
            <span className="icon">📍</span>
            <span>{event.location}</span>
          </div>
          <div className="info-item">
            <span className="icon">👥</span>
            <span>{event.registered_count}/{event.max_students} registrováno</span>
          </div>
        </div>
      </div>
      {!isPrevious && !event.is_registered && (
        <div className="event-actions">
          {event.registered_count >= event.max_students ? (
            <button className="btn btn-disabled" disabled>Plně obsazeno</button>
          ) : (
            <button 
              className="btn btn-primary" 
              onClick={() => handleRegister(event.id)}
            >
              Registrovat se
            </button>
          )}
          <a href={`/event/${event.id}`} className="btn btn-secondary">
            Detail akce
          </a>
        </div>
      )}
      {!isPrevious && event.is_registered && (
        <div className="event-actions">
          <span className="registered-badge">✓ Zaregistrován</span>
          <a href={`/event/${event.id}`} className="btn btn-secondary">
            Detail akce
          </a>
        </div>
      )}
    </div>
  );

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Načítání akcí...</p>
      </div>
    );
  }

  const filteredCurrentEvents = filterEvents(events.current);
  const filteredPreviousEvents = filterEvents(events.previous);
  const showCurrent = filter === 'all' || filter === 'current';
  const showPrevious = filter === 'all' || filter === 'previous';

  return (
    <div className="events-container">
      <div className="search-filter-bar">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Hledat akce podle názvu, popisu nebo místa..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          {searchTerm && (
            <button 
              className="clear-search" 
              onClick={() => setSearchTerm('')}
              aria-label="Vymazat hledání"
            >
              ✕
            </button>
          )}
        </div>
        <div className="filter-buttons">
          <button
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            Všechny
          </button>
          <button
            className={`filter-btn ${filter === 'current' ? 'active' : ''}`}
            onClick={() => setFilter('current')}
          >
            Nadcházející ({events.current.length})
          </button>
          <button
            className={`filter-btn ${filter === 'previous' ? 'active' : ''}`}
            onClick={() => setFilter('previous')}
          >
            Minulé ({events.previous.length})
          </button>
        </div>
      </div>

      {showCurrent && (
        <div className="events-section">
          <h2 className="section-title">
            Nadcházející akce
            {searchTerm && ` (${filteredCurrentEvents.length})`}
          </h2>
          <div className="events-grid scrollable">
            {filteredCurrentEvents.length > 0 ? (
              filteredCurrentEvents.map(event => (
                <EventCard key={event.id} event={event} isPrevious={false} />
              ))
            ) : (
              <p className="no-events">
                {searchTerm ? 'Žádné nadcházející akce nevyhovují vašemu hledání.' : 'Momentálně nejsou žádné nadcházející akce.'}
              </p>
            )}
          </div>
        </div>
      )}

      {showPrevious && (
        <div className="events-section">
          <h2 className="section-title">
            Minulé akce
            {searchTerm && ` (${filteredPreviousEvents.length})`}
          </h2>
          <div className="events-grid scrollable">
            {filteredPreviousEvents.length > 0 ? (
              filteredPreviousEvents.map(event => (
                <EventCard key={event.id} event={event} isPrevious={true} />
              ))
            ) : (
              <p className="no-events">
                {searchTerm ? 'Žádné minulé akce nevyhovují vašemu hledání.' : 'Zatím nejsou žádné minulé akce.'}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Mount the component
const root = document.getElementById('events-react-root');
if (root) {
  ReactDOM.createRoot(root).render(<EventsList />);
}

export default EventsList;
