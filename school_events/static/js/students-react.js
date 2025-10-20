// Students List React Component (vanilla JS with React via CDN)
const { useState, useEffect } = React;

function StudentsList() {
  const [students, setStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('name');

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await fetch('/api/students');
      const data = await response.json();
      setStudents(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching students:', error);
      setLoading(false);
    }
  };

  const filterAndSortStudents = () => {
    let filtered = students.filter(student =>
      student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.username.toLowerCase().includes(searchTerm.toLowerCase())
    );

    filtered.sort((a, b) => {
      if (sortBy === 'name') {
        return a.name.localeCompare(b.name, 'cs');
      } else if (sortBy === 'username') {
        return a.username.localeCompare(b.username);
      } else if (sortBy === 'events') {
        return b.event_count - a.event_count;
      }
      return 0;
    });

    return filtered;
  };

  const StudentCard = ({ student }) => (
    React.createElement('div', { className: 'student-card' },
      React.createElement('div', { className: 'student-avatar' },
        React.createElement('span', { className: 'avatar-text' },
          student.name.split(' ').map(n => n[0]).join('').toUpperCase()
        )
      ),
      React.createElement('div', { className: 'student-info' },
        React.createElement('h3', { className: 'student-name' }, student.name),
        React.createElement('div', { className: 'student-stats' },
          React.createElement('div', { className: 'stat-item' },
            React.createElement('span', { className: 'stat-icon' }, '📅'),
            React.createElement('span', { className: 'stat-value' }, student.event_count),
            React.createElement('span', { className: 'stat-label' }, 'akcí')
          )
        ),
        React.createElement('p', { className: 'student-username' }, `@${student.username}`)
      ),
      React.createElement('div', { className: 'student-actions' },
        React.createElement('a', { 
          href: `/student/${student.id}/events`, 
          className: 'btn btn-small' 
        }, 'Zobrazit akce')
      )
    )
  );

  if (loading) {
    return React.createElement('div', { className: 'loading-container' },
      React.createElement('div', { className: 'spinner' }),
      React.createElement('p', null, 'Načítání studentů...')
    );
  }

  const filteredStudents = filterAndSortStudents();

  return React.createElement('div', { className: 'students-container' },
    React.createElement('div', { className: 'students-header' },
      React.createElement('div', { className: 'search-box' },
        React.createElement('span', { className: 'search-icon' }, '🔍'),
        React.createElement('input', {
          type: 'text',
          placeholder: 'Hledat studenta podle jména nebo uživatelského jména...',
          value: searchTerm,
          onChange: (e) => setSearchTerm(e.target.value),
          className: 'search-input'
        }),
        searchTerm && React.createElement('button', {
          className: 'clear-search',
          onClick: () => setSearchTerm(''),
          'aria-label': 'Vymazat hledání'
        }, '✕')
      ),
      React.createElement('div', { className: 'sort-controls' },
        React.createElement('label', null, 'Seřadit podle:'),
        React.createElement('select', {
          value: sortBy,
          onChange: (e) => setSortBy(e.target.value),
          className: 'sort-select'
        },
          React.createElement('option', { value: 'name' }, 'Jméno'),
          React.createElement('option', { value: 'events' }, 'Počet akcí')
        )
      )
    ),
    React.createElement('div', { className: 'students-stats' },
      React.createElement('div', { className: 'stat-card' },
        React.createElement('span', { className: 'stat-number' }, students.length),
        React.createElement('span', { className: 'stat-title' }, 'Celkem studentů')
      ),
      React.createElement('div', { className: 'stat-card' },
        React.createElement('span', { className: 'stat-number' }, filteredStudents.length),
        React.createElement('span', { className: 'stat-title' }, 'Zobrazeno')
      )
    ),
    React.createElement('div', { className: 'students-grid scrollable' },
      filteredStudents.length > 0
        ? filteredStudents.map(student => React.createElement(StudentCard, { key: student.id, student }))
        : React.createElement('p', { className: 'no-results' },
            searchTerm ? 'Žádní studenti nevyhovují vašemu hledání.' : 'Zatím nejsou žádní studenti.')
    )
  );
}
