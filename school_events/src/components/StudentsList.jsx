import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';

const StudentsList = () => {
  const [students, setStudents] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('name'); // 'name', 'username', 'events'

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

    // Sort students
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
    <div className="student-card">
      <div className="student-avatar">
        <span className="avatar-text">
          {student.name.split(' ').map(n => n[0]).join('').toUpperCase()}
        </span>
      </div>
      <div className="student-info">
        <h3 className="student-name">{student.name}</h3>
        <p className="student-username">@{student.username}</p>
        <div className="student-stats">
          <div className="stat-item">
            <span className="stat-icon">📅</span>
            <span className="stat-value">{student.event_count}</span>
            <span className="stat-label">akcí</span>
          </div>
        </div>
      </div>
      <div className="student-actions">
        <a href={`/student/${student.id}/events`} className="btn btn-small">
          Zobrazit akce
        </a>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Načítání studentů...</p>
      </div>
    );
  }

  const filteredStudents = filterAndSortStudents();

  return (
    <div className="students-container">
      <div className="students-header">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Hledat studenta podle jména nebo uživatelského jména..."
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
        <div className="sort-controls">
          <label>Seřadit podle:</label>
          <select 
            value={sortBy} 
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="name">Jméno</option>
            <option value="username">Uživatelské jméno</option>
            <option value="events">Počet akcí</option>
          </select>
        </div>
      </div>

      <div className="students-stats">
        <div className="stat-card">
          <span className="stat-number">{students.length}</span>
          <span className="stat-title">Celkem studentů</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{filteredStudents.length}</span>
          <span className="stat-title">Zobrazeno</span>
        </div>
      </div>

      <div className="students-grid scrollable">
        {filteredStudents.length > 0 ? (
          filteredStudents.map(student => (
            <StudentCard key={student.id} student={student} />
          ))
        ) : (
          <p className="no-results">
            {searchTerm ? 'Žádní studenti nevyhovují vašemu hledání.' : 'Zatím nejsou žádní studenti.'}
          </p>
        )}
      </div>
    </div>
  );
};

// Mount the component
const root = document.getElementById('students-react-root');
if (root) {
  ReactDOM.createRoot(root).render(<StudentsList />);
}

export default StudentsList;
