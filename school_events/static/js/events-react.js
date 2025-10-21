// Events List React Component (vanilla JS with React via CDN)
const { useState, useEffect } = React;

function EventsList() {
  const [events, setEvents] = useState({ current: [], previous: [] });
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

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
      event.description.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const handleRegister = async (eventId) => {
    try {
      const response = await fetch(`/register_event/${eventId}`, {
        method: 'POST',
      });
      if (response.ok) {
        fetchEvents();
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
    React.createElement('div', { 
      className: 'event-card', 
      style: { opacity: isPrevious ? 0.7 : 1, animation: 'fadeIn 0.5s ease-in' }
    },
      React.createElement('div', { className: 'event-header' },
        React.createElement('h3', null, event.title),
        React.createElement('span', { 
          className: `event-status ${isPrevious ? 'past' : 'upcoming'}` 
        }, isPrevious ? 'Proběhlo' : 'Nadcházející')
      ),
      React.createElement('div', { className: 'event-details' },
        React.createElement('p', { className: 'event-description' }, event.description),
        React.createElement('div', { className: 'event-info' },
          React.createElement('div', { className: 'info-item' },
            React.createElement('span', { className: 'icon' }, '📅'),
            React.createElement('span', null, new Date(event.date).toLocaleDateString('cs-CZ'))
          ),
          event.time && React.createElement('div', { className: 'info-item' },
            React.createElement('span', { className: 'icon' }, '⏰'),
            React.createElement('span', null, event.time)
          ),
          event.location && React.createElement('div', { className: 'info-item' },
            React.createElement('span', { className: 'icon' }, '📍'),
            React.createElement('span', null, event.location)
          ),
          React.createElement('div', { className: 'info-item' },
            React.createElement('span', { className: 'icon' }, '👥'),
            React.createElement('span', null, 
              event.max_students 
                ? `${event.registered_count}/${event.max_students} registrováno`
                : `${event.registered_count} registrováno`
            )
          )
        )
      ),
      !isPrevious && !event.is_registered && React.createElement('div', { className: 'event-actions' },
        event.registered_count >= event.max_students 
          ? React.createElement('button', { className: 'btn btn-disabled', disabled: true }, 'Plně obsazeno')
          : React.createElement('button', { 
              className: 'btn btn-primary', 
              onClick: () => handleRegister(event.id) 
            }, 'Registrovat se'),
        React.createElement('a', { 
          href: `/event/${event.id}`, 
          className: 'btn btn-secondary' 
        }, 'Detail akce')
      ),
      !isPrevious && event.is_registered && React.createElement('div', { className: 'event-actions' },
        React.createElement('span', { className: 'registered-badge' }, '✓ Zaregistrován'),
        React.createElement('a', { 
          href: `/event/${event.id}`, 
          className: 'btn btn-secondary' 
        }, 'Detail akce')
      )
    )
  );

  if (loading) {
    return React.createElement('div', { className: 'loading-container' },
      React.createElement('div', { className: 'spinner' }),
      React.createElement('p', null, 'Načítání akcí...')
    );
  }

  const filteredCurrentEvents = filterEvents(events.current);
  const filteredPreviousEvents = filterEvents(events.previous);
  const showCurrent = filter === 'all' || filter === 'current';
  const showPrevious = filter === 'all' || filter === 'previous';

  return React.createElement('div', { className: 'events-container' },
    React.createElement('div', { className: 'search-filter-bar' },
      React.createElement('div', { className: 'search-box' },
        React.createElement('input', {
          type: 'text',
          placeholder: 'Hledat akce...',
          value: searchTerm,
          onChange: (e) => setSearchTerm(e.target.value),
          className: 'search-input',
          spellCheck: 'false',
          autoComplete: 'off',
          autoCorrect: 'off',
          autoCapitalize: 'off',
          'data-gramm': 'false',
          'data-gramm_editor': 'false',
          'data-enable-grammarly': 'false',
          style: { paddingLeft: '2.5rem' }
        }),
        searchTerm && React.createElement('button', {
          className: 'clear-search',
          onClick: () => setSearchTerm(''),
          'aria-label': 'Vymazat hledání'
        }, '✕')
      ),
      React.createElement('div', { className: 'filter-buttons' },
        React.createElement('button', {
          className: `filter-btn ${filter === 'all' ? 'active' : ''}`,
          onClick: () => setFilter('all')
        }, 'Všechny'),
        React.createElement('button', {
          className: `filter-btn ${filter === 'current' ? 'active' : ''}`,
          onClick: () => setFilter('current')
        }, `Nadcházející (${events.current.length})`),
        React.createElement('button', {
          className: `filter-btn ${filter === 'previous' ? 'active' : ''}`,
          onClick: () => setFilter('previous')
        }, `Minulé (${events.previous.length})`)
      )
    ),
    showCurrent && React.createElement('div', { className: 'events-section' },
      React.createElement('h2', { className: 'section-title' },
        `Nadcházející akce${searchTerm ? ` (${filteredCurrentEvents.length})` : ''}`
      ),
      React.createElement('div', { className: 'events-grid scrollable' },
        filteredCurrentEvents.length > 0
          ? filteredCurrentEvents.map(event => React.createElement(EventCard, { key: event.id, event, isPrevious: false }))
          : React.createElement('p', { className: 'no-events' },
              searchTerm ? 'Žádné nadcházející akce nevyhovují vašemu hledání.' : 'Momentálně nejsou žádné nadcházející akce.')
      )
    ),
    showPrevious && React.createElement('div', { className: 'events-section' },
      React.createElement('h2', { className: 'section-title' },
        `Minulé akce${searchTerm ? ` (${filteredPreviousEvents.length})` : ''}`
      ),
      React.createElement('div', { className: 'events-grid scrollable' },
        filteredPreviousEvents.length > 0
          ? filteredPreviousEvents.map(event => React.createElement(EventCard, { key: event.id, event, isPrevious: true }))
          : React.createElement('p', { className: 'no-events' },
              searchTerm ? 'Žádné minulé akce nevyhovují vašemu hledání.' : 'Zatím nejsou žádné minulé akce.')
      )
    )
  );
}
